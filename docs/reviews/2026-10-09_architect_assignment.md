# PetSafe PCB: review and focused finishing task

**Repository:** kerby2000/PetSafe-PCB  
**Reviewed baseline:** 522d235bfc9cd1973c41746033a9c38277aa4736 (main at review time)  
**Board:** PetSafe PPA19-16811, 100-1339 R03 A  
**Review date:** 2026-10-09

## Scope and limitations

This is an independent static review of the checked-in evidence, proposed nets, physical-to-native pin map, selected native XML net definitions, current documentation, and verification code. Relevant original PCB photographs and primary component datasheets were also examined. KiCad was not available in the review environment: native export/ERC, the complete build and the physical board were not independently exercised. No repository files were changed or pushed by this review.

The distinction between measured evidence, photographic interpretation, candidate identities and unresolved routes is valuable and should be preserved. Model/native agreement is useful but does not independently prove the physical circuit. No routed PCB is currently documented.

## A. Corrections that need little or no new bench work

### A1. Reconcile J1 physical positions and numbered footprint pads

Sources: `evidence/pin_crosswalk.json`, `output/PetSafe_netlist.xml`, `docs/LIBRARIES_AND_ALTERNATIVES.md`, original `IMG_2437.jpg` and rear `IMG_2439.jpg`.

The photographed contact order, left-to-right in IMG_2437, is:

`CLK — DAT — GND — VDD — VPP`

The current native pin mapping is:

`1 CLK; 2 DAT; 3 VPP; 4 VDD; 5 GND`.

This is not simply reversed numbering. Ground must occupy the middle position of a sequential five-pad footprint in either orientation. It cannot be the end contact, as native pin 5 currently implies. The library document acknowledges logical numbering; this needs resolution before any PCB transfer or numbered programming-cable instruction.

Identify the physical pin-1/square-pad end from the existing images. If the VPP end is pin 1, the numbered mapping is 1 VPP, 2 VDD, 3 GND, 4 DAT, 5 CLK. If the other end is deliberately numbered pin 1, use 1 CLK, 2 DAT, 3 GND, 4 VDD, 5 VPP. Use one convention consistently in crosswalk, footprint, symbol and exports. Do not change logical electrical destinations merely to renumber the connector.

Acceptance: every native J1 pin agrees with a documented physical position and the selected footprint. Keep the distinction between photograph-supported position and meter-confirmed electrical route.

### A2. Separate frozen cleanup checks from live completion checks

Sources: `tools/verify_current_review.py`, `tools/verify_v099_review.py`, `tools/refresh_review.ps1`.

The refresh pipeline currently runs checks that require:

- every issue state to remain `open`;
- 83 modeled nets and 36 ERC findings;
- 28 unresolved pads / unchanged unresolved-pad count relative to the pre-cleanup snapshot;
- every fitted capacitor except C5 to remain an unknown ceramic value.

Those are appropriate snapshot assertions for a documentation-only cleanup, but block legitimate finishing work when run as current-state requirements.

Retain the historical cleanup test as a baseline/snapshot test. For the current project, compare derived counts with current model/export data, not historical constants. Permit issue closure with a recorded result and evidence. Apply unresolved-pad coverage to active issues; retain closed issues as history. Derive the unknown-value list from component records. Preserve actual measured same-net/different-net assertions and explicit rejected connections.

Keep this small: adapt the existing validators rather than create a new verification framework. Exercise at least an issue closure and a capacitor-value update without destroying the historical record. Do not silence assertions by changing hardware hypotheses solely to satisfy them.

### A3. Remove a directional assumption from the button investigation

Sources: `evidence/proposed_nets.csv`, `evidence/remaining_work.json`, E05.

In the present model, S1/H_BUTTON already reaches PIC pin 28 through R40. The singleton `H_BUTTON_MCU` is R41.1, but its name and E05's instruction to search toward the MCU are not evidence that it is another MCU connection. It might instead be a supply, bias or other control connection.

Rename the unresolved node neutrally, or clarify its description. Review the short R41 route and likely supply/control destinations before asking Sergey to probe all PIC pins. Do not replace the uncertainty with an assumed pull-up.

