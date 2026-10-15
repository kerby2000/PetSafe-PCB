# Independent electronics review — PetSafe 100-1339 R03 A

**Snapshot:** supplied ZIP at `6ae4eaae5c20a08986edd82a593c8a1969a96641`, v0.9.28. **Method:** read `START_REVIEW.txt` and `docs/reviews/2026-10-09_pro_review_v0.9.28.md`; inspected committed XML netlist, ERC JSON, evidence and user measurements, schematic documentation and original photo references. This is an independent logical/electrical audit, **not** a new bench measurement or fresh KiCad CLI run (KiCad CLI unavailable here). Files have not been modified.

## Readiness

- **File consistency:** strong: 85 modeled partitions match exported netlist; zero open modeled pads. This only establishes agreement of two representations of the *same hypotheses*.
- **Topology:** **not finished**. The tuned antenna, excitation supply/control and demodulation/detector endpoints still have incomplete functional paths; Q3–Q11 transistor model has a polarity concern.
- **Device identity/values:** U1/U5/U6/Q8 remain datasheet-supported *candidates* rather than fully validated parts; 44 ceramic capacitances unknown. The D2 equivalent topology is better supported by measurements than its exact marking identification.
- **PCB reproduction:** not ready; PCB stack/routing, exact passives and LED footprint aren't captured to manufacture.

## Priority findings

### P0 — Five antenna tuning branches have a potential device-orientation/type error
**Refs:** Q3/Q4/Q5/Q6/Q11; R13–R16/R11; C10–C16 etc.; `TUNE_*`. **Evidence:** `output/PetSafe_netlist.xml`, `evidence/proposed_nets.csv`, `photos/originals/IMG_2433.jpg`, `IMG_2442.jpg`, `docs/MEASUREMENTS.md` (seven OL pairs).

The schematic models five **PNP** devices with the emitter (native pin 2) on GND and bases fed through 1.8-kΩ resistors from positive-supply PIC GPIOs. That is **not conventional forward-biased PNP switching**, and the antenna continuation of their capacitive midpoint nodes is incomplete. A matching transistor marking alone does not validate the physical B/E/C assignment. **High confidence as a contradiction with the presumed switch explanation; moderate confidence that at least one inferred assignment is wrong.**

**Smallest correction now:** no rewiring by conjecture. Mark Q3–Q11 transistor pin assignment / switching role explicitly provisional. Identify the Q3 physical E/B/C contacts and complete exactly one cell before repeating topology across the rest. Preserve seven measured OL exclusions.

### P0 — RF drive path still has no established driving source
**Refs:** U2 outputs/inputs, R6.2, R7.1, D1, Q8, R5, ANT1/2; `H_RF_CONTROL` and `H_D1_FREE`. **Evidence:** `output/PetSafe_netlist.xml`: `H_RF_CONTROL` contains *only* R6.2 and R7.1; `H_D1_FREE` contains *only* D1.2; `H_ANT_A` includes just TP105/R5.2; `H_ANT_B` includes C49/D2/R46/TP106.

A two-terminal internal connection of resistor ends is not the same as an oscillator excitation input. Check that the currently modeled U2 drive/timing circuit has a physical source and DC/AC return rather than assuming the common net is self-driven. D1's singleton may represent a missing RF/clamp connection, but its precise topology cannot be inferred from the short A7 marking. **High confidence incomplete; specific missing net unknown.**

**Smallest correction:** trace visible copper from R6.2/R7.1 and D1.2 first. Only after photo inspection request a single precise pad-to-via or pad-to-component continuity measurement. No blanket merge to antenna, ground, or a PIC signal.

### P1 — Receiver signal path to controller remains ambiguous
**Refs:** U3.1/U3.7, R25.1/R25.2, C23.2, R47/R48, D2.2; `H_RX_DETECT`, `RX_STAGE_LINK`. **Evidence:** `output/PetSafe_netlist.xml`; `docs/FINISHING_MEASUREMENTS.html` (R23/C40/R42 batch); `evidence/remaining_work.json` E08.

