# Via review findings - v0.9.7

## Current v0.9.7: resistive path and Q7 reconstruction

**V064–V070 = 11.2 kΩ**, with no reverse reading supplied. This rejects the direct R18 input-to-VDD assumption. It matches the nominal **1.2k R18 + 10k R19** series path. Together with IMG_2434 and the confirmed V064–V075 supply link, it supports a PNP supply-switch reconstruction: Q7.R/native2 emitter at VDD; Q7.L/native1 base joined to R18.2 and R19.1; R19.2 pulled to VDD; R18.1/V070 remains an unknown control source. Q7.S/native3 retains its collector path through R20.

**Additional reading: V049–V071 = 20 kΩ.** Recorded as a resistive path, not a direct RC2/R21 tie. V071 differs from V070; the pending V070–V049 check is still unmeasured. No path through specific resistors is inferred from this reading alone.

Those local pad assignments are explicitly **photo/circuit inferences supported by the resistance**, not new user-probed terminal confirmations. Candidate BC857C identity and operating function remain qualified. No MCU connection is guessed into the schematic. Next unmeasured candidate: V070–V049 (PIC13/RC2); then V026/RB0 only if needed.

KiCad 10.0.5 native/model validation: **86 partitions PASS; 42 ERC findings (33 open pads, four isolated labels, five power findings)**. All 26 original photo checksums remain intact. See [search reasoning and current test](VIA_PAIR_SEARCH.md).

## Historical continuity follow-up before v0.9.7

**V064–V075 is user-confirmed**, placing V075 on regulated VDD. No numerical resistance was supplied. V075 was previously associated with Q7, without a terminal; Q7.R/R19.2 remain photo candidates from IMG_2434. No terminal-level native merge is made from that component-only association. V064–V070/R18 is a different, unreported test.

**V095–V100, V095–V103 and V095–V107 all measured OL.** Together with the earlier V090 sweep there are seven excluded capacitor pairs. Stop the broad shared-node search; the three untested mutual pairs remain unknown. The [updated reasoning and single next check](VIA_PAIR_SEARCH.md) explain the changed search direction. Via graph now includes the V063/V064/V075 supply group and symmetric negative-pair records.

## Prior v0.9.6 results, retained

Four tuning-control pairs are confirmed: **V036–V108 = RA3–R14**, **V037–V102 = RA4–R15**, **V039–V097 = RA5–R16**, **V047–V091 = RC0–R11**. With the earlier RC6–R13 route, all five controls are mapped. Only RC2/pin13 and RB0/pin21 remain open GPIOs.

**V064–V063** confirms that the R37/R39 feed junction is regulated board VDD. The former separate `AUX_FEED_V063` hypothesis is merged into that rail. Motor VDD remains separate.

**V053–V071 is rejected. V090–V095/V100/V103/V107 all measured OL.** No corresponding direct connection is introduced. The remaining capacitor junctions could still form other groups; their mutual relationships remain unmeasured.

KiCad 10.0.5 validates 87 modeled net partitions. ERC: **42 findings = 33 open pins + 4 isolated labels + 5 power-drive findings**. Open pads comprise 14 populated-entry and 19 empty-option pads. All original photograph checksums pass. Q1's user-reported VDD still needs its rail distinguished.

See the [current targeted plan](VIA_PAIR_SEARCH.md) and [paired photo locator](VIA_PAIR_TESTS.html).

## Prior v0.9.5 state — current results above supersede its counts

### v0.9.5 corrections

| Via | Current association | Schematic effect |
|---|---|---|
| V114 | U2.T2 / native pin 2, GND; explicitly not Q8.T2 | Confirms existing U2 ground; resolves the old via conflict without grounding Q8 supply |
| V125, V126 | C5 negative terminal / pad 2, GND | Confirms existing capacitor ground |
| V127 | GND and LED1 | Ground the photo-selected common pair BL/BR / stock pins 3/4; internal LED mapping remains provisional |
| V011–V014 | Q1.L, user-reported VDD | Report recorded; distinguish regulated V064 from motor-supply V001 before assigning a rail |

The LED pair selection uses IMG_2432: the joined pair lies opposite the two resistor-fed terminals. The user's report establishes GND/component association; selecting the physical pair is a photo inference. Q1.L remains separate from R43.2/V015, as explicitly requested earlier. V114 supplies no evidence for the Q8 source rail, whose existing connection remains a hypothesis.