## B. Circuit consistency findings: investigate, do not auto-correct

### B1. U3 pin 5 has no modeled DC bias-current return

Sources: `evidence/proposed_nets.csv` (`RX_B_PLUS`), `output/PetSafe_netlist.xml` (net `Net-(U3B-+)`).

The native net contains exactly U3.5 and C18.1. C18's other side is on the separate TP6/R27 branch. Consequently there is no intentional DC return from this non-inverting op-amp input in the captured circuit. A normal capacitively coupled linear amplifier requires a defined bias mechanism; this capture does not yet show one.

This is a strong reconstruction warning, not proof of a defective original board. Locate the missing bias route, correct a mistaken pad assignment, or establish/document an intentional nonstandard operating mechanism. Do not add an invented resistor to make simulation plausible. Preserve the confirmed separation across C18.

Next check: use the existing photos/vias around U3.5, then target its connection to specific existing bias-resistor pads. Record a resistor-valued path to VREF separately from direct copper continuity.

### B2. Five tuning cells are not yet a working antenna network

Sources: `evidence/proposed_nets.csv`, `evidence/pin_crosswalk.json`, library choices, E04.

As captured, Q3/Q4/Q5/Q6/Q11 are PNPs with emitter pin 2 on GND, base pin 1 driven through a resistor from a PIC pin, and collector pin 3 feeding a capacitor. With ordinary nonnegative GPIO drive and the emitter at GND, this is not the usual forward-operated PNP-switch arrangement. Independently, the five capacitor midpoints do not connect to an antenna node in the current model; ANT2 has no onward modeled route.

Possible explanations include an incorrect ground association, mistaken physical transistor orientation/type, or an RF junction-switching arrangement not represented by the current interpretation. Do not change all five symbols to NPN based only on plausibility. A short marking is not unique, and a diode-mode identification of the base alone does not necessarily distinguish emitter from collector.

Finish ONE cell first, preferably Q3/C10/C11/C12: physically map the transistor pads, the three capacitor terminals on both board sides, and the actual antenna continuation. Then use symmetry to propose short checks for the other four cells. Preserve the seven recorded OL exclusions; do not repeat the broad midpoint sweep.

### B3. Several important functional signals stop locally

Sources: `evidence/proposed_nets.csv`, native XML export.

| Modeled net | Current members / missing function |
| --- | --- |
| H_RF_CONTROL | R6.2 and R7.1 only; no excitation source is modeled. |
| H_RX_DETECT | C23.2, C40.1 and R25.1 only; no detection input destination is modeled. |
| H_PIR_SIG | Q2.S and TP16.1 only; no controller input is modeled. |
| H_BAT_SENSE | R3.2, R4.1 and C28.1 only; no sampling destination is modeled. |

Some labels may themselves be wrong; require a documented functional explanation rather than blindly adding an MCU endpoint. A pin can be connected to a capacitor/test point and still have a missing onward route. Add these checks to the relevant existing issues, not a separate large process.

### B4. Q8 gate-drive headroom depends on unresolved rail voltages

Sources: proposed nets, native pin crosswalk, SIL3724A manufacturer datasheet and TI SN74LVC2G14 datasheet.

The model places Q8's P-channel source (native 2) on the L1-filtered VSYS branch. Its gate (native 3) is driven from U2 output 4 through R8. U2 is modeled on regulated VDD.

Illustration only: if the source is 6.0 V while the high gate level is 4.5 V, VGS is -1.5 V. The candidate SIL3724A datasheet specifies P-channel threshold magnitudes spanning approximately 1.0 to 2.5 V, measured at a small drain current. Therefore -1.5 V is not a guaranteed off condition. This does not establish cross-conduction in the actual product; fitted identity, actual source voltage, supply routing or operating waveform may differ from the assumptions.

After the passive routing checks, measure VDD, Q8 source voltage and the gate high/low waveform during scanning. Measure both gate and source relative to PCB GND, then compute VGS. Do not put an earth-referenced scope ground clip on a driven motor or antenna terminal. Do not infer turn-off from gate-to-ground voltage alone.

## C. Highest-value next measurements