The current `H_RX_DETECT` net contains C23.2 and R25.1, without an identified MCU input or explicit threshold circuit. R25.2 is on `RX_STAGE_LINK`; the D2.R–C20/U3.3 path is now grounded in measurements. This is **not necessarily a circuit error** (a node may be an AC coupling junction), but the intended detector output to the PIC has not been demonstrated. **High confidence functional explanation missing, medium confidence any existing net is incorrect.**

**Smallest correction:** trace the actually visible connections from U3 outputs and the surrounding C23/R25/R47 circuit before asking for probe work. Do not resurrect previously rejected R25-GND, R48-VREF, R23-VREF or C40-to-output connections.

### P1 — Q8 high-side gate turn-off cannot be assumed
**Refs:** Q8 source on `H_RF_VDD`, gates R8/R9 driven by U2 on `VDD`; `VSYS` after Q1 and L1. **Evidence:** `output/PetSafe_netlist.xml`, `docs/U6_Q8_MARKING_UPDATE.md`, `docs/MEASUREMENTS.md` (Q8 10 Ω versus 400 kΩ readings), SIL3724A candidate datasheet.

If P-source voltage is higher than the high-level gate voltage of U2, P-channel VGS can remain negative when the logic output is high. Device may not fully turn off. This remains a **conditional risk**, not evidence of measured cross-conduction. Q8 paired pad/orientation evidence also needs a final pin-map sanity check. **Moderate concern.**

**Smallest correction:** preserve current measured nodes; check the hypothetical VSYS/VDD mismatch with one powered scope capture, after unpowered path review.

### P1 — U1 regulator ON/OFF = VIN is plausible, but unmeasured source-model voltage
**Refs:** U1.1 VIN / U1.3 ON-OFF both `Net-(U1-ON/OFF)`; U1.5 VDD. **Evidence:** current XML, ABLIC S-1200 datasheet, `output/erc.json`.

The ON/OFF-to-VIN connection makes sense for an active-high-enabled LDO, and is not automatically an electrical bug. However, the actual VIN source through L2 and the regulator voltage have not been measured. Do not 'fix' the ERC by connecting `VDD` and `VSYS`, or by inserting an output power symbol on a node of uncertain provenance. **Low topology concern, medium verification need.**

### P2 — U6A option should not drive ERC when DNP
**Refs:** U6 fitted output pin 3 and U106.2 DNP output on `H_PIR_VDD`; `output/erc.json` power-output conflict. **Evidence:** `docs/FINISHING_MEASUREMENTS.html` U6A mapping; `evidence/remaining_work.json` D01.

Photographed copper may legitimately connect the two alternative regulator **footprints**; electrically, only U6 is populated. The conflict arises because U106 is modeled as an active power-output IC even though unpopulated. **High confidence representation issue, not a proven short or design fault.**

**Smallest correction:** represent U106 as three passive unpopulated footprint pads, or separately flag an explicitly DNP variant that does not assert an active power-output device in ERC. Retain all three mapped copper nets. Do not delete the option or disconnect the copper.

## Seven ERC findings: disposition

| Finding | Classification | Recommended treatment |
|---|---|---|
| U1 VIN undriven | Source-model artifact *pending physical supply validation* | Model actual upstream battery/L2/passive source with an explicitly documented PWR_FLAG if justified; don't invent regulator output. |
| U1 VSS undriven | Source-model artifact | Ground has battery negative; a single well-placed power-source declaration can satisfy model semantics once grounded path confirmed. |
| U6 VIN undriven | Source-model artifact *pending supply trace* | Verify VDD–R37–H_AUX_IN and U6.2/5 tie; then model rail source appropriately. |
| U5 motor VDD undriven | Source-model artifact | Passive battery+ through Q1 to VSYS; mark battery-derived power source, preserving pre/post-Q1 separation. |
| U3 V+ undriven | **Potential real path ambiguity** | Determine receiver rail power through Q7/D3 region before declaring power drive. |
| U6.3 ↔ U106.2 two power outputs | **DNP representation**, not simultaneous fitted devices | Change U106 schematic electrical type to passive DNP copper pads; retain net mapping. |
| `H_D1_FREE` isolated label | **Actual unresolved endpoint** | Trace D1.2; do not mark NC or attach arbitrarily. |