KiCad 10.0.5 validates 88 modeled net partitions. ERC has 50 findings: 37 open pins, eight isolated labels and five power-drive findings. The former LED input-drive finding is resolved by its ground connection. There are still six GPIOs with unknown onward destinations. All 26 original photo checksums pass.

The [targeted via-pair plan](VIA_PAIR_SEARCH.md) now has 29 local candidate groups / 33 non-rail sites, including the unresolved Q1 rail choice and one empty U6A option. Eleven proposed first-round readings remain unmeasured. [Paired photo locator](VIA_PAIR_TESTS.html).

## Historical v0.9.4 state — superseded where corrected above

120 distinct via IDs reviewed; 120 active sites / 127 stable IDs. PIC15/RC4 connects through V022-V016 to MX512H INA pin2; PIC16/RC5 connects through V023-V019 to INB pin3. Six GPIO onward destinations remain unknown. V011-V014 reach Q1.L. The user explicitly removes the old Q1.L-R43.2 photo-derived connection; R43.2 still reaches V015. Seven IDs remain unmentioned, some already photo-matched. V114 net remains the only held via conflict.

## v0.9.4 motor and Q1 corrections

| Sites | Confirmed connection | Native change |
|---|---|---|
| V016 - V022 | U5.2 INA - U4.15 RC4 | MOTOR_INA now driven by PIC |
| V019 - V023 | U5.3 INB - U4.16 RC5 | MOTOR_INB now driven by PIC |
| V011-V014 | Q1.L, explicitly not R43.2 | Withdraw old Q1.L-R43.2 link |
| V015 | R43.2 | Withdraw inferred Q1.L association |

The user explicitly answered “Remove Q1.L–R43.2 connection”. Historical fragment V_Q1_LEFT is preserved as rejected evidence, with the other 28 original fragments retained electrically. Q1.L and R43.2 now each have a known local via but unknown onward destination. This adds two open component pads while resolving two PIC pads: 37 open pads remain, of which six are PIC GPIOs.

## Prior v0.9.3 corrections

| Via | User-confirmed local destination | Remaining uncertainty |
|---|---|---|
| V036 | U4 pin5 / RA3 | Onward destination unknown |
| V037 | U4 pin6 / RA4 | Onward destination unknown |
| V039 | U4 pin7 / RA5 | Onward destination unknown |
| V047 | U4 pin11 / RC0 | Onward destination unknown |
| V049 | U4 pin13 / RC2 | Onward destination unknown |
| V072 | TP6.1; explicitly not R22.2 | Other RX_A_FILTER branches remain inferred |
| V079, V080 | SGM8542 U3 pin5 | Other receiver topology remains partly inferred |

These are local endpoint confirmations; no new component-to-component net merges. All eight unresolved GPIO onward routes now have identified local vias. TP6 and U3.5 remain separate across C18. Seven previously unmentioned IDs are now reviewed, leaving nine.

## Prior v0.9.2 corrections

| Via | Updated destination | Qualification |
|---|---|---|
| V075 | Q7 | Terminal not specified; Q7.R and former R19.2 association are photo candidates only |
| V077 | C19.2 / R29.2 / GND | User explicitly confirms junction GND; R29 opposite PIC3 end, C19 upper photo pad selected |
| V078 | C17.2 / GND | Component added to earlier GND report |
| V083 | C40.2 / GND | Component added to earlier GND report |
| V091 | R11.1 / H_TUNE_5 | Free upper pad photo-selected; onward GPIO unknown |
| V097 | R16.1 / H_TUNE_4 | Free upper pad photo-selected; onward GPIO unknown |
| V102 | R15.1 / H_TUNE_3 | Free upper pad photo-selected; onward GPIO unknown |
| V108 | R14.1 / H_TUNE_2 | Free upper pad photo-selected; onward GPIO unknown |
| V112 | C8.2 / GND | Component added to earlier GND report |
| V113, V115 | Q8.B2 / pin5 / GND | Centre-pad clarification replaces incorrect outer B1/B3 annotations |
| V114 | Q8.T2 / pin2; net unresolved | Follow-up confirms opposite-side second pin; GND versus supply not answered |
| V118 | C7.2 / GND | Component added to earlier GND report |
| V119 | C9.2; GND photo/model inference | User identifies component only |
| V117, V120, V121, V122, V124 | Rejected; not vias | Stable IDs retained; excluded from active markers |

