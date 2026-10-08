# Targeted via-to-via search — current round

Basis: **v0.9.6**. The search pool is now **23 non-rail sites in 19 local endpoint groups**, including one empty U6A option. These are not 20 proven missing nets; some local groups may need no additional connection.

## Results applied

| Pair | Result | Consequence |
|---|---|---|
| V036–V108 | Working | PIC5/RA3 → R14 |
| V037–V102 | Working | PIC6/RA4 → R15 |
| V039–V097 | Working | PIC7/RA5 → R16 |
| V047–V091 | Working | PIC11/RC0 → R11 |
| V064–V063 | Working | R37/R39 feed joins regulated VDD |
| V064–V075 | Working | V075 joins regulated VDD; exact Q7 terminal still a photo candidate |
| V053–V071 | Not connected | Reject proposed VREF/R21 direct link |
| V090–V095 | OL | No measured direct connection |
| V090–V100 | OL | No measured direct connection |
| V090–V103 | OL | No measured direct connection |
| V090–V107 | OL | No measured direct connection |
| V095–V100 | OL | No measured direct connection |
| V095–V103 | OL | No measured direct connection |
| V095–V107 | OL | No measured direct connection |

Positive pairs and the V053–V071 result were reported without numerical ohms. No numerical reading has been invented. All five tuning controls are now mapped, including the earlier RC6/R13 route. Only PIC13/RC2 at V049 and PIC21/RB0 at V026 remain open among the previously unmapped GPIOs. Other already drawn local nets can still have unknown or inferred remote connections.

## Why those pairs were proposed

The successful GPIO tests had a specific functional basis: a repeated bank of transistor/resistor cells plausibly needs separate PIC control outputs. The supply tests compared a known rail with a plausible local feed. Neither geometry nor a typical application establishes a connection without evidence.

The capacitor tests were weaker: repeated neighboring cells suggested that their junctions *might* share hidden copper. A shared node needs only one fixed-probe sweep to detect, rather than all possible pair combinations. V090 gave OL to all four others. The second sweep used V095 to test whether the remaining four shared a different node. That was a hypothesis based on repeated structure, not an observed trace or a datasheet requirement.

**Seven OL results now weaken that common-node hypothesis enough to stop broad capacitor-pair testing.** The three remaining mutual comparisons (V100–V103, V100–V107, V103–V107) are untested, not inferred negative. An OL resistance result excludes a measured direct DC path in this test; it does not exclude a signal path through capacitors. Any later test must follow a visible local route or a specific circuit endpoint.

## One remaining diagnostic check

| Test | Fixed probe | Moving probe | Purpose |
|---|---|---|---|
| B3 | V064 | V070 | Test the older R18-to-VDD assumption |

**V075 and V070 are different sites.** The new positive result puts V075 on regulated VDD. IMG_2434 suggests its continuation to Q7.R/R19.2; the user has not specified a Q7 terminal. This makes a supply-switch interpretation worth reviewing, with R18 potentially carrying a control signal. B3 checks the older assumption that R18's free end is on VDD. It is a diagnostic check, not a predicted hit. A direct result supports that rail assignment; OL redirects investigation toward the local Q7 pad and a possible control endpoint. Neither result alone proves Q7 pin functions.

Use the [paired photo locator](VIA_PAIR_TESTS.html) or [one-page marked guide](../output/pdf/PetSafe_via_pair_next_check.pdf). Refresh the page to remove completed tests. Its existing browser-storage key is preserved, including any B3 entry; completed entries remain in storage but are not requested again. The [current CSV](../evidence/via_pair_readings.csv) contains only B3. The previous four-test plan and reported C5–C7 readings are archived in `evidence/via_pair_round2_plan.json` and `evidence/via_pair_round2_readings.csv`.

Disconnect battery and programmer. Use resistance mode; report actual ohms, OL or a changing reading. Compare low readings with good probe contact and reverse probes to check. A beep alone can include a resistor or semiconductor path. Very low resistance can include an inductor or zero-ohm link. Continuity recovers electrical connectivity, not exact inner-layer geometry or layer count.

This follow-up updates the via graph and the test queue. Native schematic wiring and its validation remain **v0.9.6**; no Q7 terminal has been merged solely from an ambiguous component-level association. The old native R18/Q7 arrangement remains a hypothesis pending the targeted check.

## Remaining decisions

- Q1.L / V011–V014 is user-reported VDD, but regulated V064 versus motor-supply V001 remains unanswered. The two rails remain separate. Q1.L remains separate from explicitly excluded R43.2/V015.
- V114 is resolved as U2.T2/pin2 GND and removed from the candidate pool. It is not Q8.T2.
- If B3 is negative, review R18 as a control input before choosing a GPIO endpoint. Do not replace the capacitor sweep with a blind rail sweep. V064–V063 and V064–V075 are already confirmed.
- For V071/R21, V053 is rejected. V031/RA0 and V035/RA2 are alternative reference/filter candidates, not confirmed connections.
- Prioritize the two remaining GPIO routes, receiver/PIR/button interfaces, the exact Q7 terminal at the now-known V075 supply via and D3 terminal at V082 after the immediate checks. Empty U6A/V067 is lower priority.

The [complete via-group inventory and hypotheses](../evidence/via_pair_plan.json) retains each local endpoint association separately. No proposed next pair has been added as a schematic connection.
