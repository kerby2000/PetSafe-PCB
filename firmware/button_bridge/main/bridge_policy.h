#pragma once
#include <stdbool.h>
#include <stdint.h>

#define BRIDGE_PULSE_MS 200u
#define BRIDGE_COOLDOWN_MS 5000u
#define BRIDGE_MAX_COMMAND_AGE_MS 10000u
#define BRIDGE_BOOT_ID_LEN 32u

typedef struct {
    char boot_id[BRIDGE_BOOT_ID_LEN + 1];
    uint32_t last_sequence;
    uint64_t available_at_ms;
} bridge_policy_t;

typedef enum {
    BRIDGE_ACCEPT,
    BRIDGE_DUPLICATE,
    BRIDGE_WRONG_BOOT,
    BRIDGE_BAD_SEQUENCE,
    BRIDGE_EXPIRED,
    BRIDGE_COOLDOWN
} bridge_decision_t;

void bridge_policy_init(bridge_policy_t *state, const char *boot_id);
bridge_decision_t bridge_policy_check(const bridge_policy_t *state,
    const char *boot_id, uint32_t sequence, uint64_t deadline_ms, uint64_t now_ms);
/* Reserve before any output operation, including an attempt that may fail.
 * HTTP task owns state. A consumed sequence must never become reusable. */
bridge_decision_t bridge_policy_reserve(bridge_policy_t *state,
    const char *boot_id, uint32_t sequence, uint64_t deadline_ms, uint64_t now_ms);
void bridge_policy_commit(bridge_policy_t *state, uint32_t sequence, uint64_t now_ms);
bool bridge_parse_uint(const char *text, uint64_t limit, uint64_t *result);
bool bridge_authorized(const char *header, const char *token);