Two native pad assignments change: C19.2 and R29.2 become GND. R29.1 stays on PIC3/TP7/R28, and the independent U3.5/C18.1 fragment remains. Q8 centre pin5 was already grounded in the schematic; its via annotations are corrected without grounding the outer drains or opposite source. V114 is the only held site conflict.

## Prior v0.9.1 corrections

| Via | Current association | Evidence qualification |
|---|---|---|
| V006 | C33.2 / GND | User C33; earlier GND report; pad photo-selected |
| V007 | C34.2 / GND | User C34; earlier GND report; pad photo-selected |
| V011-V014 | Not R43.2; destination unresolved | Incorrect Q1.L/R43.2 island association removed |
| V015 | R43.2; local Q1.L fragment retained | User lower pad2; Q1 connection from original visual fragment |
| V017 | R42.1 / R44.1 / V017_CONTROL | User explicitly R42.1 and R44; free R44 pad1 photo-selected; old R42-to-ANT2 guess withdrawn |
| V018 | C35.2 / GND | User C35; earlier GND report; pad photo-selected |
| V020 | R40.1 / ICSP_DAT | User R40; free pad1 photo-selected; existing local ICSP node |
| V029 | C25.2 / C26.2 / GND | User capacitor pair; earlier GND report; return pads photo-selected |
| V033 | Rejected, not a via | User recognition correction; ID preserved |
| V034 | R3.1 / H_VBAT | User VDD/R3; previous explicit common net with V001/MX512H pin4 |
| V040 | C28.2 / GND | User C28; earlier GND report; pad photo-selected |
| V059, V061 | L2.1 / H_VBAT | User L2; earlier motor supply report; source/right pad photo-selected |
| V060 | Q2.L / GND | User Q2; earlier GND report; local pad photo-selected |
| V065 | C2.2 / GND | User C2; earlier GND report; return pad photo-selected |
| V068 | C37.2 / C36.2 / GND | User pair; earlier GND report; return pads photo-selected |
| V072 | Not R22.2; superseded by v0.9.3 TP6 assignment | Prior independent receiver-bias hypothesis still unverified |
| V073 | GND only | User explicitly resolves duplicate; no R19 ground merge |

Only two component-pad net assignments change in this batch: R42.1 and R44.1 join `V017_CONTROL`. The other entries correct via metadata or corroborate existing qualified pad assignments. The original `V_Q1_LEFT` fragment (Q1.L to R43.2) remains; the user corrected the via location, not this independent local trace. Superseded in v0.9.2: V075 now identifies Q7; exact terminal and possible R19 continuation remain photo candidates.

## Prior v0.9 endpoint corrections retained

