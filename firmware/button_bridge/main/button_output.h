#pragma once
#include <stdbool.h>
#include "esp_err.h"
#include "bridge_policy.h"

#define BUTTON_GPIO 3
void button_output_init(void);
typedef struct {
    esp_err_t error;
    /* True as soon as a HIGH write is attempted, even if that write fails. */
    bool may_have_asserted;
} button_output_result_t;
button_output_result_t button_output_press(void);
/* The HTTP handler uses this transaction: reserve, then attempt, never roll back. */
bridge_decision_t button_output_attempt(bridge_policy_t *policy, const char *boot_id,
    uint32_t sequence, uint64_t deadline_ms, uint64_t now_ms, button_output_result_t *result);
bool button_output_active(void);
bool button_output_faulted(void);
