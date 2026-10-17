#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "button_output.h"
#include "bridge_policy.h"
#include "driver/gpio.h"
#include "driver/gptimer.h"
#include "freertos/portmacro.h"

static int level = -1, rising_edges, calls, depth, driver_attempts;
static bool running, pending_alarm, initialized;
static bool low_failed_once;
static const char *scenario;
static bool (*alarm_callback)(gptimer_handle_t, const gptimer_alarm_event_data_t *, void *);
static void (*shutdown_callback)(void);
static bridge_policy_t policy;
static const char *boot = "0123456789abcdef0123456789abcdef";
static bool is(const char *name) { return strcmp(scenario, name) == 0; }

static void deliver_alarm(void) {
    assert(depth == 0);
    pending_alarm = false;
    assert(!alarm_callback((void *)1, NULL, NULL));
}
static void request_alarm(void) {
    pending_alarm = true;
    if (depth == 0) deliver_alarm();
}
void test_enter_critical(portMUX_TYPE *lock) { (void)lock; ++depth; }
void test_exit_critical(portMUX_TYPE *lock) {
    (void)lock; assert(depth > 0);
    if (--depth == 0 && pending_alarm) deliver_alarm();
}
esp_err_t gpio_set_level(int pin, int value) {
    assert(pin == 3);
    if (value == 1) {
        assert(depth > 0 && running); /* Arm before asserting; release cannot interleave. */
        assert(policy.last_sequence == 1); /* Consumed before any possible HIGH. */
        if (level != 1) ++rising_edges;
    }
    ++calls;
    if (initialized && value == 0 && is("release_low_fail")) return ESP_FAIL;
    if (initialized && value == 0 && is("assert_and_release_fail") && !low_failed_once) {
        low_failed_once = true;
        return ESP_FAIL;
    }
    level = value;
    if (value == 1 && is("alarm_at_assert")) request_alarm();
    return value == 1 && (is("assert_fail") || is("assert_and_release_fail")) ? ESP_FAIL : ESP_OK;
}
esp_err_t gpio_config(const gpio_config_t *config) {
    assert(calls == 1 && level == 0);
    assert(config->pin_bit_mask == (1ULL << 3));
    return ESP_OK;
}
esp_err_t esp_register_shutdown_handler(void (*fn)(void)) {shutdown_callback = fn; return ESP_OK;}
esp_err_t gptimer_new_timer(const gptimer_config_t *c, gptimer_handle_t *t) {
    assert(c->resolution_hz == 1000000); *t = (void *)1; return ESP_OK;
}
esp_err_t gptimer_register_event_callbacks(gptimer_handle_t t, const gptimer_event_callbacks_t *c, void *arg) {
    (void)t; (void)arg; alarm_callback = c->on_alarm; return ESP_OK;
}
esp_err_t gptimer_enable(gptimer_handle_t t) {(void)t; return ESP_OK;}
esp_err_t gptimer_set_raw_count(gptimer_handle_t t, uint64_t count) {
    (void)t; ++driver_attempts; assert(count == 0); return is("count_fail") ? ESP_FAIL : ESP_OK;
}
esp_err_t gptimer_set_alarm_action(gptimer_handle_t t, const gptimer_alarm_config_t *c) {
    (void)t; assert(c->alarm_count == 200000);
    if (is("shutdown_during_arm")) shutdown_callback();
    return is("arm_fail") ? ESP_FAIL : ESP_OK;
}
esp_err_t gptimer_start(gptimer_handle_t t) {
    (void)t; assert(depth > 0);
    if (is("start_fail")) return ESP_FAIL;
    running = true;
    if (is("alarm_at_start") || is("start_failed_after_arm")) request_alarm();
    return is("start_failed_after_arm") ? ESP_FAIL : ESP_OK;
}
esp_err_t gptimer_stop(gptimer_handle_t t) {
    (void)t; assert(depth > 0);
    if (is("stop_fail")) return ESP_FAIL;
    running = false; return ESP_OK;
}

/* Execute the production transaction used by the HTTP handler. */
static bridge_decision_t attempt(button_output_result_t *result, uint64_t now) {
    return button_output_attempt(&policy, boot, 1, now + 5000, now, result);
}

int main(int argc, char **argv) {
    assert(argc == 2); scenario = argv[1];
    bridge_policy_init(&policy, boot);
    button_output_init(); initialized = true;
    assert(level == 0 && rising_edges == 0 && !button_output_active() && !button_output_faulted());
    button_output_result_t result;
    assert(attempt(&result, 0) == BRIDGE_ACCEPT);
    bool pre_assert_failure = is("count_fail") || is("arm_fail") || is("start_fail") ||
        is("start_failed_after_arm") || is("shutdown_during_arm");
    if (pre_assert_failure) {
        assert(result.error != ESP_OK && !result.may_have_asserted);
        assert(rising_edges == 0 && level == 0 && !running && !button_output_active());
        assert(button_output_faulted());
    } else if (is("assert_fail")) {
        assert(result.error != ESP_OK && result.may_have_asserted && rising_edges == 1);
        assert(level == 0 && !running && !button_output_active() && button_output_faulted());
    } else if (is("assert_and_release_fail")) {
        assert(result.error != ESP_OK && result.may_have_asserted && rising_edges == 1);
        assert(level == 1 && running && button_output_active() && button_output_faulted());
        request_alarm(); /* The armed release was retained after the failed LOW. */
        assert(level == 0 && !running && !button_output_active() && button_output_faulted());
    } else {
        assert(result.error == ESP_OK && result.may_have_asserted && rising_edges == 1);
        if (is("alarm_at_start") || is("alarm_at_assert")) {
            assert(level == 0 && !running && !button_output_active());
        } else {
            assert(level == 1 && running && button_output_active());
            assert(button_output_press().error == ESP_ERR_INVALID_STATE && rising_edges == 1);
            if (is("shutdown")) shutdown_callback(); else request_alarm();
        }
        if (is("release_low_fail")) {
            assert(level == 1 && running && button_output_active() && button_output_faulted());
        } else {
            assert(level == 0 && !button_output_active());
            assert(running == is("stop_fail"));
            assert(button_output_faulted() == (is("stop_fail") || is("shutdown")));
        }
    }
    /* Even a failed/uncertain attempt consumes its sequence, across cooldown. */
    for (int now = 1; now <= 10001; now += 10000) {
        assert(attempt(&result, now) == BRIDGE_DUPLICATE);
        assert(driver_attempts == 1);
    }
    if (button_output_faulted()) {
        int edges = rising_edges;
        result = button_output_press();
        assert(result.error == ESP_ERR_INVALID_STATE && !result.may_have_asserted && rising_edges == edges);
    }
    assert(depth == 0);
    printf("Output PASS: %s\n", scenario);
    return 0;
}
