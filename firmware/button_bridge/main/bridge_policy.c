#include "bridge_policy.h"
#include <stddef.h>
#include <string.h>

void bridge_policy_init(bridge_policy_t *s, const char *boot_id)
{
    memset(s, 0, sizeof(*s));
    memcpy(s->boot_id, boot_id, BRIDGE_BOOT_ID_LEN);
}

bridge_decision_t bridge_policy_check(const bridge_policy_t *s,
    const char *boot_id, uint32_t sequence, uint64_t deadline, uint64_t now)
{
    if (strcmp(s->boot_id, boot_id) != 0) return BRIDGE_WRONG_BOOT;
    if (sequence == 0) return BRIDGE_BAD_SEQUENCE;
    /* Retries never produce another pulse, even after their deadline/cooldown. */
    if (sequence == s->last_sequence) return BRIDGE_DUPLICATE;
    if (s->last_sequence == UINT32_MAX || sequence != s->last_sequence + 1)
        return BRIDGE_BAD_SEQUENCE;
    if (deadline <= now || deadline - now > BRIDGE_MAX_COMMAND_AGE_MS)
        return BRIDGE_EXPIRED;
    if (now < s->available_at_ms) return BRIDGE_COOLDOWN;
    return BRIDGE_ACCEPT;
}

void bridge_policy_commit(bridge_policy_t *s, uint32_t sequence, uint64_t now)
{
    s->last_sequence = sequence;
    s->available_at_ms = now + BRIDGE_COOLDOWN_MS;
}

bridge_decision_t bridge_policy_reserve(bridge_policy_t *s,
    const char *boot_id, uint32_t sequence, uint64_t deadline, uint64_t now)
{
    bridge_decision_t decision = bridge_policy_check(s, boot_id, sequence, deadline, now);
    if (decision == BRIDGE_ACCEPT) bridge_policy_commit(s, sequence, now);
    return decision;
}

bool bridge_parse_uint(const char *text, uint64_t limit, uint64_t *result)
{
    if (!text || !*text) return false;
    uint64_t value = 0;
    for (const unsigned char *p = (const unsigned char *)text; *p; ++p) {
        if (*p < '0' || *p > '9') return false;
        unsigned digit = *p - '0';
        if (digit > limit || value > (limit - digit) / 10) return false;
        value = value * 10 + digit;
    }
    *result = value;
    return true;
}

bool bridge_authorized(const char *header, const char *token)
{
    if (!header || !token) return false;
    size_t length = strlen(token);
    if (length < 32 || length > 128 || strlen(header) != length + 7) return false;
    unsigned diff = 0;
    const char prefix[] = "Bearer ";
    for (size_t i = 0; i < 7; ++i) diff |= (unsigned char)header[i] ^ prefix[i];
    for (size_t i = 0; i < length; ++i)
        diff |= (unsigned char)header[i + 7] ^ (unsigned char)token[i];
    return diff == 0;
}
