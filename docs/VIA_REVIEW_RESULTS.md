# Via review findings - v0.9.1

101 distinct via IDs reviewed; 125 active sites / 127 stable IDs. V033 and V050 are rejected without renumbering; 26 IDs remain unmentioned, some already photo-matched. The latest batch corrects 21 sites. V017 joins R42.1 and R44.1 (R44 pad selected from the photo), replacing the earlier R42.1-to-ANT2 hypothesis. R43.2 is associated with V015, not V011-V014. V072-to-R22.2 is withdrawn. V073 is GND only; R19/V075 remains photo-derived. V113/V115 are the two remaining held conflicts. No new per-site ohms were supplied.

## Latest 21-site corrections

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
| V072 | Not R22.2; destination unresolved | Rejected via association; prior independent receiver-bias hypothesis still unverified |
| V073 | GND only | User explicitly resolves duplicate; no R19 ground merge |

Only two component-pad net assignments change in this batch: R42.1 and R44.1 join `V017_CONTROL`. The other entries correct via metadata or corroborate existing qualified pad assignments. The original `V_Q1_LEFT` fragment (Q1.L to R43.2) remains; the user corrected the via location, not this independent local trace. V075/R19.2 remains a photo association, not a newly confirmed user mapping.

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
- V113/V115: reported GND; front island appears to join Q8 outer pads, modeled as output. Keep this contradiction visible; confirm resistance to GND before changing the output topology.

## What a component association establishes

V063 establishes a local R37/R39 junction, not its source voltage. V070/R18 and V071/R21 do not establish that their remote sides share a supply or bias node. V076 corroborates the opposite R22 ground return. V067 reaches empty U6A; no fitted chip is missing there. V082 associates D3 but does not settle its exact terminal. V011-V014 are explicitly not connected to R43.2; their previous Q1.L/R43.2 annotation was incorrect. V015 is the corrected R43.2 association.

V090/C46/C47, V095/C43/C44, V100/C16/C29, V103/C13/C14 and V107/C10/C11 corroborate local tuning junctions. Their rear capacitor partners are photo-associated. Ground returns invalidate the old complete antenna series-branch assumption; onward midpoint-to-antenna links still require tracing.

MX512H **pin4 VDD** is the motor supply net H_VBAT. Its **pin1 VCC** and the regulated board VDD test point are on the separate H_VDD model net. V064 joins the latter via the R1/C3 option pads.

## IDs not yet mentioned across the user reviews

V016, V019, V027, V028, V030, V035, V036, V037, V038, V039, V042, V047, V049, V053, V075, V079, V080, V091, V097, V102, V108, V117, V119, V120, V122, V124.

These are not all unresolved: V027/V028/V030/V038/V042 already had local photo matches, and V035/V053 now have additional local associations. No need to recheck every ground site. The interactive viewer distinguishes user-reported assignment, photo-local assignment, unresolved report, held conflict and rejected detection.

## Remaining work

See [complete status report](../output/pdf/PetSafe_completion_status.pdf), [all PIC pins](../evidence/pic_gpio_status.csv), and [per-component audit](FINISHING_CHECKLIST.html). Current native file: 37 open pads (18 populated-entry, 19 DNP), eight GPIO pads open; 44 capacitor values and L1/L2 type/value unknown; three blank footprints. Existing drawn hypotheses are additional work and are not counted as open pads.

The PIC under-body candidates V036/37/39/47/49 align approximately with pins5/6/7/11/13; they are targets for continuity, not recovered buried traces. Surface photographs cannot uniquely identify an inner layer or its function.
