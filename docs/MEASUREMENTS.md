# Recorded measurements and observations

Recorded evidence, retained through v0.9.31, 2026-10-09. These are user reports, not measurements made by software. The only active bench request is the [Q3 diode-mode batch](FINISHING_MEASUREMENTS.html). Dated raw JSON events and completed photo-guide contacts are preserved here as reference, not new requests. Earlier requests are archived in [the previous narrative](history/cleanup_v0928/docs/MEASUREMENTS.md); do not repeat a reading just because it occurs there.

Available instruments reported by the user: LCR meter, Fluke 179 and Fluke 87 III. The earlier Fluke 114 inference is superseded. No actual rail voltages or powered functional results have been supplied. The 44 fitted ceramic values remain unmeasured; L1/L2 readings are recorded below.

## Numeric electrical results

The measurement requests specified battery and programmer disconnected. Shorted probe tips were initially pressure-dependent (2-5 ohm), then the user obtained **0.5 ohm**. Do not subtract a fixed baseline from every earlier reading or describe 2 ohm as exact copper resistance.

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
| R -> C20 lower metal end | 1 ohm | D2.R/native2 joins C20.2 on RX_A_PLUS |
| S -> requested ANT2 terminal | OL | No direct copper join; preserve separate nodes |
| L -> ANT2 | Directly connected | D2.L/native1 joins ANT2 on H_ANT_B |
| S -> GND TP | 700 kohm | No direct GND connection established |
| S -> VREF TP | 1.32 Mohm | No direct VREF connection established |
| S -> R46 lower pad | Clearly connected | D2.S/native3 joins R46.2 on D2_MID |
| R46 upper pad -> L / ANT2 | Connected | R46.1 joins H_ANT_B |

The user confirms **R46 is unpopulated**. Its pads sit across the probable S-to-L junction, but there is no fitted resistor or jumper between them. Upper=1/lower=2 are model assignments for this empty nonpolar option. This establishes D2's local antenna/receiver connections; it does not identify the exact 4P component, validate package numbering, or confirm the other inferred C20/C19/R28/U3.3 branches. All local/rail tests are recorded in [the D2 evidence record](../evidence/d2_diode_20261009.json); no repeat sweep is needed.

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
| S1 | 6 x 6 x 4 mm body, plus 2 mm actuator | Contact behavior and exact pad fit; stock 4.3 mm model differs from actual about 6 mm height |
| LED1 | Red and green emitters, square 1.5 x 1.5 mm | Pad geometry/numbering, channel mapping and matching footprint |

Reported connections without numerical resistance remain **user continuity reports**, never fabricated 0.0-ohm readings. V053-V071/VREF and Q1.L-R43.2 are withdrawn/rejected. V114 is U2.T2 ground, not Q8; V072 is TP6, not R22.2. Raw BATTERY+ and post-Q1 VSYS remain separate. See [current via findings](VIA_REVIEW_RESULTS.md) and the [question register](../evidence/remaining_work.json).

## 2026-10-09 Q3 diode results and R33 inspection

Q3 red QL / black QR: 2.3 V; reverse: OL. Red QL / black QS: latest 0.48 V, previously 0.35 V; reverse: OL. QR/QS: OL both ways. In-circuit results do not confirm the candidate PNP pin map; no copper changes derived from them. User could not locate R33; the unsupported entry and assumed pull-up have been withdrawn. See [the archived event](history/q3-r33-v0932.md) and the [active checklist](FINISHING_CHECKLIST.html).
