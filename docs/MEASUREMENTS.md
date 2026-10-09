# Recorded measurements and observations

Current as of 2026-10-09. These are user reports, not measurements performed by software. Full event records remain in `evidence/measurement_plan.json`, `evidence/via_audit.json`, the versioned net-change records and the [via-pair results](VIA_PAIR_TESTS.html). [The checklist](FINISHING_CHECKLIST.html) distinguishes remaining work.

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
| Q8 F-P | 10 ohm | Exact path remains unresolved; not a proven copper join |
| Q8 F-G | 300 kohm | Not direct ground |
| V064-V070 | 11.2 kohm | Supports R18 1.2k + R19 10k hypothesis; not direct VDD |
| V049-V071 | 20 kohm | Not direct continuity |
| V049-V070 | Variable 200-300 kohm | Contact-dependent/inconclusive, not OL |
| V090 to V095/V100/V103/V107 | OL, all four | No direct continuity in this test |
| V095 to V100/V103/V107 | OL, all three | No direct continuity in this test |
| D3.S to R42 | 1.2 ohm | Supports a direct connection to one R42 pad; pad2 selected from photo, not explicitly named in the reading |
| D2, all three unordered pin pairs | Variable 1-2 Mohm | User calls readings unreliable and probe-placement-dependent. Individual values and probe polarity unspecified; identity/pin functions remain unresolved |

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

These are in-circuit resistance readings, not junction voltages. Their asymmetry does not establish a unique device identity or pinout; no schematic change is justified.

**Equipment clarification:** the user confirms a **Fluke 179**, superseding the assistant's Fluke 114 inference from a photograph. The 179 supports diode test: turn to the continuity/diode position and press the yellow button to select diode mode, then check that the diode icon is displayed. With battery/programmer disconnected and capacitors discharged, repeat the same six combinations and record voltage or OL. See the manufacturer's [selector table](https://assets.fluke.com/manuals/175_____umeng0100.pdf) and [yellow-button instructions](https://assets.fluke.com/manuals/175_____umeng0200.pdf). Even diode-mode results in circuit may not uniquely identify D2.

D3 rail association is separately closed: user reports D3.L to GND and D3.R to board VDD through V082. See the [D3 measurement record](../evidence/d3_measurement_20261009.json).

### D2 diode-mode follow-up: completed

The [six diode readings](../evidence/d2_diode_20261009.json) supersede the pending test request above:

| Red probe | Black probe | Diode-mode reading |
|---|---|---|
| L | R | OL |
| R | L | 1.2 V |
| L | S | OL |
| S | L | 0.6 V |
| R | S | 0.6 V |
| S | R | OL |

They strongly support two series junctions conducting **R -> S -> L**: R is the outer anode, S the midpoint, and L the outer cathode in this working equivalent. The earlier simple PNP candidate is a poor fit to this pattern. In-circuit measurement does not prove that both junctions are internal to D2.

This resembles the **topology** of BAV99; its exact identity, ratings and package numbering are still unproved. Nexperia's BAV99 marking is A7 plus site code, not 4P. Do not import a BAV99 symbol with the old L/R numbering or restore earlier guessed rail connections. All three external endpoints remain open in the schematic.

Follow-up rail checks: **D2.R -> GND = 0.78 Mohm**, **D2.R -> VDD = 0.99 Mohm**, exactly as reported. The first does not support a direct ground connection and makes the simple ground-to-VDD clamp hypothesis unlikely. The second remains labeled R-VDD even though L-VDD was requested; pad clarification is pending. Neither high resistance is recorded as OL or used to merge nets.

## Confirmed connections and exclusions

Reported connections without numerical resistance are recorded as **user continuity reports**, not fabricated 0.0-ohm readings. Key examples include V022-V016 (PIC15-U5.2), V023-V019 (PIC16-U5.3), V036-V108, V037-V102, V039-V097, V047-V091, V064-V063, V064-V075, and V053-V070. See the [current via summary](VIA_REVIEW_RESULTS.md) and per-site audit for all reports.

V053-V071 and V053-VREF were explicitly rejected. Q1.L-R43.2 was explicitly withdrawn. Raw BATTERY+ and post-Q1 VSYS are distinct nets. V114 was corrected to U2.T2 ground, not Q8. V072 reaches TP6, not R22.2. These negative/corrective results remain constraints on future edits.

## Markings and dimensions

User readings: U6=C2NM; Q8=3724A; D2=4P; D3=A7; D4/D5=5U; D6=G3; R41=331 (330 ohm); C5=470 uF / 16 V. R29/R44=18C (15 kohm) came from photographs rather than a new meter reading.

User dimensions: C11 approximately 3.2 x 1.5 mm supports 1206; R8 approximately 1.6 x 0.77 mm, **including both metal end caps**, supports 0603. Other packages remain family/photo estimates until individually supported.

## Not yet measured

No actual rail voltages, powered functional results or LCR capacitor/inductor values have been supplied. The user has an LCR meter, a Fluke 179 and a Fluke 87 III. Both Fluke models support diode testing; see also the [87 III manual](https://assets.fluke.com/manuals/8xiii___umeng0300.pdf). Prioritize RF/tuning values; record frequency, mode and in-circuit versus isolated-lead status. Do not infer a ceramic's value, voltage rating or dielectric from package size.
