#pragma once
#include <stdbool.h>
#include "esp_err.h"

#define BUTTON_GPIO 3
void button_output_init(void);
esp_err_t button_output_press(void);
bool button_output_active(void);
