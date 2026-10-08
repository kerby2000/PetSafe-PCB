# Via review findings - v0.9

The original user list supplied 97 distinct site IDs. The correction confirms V025=GND and adds V026=PIC21/RB0, bringing the reviewed count to 98. Twenty-nine catalog IDs remain unmentioned; several already have photo-derived local connections. V050 is rejected as not a via, leaving 126 active sites without renumbering the original 127 IDs. No per-via ohms were supplied. Component-endpoint assignments below combine those reports with the existing front/rear photos.

## Applied corrections

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
- V073 was reported as GND and R19. The R19 free-pad via appears to be V075. Do not use the duplicate to ground R19.
- V113/V115: reported GND; front island appears to join Q8 outer pads, modeled as output. Keep this contradiction visible; confirm resistance to GND before changing the output topology.

## What a component association establishes

V063 establishes a local R37/R39 junction, not its source voltage. V070/R18, V071/R21 and V072/R22 do not establish that their remote sides share a supply or bias node. V076 corroborates the opposite R22 ground return. V067 reaches empty U6A; no fitted chip is missing there. V082 associates D3 but does not settle its exact terminal. V011-014 visibly share the Q1.L/R43.2 island, with transistor pin function still provisional.

V090/C46/C47, V095/C43/C44, V100/C16/C29, V103/C13/C14 and V107/C10/C11 corroborate local tuning junctions. Their rear capacitor partners are photo-associated. Ground returns invalidate the old complete antenna series-branch assumption; onward midpoint-to-antenna links still require tracing.

MX512H **pin4 VDD** is the motor supply net H_VBAT. Its **pin1 VCC** and the regulated board VDD test point are on the separate H_VDD model net. V064 joins the latter via the R1/C3 option pads.

## IDs absent from this user message

V016, V017, V019, V020, V027, V028, V030, V033, V035, V036, V037, V038, V039, V042, V047, V049, V053, V075, V079, V080, V091, V097, V102, V108, V117, V119, V120, V122, V124.

These are not all unresolved: V027/V028/V030/V038/V042 already had local photo matches, and V035/V053 now have additional local associations. No need to recheck every ground site. The interactive viewer distinguishes user-reported assignment, photo-local assignment, unresolved report, held conflict and rejected detection.

## Remaining work

See [complete status report](../output/pdf/PetSafe_completion_status.pdf), [all PIC pins](../evidence/pic_gpio_status.csv), and [per-component audit](FINISHING_CHECKLIST.html). Current native file: 37 open pads (18 populated-entry, 19 DNP), eight GPIO pads open; 44 capacitor values and L1/L2 type/value unknown; three blank footprints. Existing drawn hypotheses are additional work and are not counted as open pads.

The PIC under-body candidates V036/37/39/47/49 align approximately with pins5/6/7/11/13; they are targets for continuity, not recovered buried traces. Surface photographs cannot uniquely identify an inner layer or its function.
