#include "button_output.h"
#include "bridge_policy.h"
#include <stdatomic.h>
#include "driver/gpio.h"
#include "driver/gptimer.h"
#include "esp_attr.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/portmacro.h"

static gptimer_handle_t pulse_timer;
static atomic_bool active;
static atomic_bool faulted;
static portMUX_TYPE output_lock = portMUX_INITIALIZER_UNLOCKED;

/* Caller holds output_lock. A failed LOW write means the output is unknown,
 * not released. Any driver error inhibits further attempts until restart. */
static void IRAM_ATTR release_locked(void)
{
    esp_err_t low = gpio_set_level(BUTTON_GPIO, 0);
    /* Do not cancel a pending release alarm if the LOW write itself failed. */
    esp_err_t stopped = low == ESP_OK ? gptimer_stop(pulse_timer) : ESP_OK;
    if (low != ESP_OK || stopped != ESP_OK) atomic_store(&faulted, true);
    atomic_store(&active, low != ESP_OK);
}

static bool IRAM_ATTR release_alarm(gptimer_handle_t timer,
    const gptimer_alarm_event_data_t *event, void *context)
{
    (void)event;
    (void)context;
    /* No logging, HTTP, allocation or flash access in the release interrupt. */
    (void)timer;
    portENTER_CRITICAL_ISR(&output_lock);
    release_locked();
    portEXIT_CRITICAL_ISR(&output_lock);
    return false;
}

static void release_on_restart(void)
{
    portENTER_CRITICAL(&output_lock);
    atomic_store(&faulted, true); /* No assertion after shutdown has begun. */
    release_locked();
    portEXIT_CRITICAL(&output_lock);
}

void button_output_init(void)
{
    /* Set the output latch before enabling the pad's output driver. */
    ESP_ERROR_CHECK(gpio_set_level(BUTTON_GPIO, 0));
    gpio_config_t pin = {
        .pin_bit_mask = 1ULL << BUTTON_GPIO,
        .mode = GPIO_MODE_OUTPUT,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&pin));
    gptimer_config_t timer = {
        .clk_src = GPTIMER_CLK_SRC_DEFAULT,
        .direction = GPTIMER_COUNT_UP,
        .resolution_hz = 1000000,
    };
    ESP_ERROR_CHECK(gptimer_new_timer(&timer, &pulse_timer));
    gptimer_event_callbacks_t callbacks = {.on_alarm = release_alarm};
    ESP_ERROR_CHECK(gptimer_register_event_callbacks(pulse_timer, &callbacks, NULL));
    ESP_ERROR_CHECK(gptimer_enable(pulse_timer));
    ESP_ERROR_CHECK(esp_register_shutdown_handler(release_on_restart));
}

button_output_result_t button_output_press(void)
{
    button_output_result_t result = {.error = ESP_ERR_INVALID_STATE};
    portENTER_CRITICAL(&output_lock);
    if (atomic_load(&faulted) || atomic_load(&active)) {
        portEXIT_CRITICAL(&output_lock);
        return result;
    }
    atomic_store(&active, true); /* Reserve while preparing the stopped timer. */
    portEXIT_CRITICAL(&output_lock);
    gptimer_alarm_config_t alarm = {.alarm_count = BRIDGE_PULSE_MS * 1000ULL};
    result.error = gptimer_set_raw_count(pulse_timer, 0);
    if (result.error == ESP_OK) result.error = gptimer_set_alarm_action(pulse_timer, &alarm);

    /* Serialize start + HIGH with the release ISR. Merely moving start before
     * HIGH without this lock allows an alarm to release first, then a late
     * HIGH to hold the button indefinitely. No delay or allocation here. */
    portENTER_CRITICAL(&output_lock);
    if (result.error == ESP_OK && atomic_load(&faulted)) result.error = ESP_ERR_INVALID_STATE;
    if (result.error == ESP_OK) result.error = gptimer_start(pulse_timer);
    if (result.error == ESP_OK) {
        result.may_have_asserted = true;
        result.error = gpio_set_level(BUTTON_GPIO, 1);
    }
    if (result.error != ESP_OK) {
        atomic_store(&faulted, true);
        release_locked();
    }
    portEXIT_CRITICAL(&output_lock);
    return result;
}

bool button_output_active(void)
{
    return atomic_load(&active);
}

bridge_decision_t button_output_attempt(bridge_policy_t *policy, const char *boot_id,
    uint32_t sequence, uint64_t deadline_ms, uint64_t now_ms, button_output_result_t *result)
{
    bridge_decision_t decision = bridge_policy_reserve(policy, boot_id, sequence, deadline_ms, now_ms);
    if (decision == BRIDGE_ACCEPT) *result = button_output_press();
    return decision;
}

bool button_output_faulted(void)
{
    return atomic_load(&faulted);
}
