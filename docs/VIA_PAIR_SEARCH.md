# Targeted via-to-via search — current round

Basis: **v0.9.8**. The remaining search pool has **17 sites in 13 local endpoint groups**. These are not 13 proven missing nets. V067/U6A is now mapped to J3.1/PIR supply; no generic GPIO batch remains pending.

## Results applied

| Pair | Result | Consequence |
|---|---|---|
| V053–V070 | Connected | PIC12/RC1 → R18.1; user checked |
| V053–VREF | NOT connected | Withdraw old RC1/VREF photo assumption |
| V049–TP3 | Connected | PIC13/RC2 → TP3; local R10 branch remains photo-derived |
| V026–VREF | Connected | PIC21/RB0 → native TP104, labelled VREF |
| V067–J3.1 | Connected | Earlier U6A pad association joins H_PIR_VDD; DNP retained |
| V036–V108 | Working | PIC5/RA3 → R14 |
| V037–V102 | Working | PIC6/RA4 → R15 |
| V039–V097 | Working | PIC7/RA5 → R16 |
| V047–V091 | Working | PIC11/RC0 → R11 |
| V064–V063 | Working | R37/R39 feed joins regulated VDD |
| V064–V075 | Working | V075 joins regulated VDD; Q7/R19 local pad selection photo-derived |
| V064–V070 | 11.2 kΩ | Resistive path; direct R18 input-to-VDD assumption withdrawn |
| V049–V071 | 20 kΩ | Resistive path to the R21-associated node; not the pending V070/R18 test |
| V049–V070 | Variable 200–300 kΩ | No continuity demonstrated; contact-dependent, not a definitive open |
| V053–V071 | Not connected | Reject proposed V053/RC1-to-R21 direct link |
| V090–V095 | OL | No measured direct connection |
| V090–V100 | OL | No measured direct connection |
| V090–V103 | OL | No measured direct connection |
| V090–V107 | OL | No measured direct connection |
| V095–V100 | OL | No measured direct connection |
| V095–V103 | OL | No measured direct connection |
| V095–V107 | OL | No measured direct connection |

Positive pairs and the V053–V071 result were reported without numerical ohms. No numerical reading has been invented. All five tuning controls are now mapped, including the earlier RC6/R13 route. No PIC pads remain open in the model. RC1 now reaches R18, RC2 reaches TP3 and RB0 reaches VREF. Other already drawn local nets can still have unknown or inferred remote connections.

## Why those pairs were proposed

The successful GPIO tests had a specific functional basis: a repeated bank of transistor/resistor cells plausibly needs separate PIC control outputs. The supply tests compared a known rail with a plausible local feed. Neither geometry nor a typical application establishes a connection without evidence.

The capacitor tests were weaker: repeated neighboring cells suggested that their junctions *might* share hidden copper. A shared node needs only one fixed-probe sweep to detect, rather than all possible pair combinations. V090 gave OL to all four others. The second sweep used V095 to test whether the remaining four shared a different node. That was a hypothesis based on repeated structure, not an observed trace or a datasheet requirement.

**Seven OL results now weaken that common-node hypothesis enough to stop broad capacitor-pair testing.** The three remaining mutual comparisons (V100–V103, V100–V107, V103–V107) are untested, not inferred negative. An OL resistance result excludes a measured direct DC path in this test; it does not exclude a signal path through capacitors. Any later test must follow a visible local route or a specific circuit endpoint.

## What the 11.2 kΩ reading changes

R18 is marked 122 (1.2 kΩ) and R19 is marked 01C (10 kΩ). Their nominal sum is **11.2 kΩ**, matching the reported in-circuit reading. The measured path is not direct copper. Combined with IMG_2434 and the earlier V064–V075 supply confirmation, it supports this local reconstruction:

`V070 → R18 (1.2k) → Q7 base / R19 (10k) → V075 / regulated VDD`

Q7's emitter joins VDD; R19 is a base-emitter pull-up, and the collector feeds the receiver supply through R20. This is a **photo/resistance-supported circuit inference**, not proof from resistance alone. The Q7 candidate remains BC857C; the official Nexperia datasheet supplies the candidate pin roles (1=B, 2=E, 3=C), not the board wiring. No reverse-probe reading or isolated resistor measurement was supplied.

Native v0.9.7 removes the old direct R18.1-to-VDD assumption, moves R18.2 to the base junction, and places Q7.R/R19.2 on VDD. No GPIO source is invented. Validation checks 86 model/native partitions; 42 ERC findings remain (33 open pads, four isolated labels, five power findings).

The additional **V049–V071 = 20 kΩ** report is recorded independently. V071 reaches R21; V070 reaches R18. This reading excludes a direct RC2-to-V071 link but does not identify the resistance path through the unpowered receiver circuit. It is independent of D1, and no specific series-resistor path is claimed from 20 kΩ alone.

## Completed GPIO follow-up

V049–V070 returned variable 200–300 kΩ with probe placement. This remains inconclusive/contact-dependent, not OL or a recovered resistor value. The proposed D2 V070–V026 check was never measured and was withdrawn when the user identified RB0/VREF. It must not be recorded as rejected.

The user then explicitly excluded V053 from VREF and confirmed **V053–V070**. Thus RC1/PIC12 reaches R18.1 while RB0/PIC21 reaches VREF/TP104. The former RC1–VREF photo interpretation is withdrawn. RC2/PIC13 reaches TP3; its prior local R10.1 branch remains photo-derived. V067 reaches J3 pin 1/red wire, mapped to H_PIR_VDD; this preserves the previous local U6A.R1 pad association without identifying the unpopulated device.

The [photo locator](VIA_PAIR_TESTS.html) and [printable guide](../output/pdf/PetSafe_via_pair_next_check.pdf) now show the completed V053–V070 route. No repeat reading is requested. Earlier browser storage and round-2/3/4/5 evidence are preserved. New reports are in `v098_net_changes.json` and `via_user_review.json`.

Validation: **85 native/model net partitions PASS; 37 ERC findings = 29 open pads + 3 isolated labels + 5 power findings**. The 29 open pads comprise 11 populated-entry and 18 empty-option pads. Local modeled connections can still have missing remote continuations or inferred branches.

## Remaining decisions

- Q1.L / V011–V014 is user-reported VDD, but regulated V064 versus motor-supply V001 remains unanswered. The two rails remain separate. Q1.L remains separate from explicitly excluded R43.2/V015.
- V114 is resolved as U2.T2/pin2 GND and removed from the candidate pool. It is not Q8.T2.
- B3 is complete at 11.2 kΩ. Do not repeat it or start a blind rail sweep. V064–V063 and V064–V075 remain confirmed.
- For V071/R21, V053 is rejected. V031/RA0 and V035/RA2 are alternative reference/filter candidates, not confirmed connections.
- The formerly open GPIO list is complete. Prioritize remote continuations of already-local nodes, receiver/PIR/button interfaces, Q7 identity/function qualifications and the D3 terminal at V082. V067/U6A is now mapped to J3.1.

The [complete via-group inventory and hypotheses](../evidence/via_pair_plan.json) retains each local endpoint association separately. No proposed next pair has been added as a schematic connection.

Latest v0.9.8 report: **V015-TP14 confirmed**, joining R43.2 to TP14. Q1.L remains excluded. Existing TP14-Q1.S branch and H_BAT_DETECT functional name remain hypotheses; no numeric resistance supplied.

Latest v0.9.8 report: **V017-TP4 confirmed**, joining R42.1/R44.1 to TP4 and PIC25/RB4. Existing C41 branch and R44 pad selection retain their photo-derived basis. No numeric resistance supplied.
