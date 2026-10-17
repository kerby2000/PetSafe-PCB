#include "button_output.h"
#include "bridge_policy.h"
#include <stdatomic.h>
#include "driver/gpio.h"
#include "driver/gptimer.h"
#include "esp_attr.h"
#include "esp_system.h"

static gptimer_handle_t pulse_timer;
static atomic_bool active;

static bool IRAM_ATTR release_alarm(gptimer_handle_t timer,
    const gptimer_alarm_event_data_t *event, void *context)
{
    (void)event;
    (void)context;
    /* No logging, HTTP, allocation or flash access in the release interrupt. */
    gpio_set_level(BUTTON_GPIO, 0);
    gptimer_stop(timer);
    atomic_store(&active, false);
    return false;
}

static void release_on_restart(void)
{
    gpio_set_level(BUTTON_GPIO, 0);
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
    ESP_ERROR_CHECK(esp_register_shutdown_handler(release_on_restart));
    gptimer_config_t timer = {
        .clk_src = GPTIMER_CLK_SRC_DEFAULT,
        .direction = GPTIMER_COUNT_UP,
        .resolution_hz = 1000000,
    };
    ESP_ERROR_CHECK(gptimer_new_timer(&timer, &pulse_timer));
    gptimer_event_callbacks_t callbacks = {.on_alarm = release_alarm};
    ESP_ERROR_CHECK(gptimer_register_event_callbacks(pulse_timer, &callbacks, NULL));
    ESP_ERROR_CHECK(gptimer_enable(pulse_timer));
}

esp_err_t button_output_press(void)
{
    bool expected = false;
    if (!atomic_compare_exchange_strong(&active, &expected, true))
        return ESP_ERR_INVALID_STATE;
    gptimer_alarm_config_t alarm = {.alarm_count = BRIDGE_PULSE_MS * 1000ULL};
    esp_err_t result = gptimer_set_raw_count(pulse_timer, 0);
    if (result == ESP_OK) result = gptimer_set_alarm_action(pulse_timer, &alarm);
    if (result == ESP_OK) result = gpio_set_level(BUTTON_GPIO, 1);
    if (result == ESP_OK) result = gptimer_start(pulse_timer);
    if (result != ESP_OK) {
        gpio_set_level(BUTTON_GPIO, 0);
        atomic_store(&active, false);
    }
    return result;
}

bool button_output_active(void)
{
    return atomic_load(&active);
}
