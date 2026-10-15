# Recorded measurements and observations

Recorded evidence, retained through v0.9.39, updated 2026-10-14. These are user reports. The antenna batch is complete: M-ANT1 OL, M-ANT2 OL, ANT1-ANT2 approximately 5 ohms; C11 outer end N to GND 414 kohm, N-ANT1 5 ohms (repeated), ANT1-GND 414 kohm. The follow-up 414 kohm initially attributed to N-ANT2 was corrected by the user to ANT2-GND. The actual N-ANT2 measurement is **1.4 ohm**, supporting the corrected ANT2 connection. The earlier “below 1 ohm” was an expectation, not a measured value. No repeat requested. See the [result record](../evidence/antenna_outer_rail_results_20261014.json) and [bounded schematic correction](../evidence/antenna_outer_rail_correction_v0937.json). Completed readings and raw corrections are preserved; older questions are history, not new requests.

Available instruments reported by the user: LCR meter, Fluke 179 and Fluke 87 III. The earlier Fluke 114 inference is superseded. Six powered DC readings are now recorded: TP14/OUTA 0 V (the earlier BATTERY+ association was rejected by B60 and corrected using TP14-U5.8 = 1.5 ohm), VSYS 6.3 V, RF supply 6.3 V, VDD 4.5 V, VREF 0 V and J3.1/PIR supply 3.3 V with the PIR connected. The red LED blinked approximately once per second. See [the supply results](../evidence/supply_baseline_results_20261014.json). These are operating-state observations, not complete functional validation. B59 C25/RA0-to-TP6 = 1.5 ohm supports the RX_A_FILTER net merge. The 44 fitted ceramic values remain unmeasured; L1/L2 readings are recorded below.

## Numeric electrical results

The resistance and diode measurement requests below specified battery and programmer disconnected. The separately recorded B53-B58 supply checks were powered DC voltage readings. Shorted probe tips were initially pressure-dependent (2-5 ohm), then the user obtained **0.5 ohm**. Do not subtract a fixed baseline from every earlier reading or describe 2 ohm as exact copper resistance.

| Test | User reading | Interpretation |
|---|---|---|
| U6 G-C | 2.7 ohm | Supports ground at C; contact baseline was uncertain |
| U6 G-B | 34 kohm | Resistive path, not a direct ground join |
| U6 G-A | 4.2 kohm | Resistive path, not a direct ground join |
| Q8 D-E | 2 ohm | Supports the joined outer-pad node |
| Q8 E-F | 400 kohm | Rejects direct C6-to-output copper |
| Q8 S-G | 2 ohm | Supports ground association |
| Q8 F-P, earlier | 10 ohm | Preserved observation; superseded for current connection assessment by B37 below |
| Q8 P-F, B37 | 1 ohm | Supports Q8.T2/native2 to C6.1 on H_RF_VDD. Fresh baseline/stability not supplied; no exact trace-resistance or device-identity claim |
| Q8 F-G | 300 kohm | Not direct ground |
| V064-V070 | 11.2 kohm | Supports R18 1.2k + R19 10k hypothesis; not direct VDD |
| V049-V071 | 20 kohm | Not direct continuity |
| V049-V070 | Variable 200-300 kohm | Contact-dependent/inconclusive, not OL |
| V090 to V095/V100/V103/V107 | OL, all four | No direct continuity in this test |
| V095 to V100/V103/V107 | OL, all three | No direct continuity in this test |
| D3.S to R42 | 1.2 ohm | Supports a direct connection to one R42 pad; pad2 selected from photo, not explicitly named in the reading |
| D2, all three unordered pin pairs | Variable 1-2 Mohm | User calls readings unreliable and probe-placement-dependent. Individual values and probe polarity unspecified; initial resistance readings alone did not establish identity/pin functions |

Lettered Q8/U6 endpoints refer to the preserved annotated measurement photos, not package pin numbers. OL does not imply the absence of capacitive coupling.

The subsequent [D2 resistance record](../evidence/d2_resistance_20261009.json) supplies all six probe polarities:

| Red probe | Black probe | Reported resistance |
|---|---|---|
| L | R | 0.5 Mohm |
| R | L | 1.44 Mohm |
| L | S | 272 kohm |
| S | L | 1.75 Mohm |
| R | S | 1.75 Mohm |
| S | R | 272 kohm |

These are in-circuit resistance readings, not junction voltages. Their asymmetry does not establish a unique device identity or pinout; these readings alone did not justify a schematic change.

D3 rail association is separately closed: user reports D3.L to GND and D3.R to board VDD through V082. See the [D3 measurement record](../evidence/d3_measurement_20261009.json).

### D2 diode-mode follow-up: completed

The completed [six diode readings](../evidence/d2_diode_20261009.json) are:

