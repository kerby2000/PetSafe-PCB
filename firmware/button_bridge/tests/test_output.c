#include <assert.h>
#include <stdio.h>
#include "button_output.h"
#include "driver/gpio.h"
#include "driver/gptimer.h"

static int level = -1, rising_edges, calls;
static int fail_stage;
static bool running;
static bool (*alarm_callback)(gptimer_handle_t, const gptimer_alarm_event_data_t *, void *);
static void (*shutdown_callback)(void);

esp_err_t gpio_set_level(int pin, int value) {
    assert(pin == 3);
    if (value == 1 && level != 1) ++rising_edges;
    level = value; ++calls; return ESP_OK;
}
esp_err_t gpio_config(const gpio_config_t *config) {
    assert(calls == 1 && level == 0); /* LOW before enabling output. */
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
    (void)t; assert(count == 0); return fail_stage == 1 ? ESP_FAIL : ESP_OK;
}
esp_err_t gptimer_set_alarm_action(gptimer_handle_t t, const gptimer_alarm_config_t *c) {
    (void)t; assert(c->alarm_count == 200000); return fail_stage == 2 ? ESP_FAIL : ESP_OK;
}
esp_err_t gptimer_start(gptimer_handle_t t) {
    (void)t; if (fail_stage == 3) return ESP_FAIL; running = true; return ESP_OK;
}
esp_err_t gptimer_stop(gptimer_handle_t t) {(void)t; running = false; return ESP_OK;}

int main(void) {
    button_output_init();
    assert(level == 0 && rising_edges == 0 && !button_output_active());
    assert(button_output_press() == ESP_OK && level == 1 && running);
    assert(button_output_active() && rising_edges == 1);
    assert(button_output_press() == ESP_ERR_INVALID_STATE && rising_edges == 1);
    /* The actual release callback has no dependency on any HTTP loop. */
    assert(!alarm_callback((void *)1, NULL, NULL));
    assert(level == 0 && !running && !button_output_active());
    assert(button_output_press() == ESP_OK && rising_edges == 2);
    shutdown_callback();
    assert(level == 0);
    alarm_callback((void *)1, NULL, NULL);
    for (fail_stage = 1; fail_stage <= 3; ++fail_stage) {
        assert(button_output_press() == ESP_FAIL);
        assert(level == 0 && !running && !button_output_active());
    }
    puts("Output PASS: LOW before output enable, fixed alarm, no overlap, ISR/restart release, failure release");
    return 0;
}
