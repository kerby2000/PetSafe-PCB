#pragma once
#include <stdint.h>
#include "esp_err.h"
enum {GPIO_MODE_OUTPUT, GPIO_PULLDOWN_ENABLE, GPIO_PULLUP_DISABLE, GPIO_INTR_DISABLE};
typedef struct {uint64_t pin_bit_mask; int mode, pull_down_en, pull_up_en, intr_type;} gpio_config_t;
esp_err_t gpio_set_level(int pin, int value);
esp_err_t gpio_config(const gpio_config_t *config);