| Red probe | Black probe | Diode-mode reading |
|---|---|---|
| L | R | OL |
| R | L | 1.2 V |
| L | S | OL |
| S | L | 0.6 V |
| R | S | 0.6 V |
| S | R | OL |

They strongly support two series junctions conducting **R -> S -> L**: R is the outer anode, S the midpoint, and L the outer cathode in this working equivalent. The earlier simple PNP candidate is a poor fit to this pattern. In-circuit measurement does not prove that both junctions are internal to D2.

This resembles the **topology** of BAV99; its exact identity, ratings and package numbering are still unproved. Nexperia's BAV99 marking is A7 plus site code, not 4P. The active D2 symbol remains an explicitly numbered unknown-device placeholder; earlier guessed rail connections are withdrawn. All three local destinations are now resolved as listed below.

Follow-up rail checks: **D2.R -> GND = 0.78 Mohm**, **D2.R -> VDD = 0.99 Mohm**. The user explicitly confirms that the second reading is R-VDD, not L-VDD. Neither reading supports a direct rail connection. Neither high resistance is recorded as OL or used to merge nets.

The [user's annotated pad photo](../photos/user_updates/D2_user_pad_labels_20261009.png) fixes the measurement labels: **R is upper-left toward C20, L is upper-right beside R46, S is the single lower pad**. These letters are user labels, not automatic left/right directions. The measured sequence R -> S -> L is unchanged. Native placeholder numbers remain bookkeeping, not a verified device pinout.

The user subsequently supplied **L -> VDD = 740 kohm** and **L -> GND = 450 kohm**. All four outer-pad rail checks are now complete, with no direct VDD/GND join supported. This makes the simple ground-to-VDD clamp assumption unlikely; it does not exclude other diode functions or establish a defective part. Do not model these in-circuit resistances as discrete resistors.

The subsequent local checks resolve all three D2 destinations:

| Check | User result | Model interpretation |
|---|---|---|
| R -> C20 lower metal end | 1 ohm | D2.R/native2 joins C20.2 on D2_C20; the former RX_A_PLUS assignment is superseded by the v0.9.46 measurements |
| S -> requested ANT2 terminal | OL | No direct copper join; preserve separate nodes |
| L -> ANT2 | Directly connected | D2.L/native1 joins ANT2 on H_ANT_B |
| S -> GND TP | 700 kohm | No direct GND connection established |
| S -> VREF TP | 1.32 Mohm | No direct VREF connection established |
| S -> R46 lower pad | Clearly connected | D2.S/native3 joins R46.2 on D2_MID |
| R46 upper pad -> L / ANT2 | Connected | R46.1 joins H_ANT_B |

The user confirms **R46 is unpopulated**. Its pads sit across the probable S-to-L junction, but there is no fitted resistor or jumper between them. Upper=1/lower=2 are model assignments for this empty nonpolar option. This establishes D2's local connections, not the exact 4P identity or package numbering. The later [receiver-input results](../evidence/receiver_input_results_20261015.json) establish D2_C20 = D2.R/C20.2/R28.2 and reject a direct join to U3.3 or TP7. R28.1 remains on TP7/PIC RA1 through the existing 1-Mohm resistor. Subsequent RX-1 = 1.023 Mohm and RX-2 = 271 kohm, versus 1-ohm probes, reject C19.1-to-U3.3 and C20.1-to-GND; their onward destinations remain unknown. Settling behavior was not supplied. C19 and C20 are not a verified parallel pair; their individual starred estimates are unchanged. All local/rail tests are recorded in [the D2 evidence record](../evidence/d2_diode_20261009.json); no repeat sweep is needed.

## Further completed readings and corrections

| Evidence | Current result |
|---|---|
| U3/J3 batches | U3.5-VREF/R22.2 about 1 ohm; R22.1 GND. U3.6-R23.1 about 1 ohm, 5.6k through R23. R23.2-C40.1/R42.1 about 1 ohm each. J3.3-GND about 1 ohm; J3.2-R38 about 1 ohm, 10k through R38; J3.2-GND 290k. |
| Rejected direct joins | R23 to C18/TP6: 300k/400k/600k; TP16 to TP11/TP17: 400k each. Values are preserved as resistance, not OL or fictitious fitted resistors. |
| PIC21/PIR | TP16-VREF 0.8 Mohm; user explicitly withdrew PIC21-VREF and confirmed PIC21-TP16/Q2.S. U7.1/2/3 connect to J3.3/2/1. |
| D6/U6 | D6 V-GND and W-VPP about 1 ohm; V-to-W 0.7 V, reverse OL: A=GND/K=VPP. U6 pin5-pin2 about 1 ohm. Pin4 unused by user/photo evidence. |
| Photo/user routing | C25-RA0, C26-RA1 with shared ground; C6 parallels C5; R47/C42 stage-link copper; R41-VPP; J6/Q9 options; U6A's three pads. No new numerical reading is implied by annotations. |
| C49 | User confirms rear C49 between ANT2 and GND; existing DNP status retained. |
| L1 / L2 | LCR readings **1.4 uH / 2.2 uH**. Frequency, mode, fixture compensation and isolation condition are unreported; exact nominal part and ratings remain qualified. |

See [U3/J3 batch1](../evidence/u3_j3_measurements_20261009.json), [batch2](../evidence/u3_j3_batch2_20261009.json), [R23 batch3](../evidence/u3_r23_batch3_20261009.json), [batch4](../evidence/u3_r23_batch4_20261009.json), [PIC21 correction](../evidence/pic21_tp16_followup_20261009.json), [D6/U6 results](../evidence/d6_u6_open_pad_results_20261009.json), [C49 record](../evidence/c49_connections_20261009.json) and [L1/L2 record](../evidence/l1_l2_inductance_20261009.json). The [measurement page](FINISHING_MEASUREMENTS.html) retains probe labels and all completed readings.

## Markings and dimensions already supplied

U6=C2NM; Q8=3724A; D2=4P; D3=A7; D4/D5=5U; D6=G3; R41=331 (330 ohm). R29/R44=18C (15k) came from photographs, not new meter readings.

| Part | Supplied observation | What remains |
|---|---|---|
| C5 | 470 uF / 16 V; diameter 6.33 mm, height 16 mm | Lead pitch/drill fit for PCB reproduction; stock 7 mm housing differs from actual 16 mm |
| R8 | 1.6 x 0.77 mm including end caps | 0603 body supported; ratings/other resistors remain qualified |
| C11 | About 3.2 x 1.5 mm | 1206 supported; capacitance unknown |
| S1 | 6 x 6 x 4 mm body, plus 2 mm actuator | Contacts verified in B38-B41; exact pad fit remains; stock 4.3 mm model differs from actual about 6 mm height |
| LED1 | Red and green emitters, square 1.5 x 1.5 mm | Pad geometry/numbering and matching footprint; colour branches established by B42/B43 |

Reported connections without numerical resistance remain **user continuity reports**, never fabricated 0.0-ohm readings. V053-V071/VREF and Q1.L-R43.2 are withdrawn/rejected. V114 is U2.T2 ground, not Q8; V072 is TP6, not R22.2. Raw BATTERY+ and post-Q1 VSYS remain separate. See [current via findings](VIA_REVIEW_RESULTS.md) and the [question register](../evidence/remaining_work.json).

## 2026-10-09 Q3 diode results and R33 inspection

Q3 red QL / black QR: 2.3 V; reverse: OL. Red QL / black QS: latest 0.48 V, previously 0.35 V; reverse: OL. QR/QS: OL both ways. In-circuit results do not confirm the candidate PNP pin map; no copper changes derived from them. User could not locate R33; the unsupported entry and assumed pull-up have been withdrawn. See [the archived event](history/q3-r33-v0932.md) and the [active checklist](FINISHING_CHECKLIST.html).

## S1 contacts, v0.9.34

A-B and C-D: 1 ohm each. B-D: OL released, 1 ohm held pressed. Additional A-C: OL, without a separate button-state label. Confirms the drawn common pairs and normally-open action; E05 closed. Exact footprint/housing remains qualified. Raw evidence: [S1 results](../evidence/s1_contact_results_20261009.json).

## LED1 colour results, v0.9.35

With black on K, A lights green and B lights red. Photo A reaches R31/PIC22/native LED1 pin2; B reaches R30/PIC23/native pin1. The user reported 0.96 V and then clarified that it applies to both A-K and B-K. Both readings are recorded as in-circuit diode-mode observations. No isolated LED forward-voltage specification or manufacturer pad numbering is inferred. [Raw results](../evidence/led1_colour_results_20261009.json).

## Antenna midpoint results, 2026-10-14

[Raw reports and interpretation](../evidence/antenna_midpoint_results_20261014.json): B44 M-A = OL; B45 M-B = OL; B46 A-B approximately 5 ohms. Requested setup was resistance mode, battery/programmer disconnected and antenna left fitted. No direct midpoint-to-antenna DC path was detected; capacitive coupling remains possible. The 5-ohm path does not turn ANT1 and ANT2 into one PCB copper net. Schematic connectivity is unchanged.

B62 TP5/H_RX_VDD to GND: **0.066 V (66 mV)**, powered in the same red-blinking state with PIR connected. Stability was not reported. This does not establish a short or a defective Q7. See [receiver supply evidence](../evidence/receiver_supply_results_20261014.json); subsequent B63/B64 readings are below.

B63/B64 R19 left/right to GND: **0 V / 4.5 V** in the same powered red-blinking state. Stability not supplied. B65/B66 below subsequently confirmed the R19-to-Q7 joins. See [Q7/R19 conflict and next checks](../evidence/q7_r19_voltage_results_20261014.json).

B65/B66: **Q7.L-R19.1 = 1.5 ohm; Q7.R-R19.2 = 1.5 ohm**, unpowered. Both existing joins are now measurement-supported, without changing nets. Candidate terminal roles and operating behavior remain open; the subsequent diode results are below. See [join results](../evidence/q7_r19_join_results_20261014.json).

B67-B70, Q7 fitted and power disconnected: **QR->QL 0.74 V; QL->QR 1.74 V; QS->QL 0.74 V; QL->QS OL**. Supports PNP/base-at-QL polarity; E/C and exact identity are not independently established. Parallel circuit paths can explain finite reverse readings. B71 below supplies the direct powered comparison. See [diode evidence](../evidence/q7_diode_results_20261014.json).

B71 direct powered **QR-QL = 0 V**, original battery and PIR connected. Stability not supplied. Supports no forward base-emitter bias in the latest state, consistent with inactive Q7/low receiver supply. Earlier separate 0/4.5 V readings remain conflicting historical observations; no part failure is inferred. See [direct bias result](../evidence/q7_direct_bias_result_20261014.json). Next: E03 Q8 gate-source voltages.

B72/B73 powered at rest: **Q8 candidate P-channel VGS = 0 V; N-channel VGS = +6.3 V**. Stability not supplied. Supports P off/N on bias, not waveform or current verification. U2 is modeled on 4.5 V VDD, so B74/B75 now check its supply against C6/RF and printed VDD separately. See [Q8 gate-bias evidence](../evidence/q8_gate_bias_results_20261014.json).

B74/B75, unpowered: **U2 UV to C6 PS = 24 ohm; U2 UV to printed VDD = 48 ohm**. No new probe baseline or stability report supplied. Neither establishes a direct copper join; no rail merge or added resistor follows. B76 now requests U2 local supply voltage against confirmed ground. See [U2 supply-join evidence](../evidence/u2_supply_join_results_20261014.json).

The user additionally reports continuity beeps on both B74/B75 pairs (Fluke model/range unspecified). This does not establish a copper join. Current-model review finds no series resistor in U2.5-to-VDD; R5=22 ohm is in the RF output/antenna branch, R8/R9=220 ohm are gate resistors, and R37=22 ohm feeds the PIR regulator. RF-to-VDD includes L1/L2 and active regulator U1; that is not a simple resistance calculation. The cause of 24/48 ohm remains unresolved.

B76, powered: **U2 supply UV to Q8 confirmed ground NS=6.3V**. Stability not supplied. This challenges the modeled U2-to-regulated-VDD association but does not establish a new copper join; B77 compares these nodes directly in one state. If U2 is the SN74LVC2G14 candidate,6.3V exceeds its recommended5.5V supply maximum; identity/operation remain qualified. See [U2 local voltage evidence](../evidence/u2_supply_voltage_result_20261014.json).

B77, powered direct **U2 UV to printed VDD = +1.8 V**. This rejects their drawn direct copper connection. Actual U2 supply feed remains to be traced; B78/B79 check U2-to-C7 and C7-to-C6. See [direct separation evidence](../evidence/u2_vdd_separation_result_20261014.json).

B78/B79, unpowered: **U2-to-C7 upper end = 1.5 ohm; C7 upper-to-C6 upper = 27 ohm**. Local bypass join is supported; direct RF rail join is not. R5=22 ohm is now the targeted series-feed candidate; its inherited RF output placement was inferred. See [C7 feed evidence](../evidence/u2_c7_feed_results_20261015.json).

B80/B81: **C7 upper-R5 upper = 4 ohm; C6 upper-R5 lower = 3.3 ohm**. Combined evidence supports R5 as the 22-ohm U2 supply feed; old output/antenna placement withdrawn. Contact contributions remain unquantified. B82 checks Q8 output-to-ANT1. [R5 evidence](../evidence/r5_supply_feed_results_20261015.json).

## 2026-10-15 - RF output and supply correction

B82 Q8 joined output to ANT1: **4.5 ohm**, antenna fitted. B82 OD-ANT1 = 4.5 ohm. Alone this cannot distinguish contact resistance from a path through the fitted approximately 5-ohm antenna. IMG_2431 shows the joined outer Q8 pads; board_upper.png shows that output copper continuing around Q8 toward ANT1. The direct output-to-ANT1 route is accepted as photo-supported with a compatible low-resistance reading, not proved by resistance magnitude alone. R5 is not in this output path.

Current topology: RF supply -> R5 (22 ohm) -> U2/C7; Q8 output -> ANT1. Printed VDD remains separate. [Bounded correction](../evidence/u2_r5_topology_correction_v0940.json). Owner has a scope but defers its use; continue schematic values, identities and packages first.