**Before/after net-membership discipline:** Proposed DNP-symbol replacement preserves `H_AUX_IN = {U6.2,U6.5,U106.1,...}`, `H_PIR_VDD = {U6.3,U106.2,J3.1,...}`, and GND `{U106.3,...}`; only the *pin electrical type/representation* changes. All other findings above are measurement requests and **do not justify a net-membership edit yet**. A future power flag would add a source-classification element to a *confirmed existing* net, not join two nets.

## Five or fewer high-value bench checks — ordered, conditional

Before these: **agent should first trace visible surface copper** in original photos, applying already recorded user-confirmed connections and negative evidence; remove any check resolved visually. Unpowered resistance readings use a stable shorted-lead baseline, batteries disconnected and capacitors discharged. Don't use an ohmmeter on powered nodes.

1. **One Q3 tuning-cell identity/topology check — `IMG_2433`, `IMG_2442`, Q3 physical single/paired pads, R13.2, C10.1, C10.2/C11.2/C12.2, V107, ANT1/ANT2.** Check any *hidden* physical pad/via relationships left ambiguous by the photos; with an isolated device if indispensable, use directional diode tests to distinguish base from C/E (not assume diode mode uniquely distinguishes collector from emitter). **Direct low-ohm connection** identifies common copper; **OL** separates branches; diode drops suggest junction paths. This selects a physically valid transistor orientation and establishes one actual antenna connection.
2. **RF excitation hidden termination — `IMG_2431/2432`, R6.2–R7.1 (`H_RF_CONTROL`), D1.2 (`H_D1_FREE`), and nearby already-numbered vias.** Only after visual follow-up, probe R6/R7 common to one photo-selected candidate driver/antenna path, and D1.2 to its photo-selected neighbor. **~probe-baseline** = direct net; **marked-resistor-sized** = indirect path; **OL** = no direct copper. The needed candidate endpoints must come from actual image tracing; none is yet grounded enough to prescribe an exact remote PIC pad.
3. **Receiver output onward route — `IMG_2429/2434`, C23.2/R25.1 (`H_RX_DETECT`), R25.2/R47/R48 (`RX_STAGE_LINK`), and U3 outputs.** After tracing the visible metal, probe only the hidden suspected interface/via. Near-zero versus resistor-valued/OL distinguishes direct endpoint from an RC coupling path. Do **not** sweep PIC pins or reverse recorded negative evidence.
4. **S1 actual contact table, if needed for final schematic — `IMG_2438`, S1 photographed four leads.** With power disconnected read continuity on each lateral/top/bottom candidate pair **released and pressed**, documenting the four physical contacts. 0 Ω at rest identifies internally shared side; closure only when pressed identifies opposite sides. This settles the assumed switch pin mapping without retesting R41→VPP.
5. **One powered voltage/timing batch, after the above routing audit — measure BATTERY+, VSYS, VDD, VREF, U6.3/J3.1, U3.8, Q8 P-source and both gate pins at idle and during triggered RFID scan, plus U5 INA/INB pulses if a scope is available.** Compare Q8 gate minus source; look for receiver rail enable. These discriminate actual regulation/switching behavior from mistaken power-node assumptions. Use common board ground; never clip an earth-grounded scope reference onto a motor/antenna drive node.

*Note:* The first three are conditional **one-path-at-a-time** checks; no measurement request should be sent until photos establish a specific unresolved hidden endpoint. There is no justification for a bulk via sweep or measuring 44 ceramic capacitors before topology closure.

## What cannot yet be asserted

Exact fabricated layer count, actual RF resonance and individual parallel capacitor values, original programmed firmware behaviour, absolute EMI/ESD margins, and selected chip manufacturer from nonunique short codes. Seven or zero ERC findings would not prove these properties. The supplied archive covers the **main board**, not a finished PIR daughterboard reverse engineering or a routed PCB.
