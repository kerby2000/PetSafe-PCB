# Targeted via-to-via search — current round

Basis: **v0.9.6**. The search pool is now **24 non-rail sites in 20 local endpoint groups**, including one empty U6A option. These are not 20 proven missing nets; some local groups may need no additional connection.

## Results applied

| Pair | Result | Consequence |
|---|---|---|
| V036–V108 | Working | PIC5/RA3 → R14 |
| V037–V102 | Working | PIC6/RA4 → R15 |
| V039–V097 | Working | PIC7/RA5 → R16 |
| V047–V091 | Working | PIC11/RC0 → R11 |
| V064–V063 | Working | R37/R39 feed joins regulated VDD |
| V053–V071 | Not connected | Reject proposed VREF/R21 direct link |
| V090–V095 | OL | No measured direct connection |
| V090–V100 | OL | No measured direct connection |
| V090–V103 | OL | No measured direct connection |
| V090–V107 | OL | No measured direct connection |

Positive pairs and the V053–V071 result were reported without numerical ohms. No numerical reading has been invented. All five tuning controls are now mapped, including the earlier RC6/R13 route. Only PIC13/RC2 at V049 and PIC21/RB0 at V026 remain open among the previously unmapped GPIOs. Other already drawn local nets can still have unknown or inferred remote connections.

## Four next checks

| Test | Fixed probe | Moving probe | Purpose |
|---|---|---|---|
| B3 | V064 | V070 | Is the R18 receiver feed also on regulated VDD? |
| C5 | V095 | V100 | Compare the remaining capacitor junctions |
| C6 | V095 | V103 | Same anchor |
| C7 | V095 | V107 | Same anchor |

Use the [paired photo locator](VIA_PAIR_TESTS.html) or [one-page marked guide](../output/pdf/PetSafe_via_pair_round2.pdf). The page prepares a reply for copying; it does not submit readings automatically. Refresh it to remove completed tests. The [current CSV](../evidence/via_pair_readings.csv) records only the next checks. Earlier proposals and readings are retained in `evidence/via_pair_round1_plan.json` and `evidence/via_pair_round1_readings.csv`.

Disconnect battery and programmer. Use resistance mode; report actual ohms, OL or a changing reading. Compare low readings with good probe contact and reverse probes to check. A beep alone can include a resistor or semiconductor path. Very low resistance can include an inductor or zero-ohm link. Continuity recovers electrical connectivity, not exact inner-layer geometry or layer count.

The four OL results exclude direct V090 connections to the tested junctions. They do **not** prove the remaining four are mutually isolated. C5–C7 check that smaller group using one fixed probe. The shared-node hypothesis is now weaker. If these are all OL too, stop broad pairwise testing and trace toward antenna/component endpoints; first verify contact against a known local capacitor junction before drawing conclusions from repeated OL.

## Remaining decisions

- Q1.L / V011–V014 is user-reported VDD, but regulated V064 versus motor-supply V001 remains unanswered. The two rails remain separate. Q1.L remains separate from explicitly excluded R43.2/V015.
- V114 is resolved as U2.T2/pin2 GND and removed from the candidate pool. It is not Q8.T2.
- If B3 is negative, choose a motor-supply or switched-feed comparison next. V064–V063 is already confirmed and will not be repeated.
- For V071/R21, V053 is rejected. V031/RA0 and V035/RA2 are alternative reference/filter candidates, not confirmed connections.
- Prioritize the two remaining GPIO routes, receiver/PIR/button interfaces, Q7 terminal at V075 and D3 terminal at V082 after the immediate checks. Empty U6A/V067 is lower priority.

The [complete via-group inventory and hypotheses](../evidence/via_pair_plan.json) retains each local endpoint association separately. No proposed next pair has been added as a schematic connection.