| Pad | Earlier net | Current net | Basis |
|---|---|---|---|
| C27.1 | Open | H_VBAT | C27 photo left pad to V003/V004; user ties these to MX512H pin4 motor VDD. |
| C27.2 | Open | H_GND | C27 photo right pad to V008/V009/V010 user GND. |
| R1.1 | Open | H_VDD | DNP free pads via V064 to board VDD test point / U1 output. This is distinct from MX512H pin4 motor VDD. |
| C3.1 | Open | H_VDD | DNP free pads via V064 to board VDD test point / U1 output. This is distinct from MX512H pin4 motor VDD. |
| R2.1 | Open | H_GND | DNP free pads lie on front ground copper shared with V057/V058. |
| C4.1 | Open | H_GND | DNP free pads lie on front ground copper shared with V057/V058. |
| R37.1 | H_VDD | AUX_FEED_V063 | User V063 joins R37 and R39; photo identifies their lower ends. Withdraw conflicting H_VDD and GND guesses. Remote feed unknown. |
| R39.2 | H_GND | AUX_FEED_V063 | User V063 joins R37 and R39; photo identifies their lower ends. Withdraw conflicting H_VDD and GND guesses. Remote feed unknown. |
| R10.2 | H_RF_MONITOR | H_GND | R10 free end visibly joins V116, user GND. |
| R32.1 | H_PIR_SIG | H_GND | R32 photo upper pad to V024, user GND; withdraw earlier PIR-signal guess. |
| Q9.R | Open | H_GND | DNP Q9 lower-right pad to V021, user GND; pad mapping R=stock pin2. |
| U4.12 | Open | PIC_RC1_VREF | PIC pin12 visible trace reaches V053, the VREF-labelled board pad. Remote continuation/function remains unknown. |
| VREF.1 | Open | PIC_RC1_VREF | PIC pin12 visible trace reaches V053, the VREF-labelled board pad. Remote continuation/function remains unknown. |
| Q11.L | H_ANT_A | H_GND | First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established. |
| Q6.L | H_ANT_A | H_GND | First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established. |
| Q5.L | H_ANT_A | H_GND | First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established. |
| Q4.L | H_ANT_A | H_GND | First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established. |
| Q3.L | H_ANT_A | H_GND | First four transistor L pads visibly join V089/V094/V099/V104, user GND. Q3 L joins the same front copper by photo inference. Candidate emitter functions not independently established. |
| C47.1 | H_ANT_B | H_GND | Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown. |
| C44.1 | H_ANT_B | H_GND | Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown. |
| C29.1 | H_ANT_B | H_GND | Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown. |
| C14.1 | H_ANT_B | H_GND | Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown. |
| C11.1 | H_ANT_B | H_GND | Front lower tuning-capacitor common band joins V087/V088 user GND. Withdraw antenna B assignment of these pads; midpoint antenna links remain unknown. |
| C48.1 | H_ANT_B | H_GND | Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping. |
| C45.1 | H_ANT_B | H_GND | Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping. |
| C38.1 | H_ANT_B | H_GND | Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping. |
| C15.1 | H_ANT_B | H_GND | Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping. |
| C12.1 | H_ANT_B | H_GND | Rear tuning-capacitor ground-side lands share copper around V093/V096/V101/V105. These are user-GND sites; opposite lands retain the local front/rear midpoint grouping. |

## Reports held for clarification

- Resolved by user: V025=GND; V026=PIC21/RB0. The onward RB0 destination is still unknown.
- Resolved by user: V073 is GND only. R19/V075 remains a photo association, not user-confirmed.
- Resolved in v0.9.2: V113/V115 reach centre Q8.B2/pin5 GND. The earlier outer-pad annotation was wrong. V114 opposite T2/pin2 net remains unresolved.

## What a component association establishes

V063 establishes a local R37/R39 junction, not its source voltage. V070/R18 and V071/R21 do not establish that their remote sides share a supply or bias node. V076 corroborates the opposite R22 ground return. V067 reaches empty U6A; no fitted chip is missing there. V082 associates D3 but does not settle its exact terminal. V011-V014 are explicitly not connected to R43.2; their previous Q1.L/R43.2 annotation was incorrect. V015 is the corrected R43.2 association.

V090/C46/C47, V095/C43/C44, V100/C16/C29, V103/C13/C14 and V107/C10/C11 corroborate local tuning junctions. Their rear capacitor partners are photo-associated. Ground returns invalidate the old complete antenna series-branch assumption; onward midpoint-to-antenna links still require tracing.

MX512H **pin4 VDD** is the motor supply net H_VBAT. Its **pin1 VCC** and the regulated board VDD test point are on the separate H_VDD model net. V064 joins the latter via the R1/C3 option pads.

## IDs not yet mentioned across the user reviews

V016, V019, V027, V028, V030, V035, V036, V037, V038, V039, V042, V047, V049, V053, V079, V080.

These are not all unresolved: V027/V028/V030/V038/V042 already had local photo matches, and V035/V053 now have additional local associations. No need to recheck every ground site. The interactive viewer distinguishes user-reported assignment, photo-local assignment, unresolved report, held conflict and rejected detection.

## Remaining work

See [complete status report](../output/pdf/PetSafe_completion_status.pdf), [all PIC pins](../evidence/pic_gpio_status.csv), and [per-component audit](FINISHING_CHECKLIST.html). Current native file: 37 open pads (18 populated-entry, 19 DNP), six GPIO pads open; 44 capacitor values and L1/L2 type/value unknown; three blank footprints. Existing drawn hypotheses are additional work and are not counted as open pads.

The PIC under-body candidates V036/37/39/47/49 align approximately with pins5/6/7/11/13; they are targets for continuity, not recovered buried traces. Surface photographs cannot uniquely identify an inner layer or its function.
