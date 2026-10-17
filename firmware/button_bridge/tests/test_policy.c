#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "bridge_policy.h"

int main(void)
{
    bridge_policy_t s;
    const char *boot = "0123456789abcdef0123456789abcdef";
    bridge_policy_init(&s, boot);
    assert(s.last_sequence == 0);
    assert(bridge_policy_reserve(&s, boot, 1, 0, 0) == BRIDGE_EXPIRED);
    assert(s.last_sequence == 0); /* Invalid requests cannot consume sequences. */
    assert(bridge_policy_check(&s, boot, 1, 5000, 0) == BRIDGE_ACCEPT);
    /* Checking/rejecting a request cannot change state or reserve an output pulse. */
    assert(s.last_sequence == 0);
    assert(bridge_policy_check(&s, "oldboot", 1, 5000, 0) == BRIDGE_WRONG_BOOT);
    assert(bridge_policy_check(&s, boot, 0, 5000, 0) == BRIDGE_BAD_SEQUENCE);
    assert(bridge_policy_check(&s, boot, 2, 5000, 0) == BRIDGE_BAD_SEQUENCE);
    assert(bridge_policy_check(&s, boot, 1, 100, 100) == BRIDGE_EXPIRED);
    assert(bridge_policy_check(&s, boot, 1, 10101, 100) == BRIDGE_EXPIRED);
    assert(bridge_policy_check(&s, boot, 1, 10099, 100) == BRIDGE_ACCEPT);
    assert(bridge_policy_reserve(&s, boot, 1, 5000, 100) == BRIDGE_ACCEPT);
    assert(s.last_sequence == 1 && s.available_at_ms == 5100);
    assert(bridge_policy_reserve(&s, boot, 1, 5000, 100) == BRIDGE_DUPLICATE);
    assert(bridge_policy_check(&s, boot, 1, 5000, 200) == BRIDGE_DUPLICATE);
    assert(bridge_policy_check(&s, boot, 1, 5000, 9000) == BRIDGE_DUPLICATE);
    assert(bridge_policy_check(&s, "oldboot", 1, 5000, 200) == BRIDGE_WRONG_BOOT);
    assert(bridge_policy_check(&s, boot, 2, 6000, 5099) == BRIDGE_COOLDOWN);
    assert(bridge_policy_check(&s, boot, 2, 6000, 5100) == BRIDGE_ACCEPT);
    bridge_policy_commit(&s, 2, 5100);
    assert(bridge_policy_check(&s, boot, 1, 20000, 11000) == BRIDGE_BAD_SEQUENCE);
    assert(bridge_policy_check(&s, boot, 2, 20000, 11000) == BRIDGE_DUPLICATE);
    assert(bridge_policy_check(&s, boot, 3, 20000, 11000) == BRIDGE_ACCEPT);
    s.last_sequence = UINT32_MAX;
    assert(bridge_policy_check(&s, boot, 0, 20000, 11000) == BRIDGE_BAD_SEQUENCE);

    uint64_t n = 99;
    assert(bridge_parse_uint("4294967295", UINT32_MAX, &n) && n == UINT32_MAX);
    assert(!bridge_parse_uint("4294967296", UINT32_MAX, &n));
    assert(bridge_parse_uint("18446744073709551615", UINT64_MAX, &n) && n == UINT64_MAX);
    assert(!bridge_parse_uint("18446744073709551616", UINT64_MAX, &n));
    assert(!bridge_parse_uint("-1", UINT32_MAX, &n));
    assert(!bridge_parse_uint("1.5", UINT32_MAX, &n));
    assert(!bridge_parse_uint("1x", UINT32_MAX, &n));
    assert(!bridge_parse_uint(" 1", UINT32_MAX, &n));
    assert(!bridge_parse_uint("", UINT32_MAX, &n));
    assert(!bridge_parse_uint("9", 5, &n));

    const char *token = "abcdefghijklmnopqrstuvwxyz0123456789";
    assert(bridge_authorized("Bearer abcdefghijklmnopqrstuvwxyz0123456789", token));
    assert(!bridge_authorized("Bearer abcdefghijklmnopqrstuvwxyz0123456780", token));
    assert(!bridge_authorized("bearer abcdefghijklmnopqrstuvwxyz0123456789", token));
    assert(!bridge_authorized("Bearer short", "short"));
    assert(!bridge_authorized("Bearer ", ""));
    assert(!bridge_authorized(NULL, token));
    puts("Policy PASS: boot/replay/sequence/expiry/cooldown/overflow/authentication");
    return 0;
}
