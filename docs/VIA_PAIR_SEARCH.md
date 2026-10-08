# Targeted via-to-via search — current round

Basis: **v0.9.7**. The search pool is now **23 non-rail sites in 19 local endpoint groups**, including one empty U6A option. These are not 19 proven missing nets; some local groups may need no additional connection.

## Results applied

| Pair | Result | Consequence |
|---|---|---|
| V036–V108 | Working | PIC5/RA3 → R14 |
| V037–V102 | Working | PIC6/RA4 → R15 |
| V039–V097 | Working | PIC7/RA5 → R16 |
| V047–V091 | Working | PIC11/RC0 → R11 |
| V064–V063 | Working | R37/R39 feed joins regulated VDD |
| V064–V075 | Working | V075 joins regulated VDD; Q7/R19 local pad selection photo-derived |
| V064–V070 | 11.2 kΩ | Resistive path; direct R18 input-to-VDD assumption withdrawn |
| V049–V071 | 20 kΩ | Resistive path to the R21-associated node; not the pending V070/R18 test |
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

## What the 11.2 kΩ reading changes

R18 is marked 122 (1.2 kΩ) and R19 is marked 01C (10 kΩ). Their nominal sum is **11.2 kΩ**, matching the reported in-circuit reading. The measured path is not direct copper. Combined with IMG_2434 and the earlier V064–V075 supply confirmation, it supports this local reconstruction:

`V070 → R18 (1.2k) → Q7 base / R19 (10k) → V075 / regulated VDD`

Q7's emitter joins VDD; R19 is a base-emitter pull-up, and the collector feeds the receiver supply through R20. This is a **photo/resistance-supported circuit inference**, not proof from resistance alone. The Q7 candidate remains BC857C; the official Nexperia datasheet supplies the candidate pin roles (1=B, 2=E, 3=C), not the board wiring. No reverse-probe reading or isolated resistor measurement was supplied.

Native v0.9.7 removes the old direct R18.1-to-VDD assumption, moves R18.2 to the base junction, and places Q7.R/R19.2 on VDD. No GPIO source is invented. Validation checks 86 model/native partitions; 42 ERC findings remain (33 open pads, four isolated labels, five power findings).

The additional **V049–V071 = 20 kΩ** report is recorded independently. V071 reaches R21; V070 reaches R18. This reading excludes a direct RC2-to-V071 link but does not identify the resistance path through the unpowered receiver circuit. It does not answer D1 below, and no specific series-resistor path is claimed from 20 kΩ alone.

## Next: one control candidate

| Test | Fixed probe | Moving probe | Purpose |
|---|---|---|---|
| D1 | V070 | V049 | Does PIC13/RC2 drive the R18 input? |

RC2 is one of two PIC GPIOs whose onward destination remains unknown. The proposed receiver-enable function makes it a useful candidate, but no buried trace or datasheet establishes this particular GPIO choice. If not direct, the next alternative is V070–V026 (PIC21/RB0). Other already-local PIC nets may also have unknown continuations; neither pin is assigned by elimination.

Use the [paired photo locator](VIA_PAIR_TESTS.html) or [marked guide](../output/pdf/PetSafe_via_pair_next_check.pdf). Refresh the page; it now requests D1 only. Browser-storage entries are preserved under the existing key. The [current CSV](../evidence/via_pair_readings.csv) contains D1. The completed B3 plan and 11.2 kΩ reading are archived as `evidence/via_pair_round3_plan.json` and `evidence/via_pair_round3_readings.csv`; the earlier capacitor results remain in the round-2 archive and the user-review log.

Disconnect battery and programmer. Use resistance mode; report actual ohms, OL or a changing reading. Compare low readings with good probe contact and reverse probes to check. A beep alone can include a resistor or semiconductor path. Very low resistance can include an inductor or zero-ohm link. Continuity recovers electrical connectivity, not exact inner-layer geometry or layer count.

## Remaining decisions

- Q1.L / V011–V014 is user-reported VDD, but regulated V064 versus motor-supply V001 remains unanswered. The two rails remain separate. Q1.L remains separate from explicitly excluded R43.2/V015.
- V114 is resolved as U2.T2/pin2 GND and removed from the candidate pool. It is not Q8.T2.
- B3 is complete at 11.2 kΩ. Do not repeat it or start a blind rail sweep. V064–V063 and V064–V075 remain confirmed.
- For V071/R21, V053 is rejected. V031/RA0 and V035/RA2 are alternative reference/filter candidates, not confirmed connections.
- Prioritize the two remaining GPIO routes, receiver/PIR/button interfaces, the remaining Q7 identity/function qualifications and D3 terminal at V082 after the immediate checks. Empty U6A/V067 is lower priority.

The [complete via-group inventory and hypotheses](../evidence/via_pair_plan.json) retains each local endpoint association separately. No proposed next pair has been added as a schematic connection.