Use the original hardware and supplies unchanged. Disconnect all power/programmers and allow capacitors to discharge for continuity/diode/LCR work. Use the established photo pad labels as well as numeric pin assignments where the device identity is still provisional.

1. D3/V082: measure V082 to each of D3's three physical pads. This localizes the confirmed VDD association without guessing which receiver net to merge. D2's existing directed diode-mode tests remain appropriate if not already completed.
2. U3.5: find its DC-bias path or a missing branch to existing components; do not short across C18.
3. J3: establish which of pins 2 and 3 is ground by continuity, then trace the Q2/TP16 signal onward. Wire colour alone is not evidence.
4. One complete tuning cell: resolve topology and transistor pad functions before measuring all five capacitance groups.
5. R41's free end, H_RF_CONTROL, H_RX_DETECT and H_BAT_SENSE: use existing via/photo evidence to choose specific candidate endpoints, rather than a large unstructured scan.
6. Following routing reconciliation: one powered session to measure BATTERY+, VSYS, VDD, VREF, U6 output, Q8 source/gates and the two U5 control inputs. Record idle and a triggered scan; the receiver supply may be switched.

Do not redo established positive/negative tests simply because another generated report omitted them. A stable nonzero resistance is not automatically a direct net: ferrite beads, inductors, resistors, transistor junctions and contact resistance require interpretation.

## D. Capacitor values and footprints: finish efficiently

There are two legitimate milestones, not one ambiguous completion percentage:

**Topology complete:** populated components and functional block interfaces have supported connections; unresolved candidate identities/polarities are reduced to compatible functions; remaining exceptions are individually documented.

**Value/package complete:** required component values and physical geometry are recovered; unresolved manufacturer/ratings are clearly differentiated from electrically equivalent design choices. A routed PCB is a separate deliverable.

First measure frequency-sensitive components: the verified tuning cells, RF drive shaping and receiver coupling/feedback filters. Measure general bypass values afterward. Do not copy a common 100 nF value onto every unmarked ceramic.

The present model places C11 and C12 in parallel, with the same pair of nodes. An in-circuit LCR reading would then give a network value, not each individual capacitor. If that topology is confirmed, one branch measurement can establish an effective capacitance; separate individual values only when needed for faithful BOM reproduction. Isolate a terminal only where necessary and retain which frequency/mode/amplitude and in-circuit/isolation condition was used. Other parallel groups require the same treatment. Do not allocate an assumed split of a measured sum.

Do not spend the next session perfecting C5/S1/LED1 footprints before the main signal paths. These dimensions matter for physical reproduction, but cannot repair an incomplete receiver or antenna circuit. The current 147 assigned footprints are family candidates, not 147 verified land patterns.

## E. Review completion and suggested deliverables

Use a review branch and preserve main; the current request was for review, not a remote write. Follow the user's repository working rules and preserve local project/history files.

Deliver a small corrective change with A1-A3 addressed, the B findings attached to existing issues with specific evidence-based next checks, a fresh native export/ERC and updated current-state counts. Keep unknown physical connections unresolved until measurements or unambiguous photographic copper support the edit. The ERC total should decrease because real gaps close, not because unknown pins are marked intentional no-connects. Documented power-source declarations/waivers are appropriate only once the actual supply path is established.

Do not replace the PIC, change batteries or redesign the RF front end as part of this finishing task.

## Source locations

Pinned repository baseline:
`https://github.com/kerby2000/PetSafe-PCB/tree/522d235bfc9cd1973c41746033a9c38277aa4736`

Primary component documents consulted:
- MCC SIL3724A manufacturer PDF, mirrored at `https://static.chipdip.ru/lib/761/DOC050761871.pdf` (pin diagram and P-channel threshold table).
- TI SN74LVC2G14: `https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf`.
- Nexperia PBSS5140T: `https://assets.nexperia.com/documents/data-sheet/PBSS5140T.pdf` (existing alternative 2H-marked PNP candidate, not a new fitted-part identification).

The repository's other primary sources, measured exclusions and candidate boundaries remain authoritative project evidence. This review adds reasoning and proposed checks, not new bench measurements.
