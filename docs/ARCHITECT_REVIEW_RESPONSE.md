# Architect review response - 2026-10-09

Baseline: 522d235. Local review branch: `codex/architect-review-522d235`. The supplied [assignment](reviews/2026-10-09_architect_assignment.md) is review evidence; no new bench readings are implied. Main and the remote are preserved.

## Corrections

| Finding | Action / evidence |
|---|---|
| A1 - J1 physical numbering | IMG_2437 clearly shows CLK-DAT-GND-VDD-VPP left-to-right and the square pad at VPP. IMG_2439 corroborates the square end. Stock header now maps **1 VPP, 2 VDD, 3 GND, 4 DAT, 5 CLK**. Crosswalk, stock-symbol wiring, MCP metadata, footprint basis and exports agree. Logical destinations are unchanged. This establishes photograph-supported position, not new measured continuity. |
| A2 - frozen checks in live workflow | The original cleanup tests/reports are preserved in `docs/history/cleanup_522d235/`; `verify_cleanup_snapshot.py` reads the pinned Git baseline. Current checks derive counts from current model/export data, permit evidence-backed closure, and use per-component value evidence. In-memory tests exercise closure and a recovered individual capacitor value without writing fictitious measurements. Measured positive/negative constraints remain checked. |
| A3 - button direction assumption | Renamed R41's unresolved node **H_R41_FREE**. S1/H_BUTTON already reaches PIC28 through R40. E05 now starts with the short R41 route and selected supply/bias/control candidates; it neither assumes another MCU connection nor adds a pull-up. |

## Circuit findings retained as unresolved work

| Finding | Assessment and existing issue |
|---|---|
| B1 - U3.5 DC return | Confirmed as a model inconsistency warning: RX_B_PLUS contains U3.5 and C18.1 only. E08 now prioritizes the nearby R23/R22 bias-facing pads and a separate resistance measurement to VREF. No new resistor or C18 short added. |
| B2 - tuning topology | Confirmed concern: current PNP emitter-to-GND interpretation does not describe ordinary GPIO-controlled forward PNP switching, and capacitor midpoints/ANT2 have incomplete continuations. E04 prioritizes one complete Q3 cell, preserving all seven OL exclusions. No transistor-type substitution made. |
| B3 - local functional endpoints | RF excitation, receiver detector output and PIR output lack modeled source/destinations; added to E06/E08/E07. **Qualification:** H_BAT_SENSE already reaches PIC24 through R4/PIC_RB3_RETURN. Its mechanism and photo-route confidence remain uncertain, but an extra MCU wire is not warranted by the net-member list. |
| B4 - Q8 gate headroom | Valid conditional warning, added to E03/E09. Actual source/gate voltages are unmeasured. The candidate's threshold does not guarantee turn-off for the illustrative -1.5 V case, nor does that example prove cross-conduction in this product. |

The [MCC SIL3724A datasheet](https://static.chipdip.ru/lib/761/DOC050761871.pdf), page 3, specifies P-channel threshold at -250 uA with magnitude 1.0 to 2.5 V. The [TI SN74LVC2G14 datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf) defines the logic driver's supply/output behavior. These support the conditional headroom check, not fitted-part identity or actual operating voltages.

## Efficient next session

Disconnect power/programmer and discharge capacitors for continuity, diode and LCR work. Keep the original hardware/supplies. Do not repeat accepted or rejected pairs simply because a report changes.

1. **D3/V082 completed during this review:** user measured D3.L to GND and D3.R to VDD through V082. D3.S to R42 reads 1.2 ohm (resistor end not explicitly named; the photo selects pad2). E02 is closed with the [measurement record](../evidence/d3_measurement_20261009.json); do not repeat these checks. D2's separate diode guide remains outstanding.
2. **U3.5:** inspect V079/V080 and IMG_2434; check the VREF-facing R23.2 and R22.2 pads, then measure resistance to VREF separately. A resistor-valued path is not a direct net. Check R48 only if those results/photo traces warrant it.
3. **J3:** confirm which of pins 2/3 is GND, then trace Q2/TP16 onward. Colour alone is insufficient.
4. **One tuning cell:** Q3 physical pads, C10/C11/C12 both sides, V107 and antenna continuation. Resolve topology before individual capacitances. Diode-mode base identification alone need not resolve collector/emitter.
5. **Other endpoints:** use photos to choose specific R41, RF excitation and detector-output destinations; review the existing R3/R4/PIC24 path functionally.
6. **After routing:** one idle/triggered-scan powered session for BATTERY+, VSYS, VDD, VREF, U6 output, Q8 source/gates and U5 control inputs. Gate waveforms need a scope if available; measure against PCB GND, compute VGS, and never clip an earth-referenced scope ground to a driven antenna/motor terminal.

The [live checklist](FINISHING_CHECKLIST.html) holds all details and closure criteria. Separate topology completion from value/package completion. Prioritize verified tuning/RF/receiver network values over bypass values or the last three footprints. Record LCR frequency, mode, amplitude and isolation condition. If C11/C12 parallel topology is confirmed, an effective network value may suffice initially; do not invent a split for the BOM.

## Validation

Fresh KiCad 10 native exports, ERC, model/physical-pin comparison, stock footprints, measured electrical constraints, active-issue coverage and synthetic progress cases are run for this review. See `evidence/current_review_verification.json` and `evidence/live_evidence_verification.json` for current results. J1 numbering and R41 naming do not close unknown physical connections, so no artificial ERC decrease is expected. Original photos/ZIP and local project/history files are preserved.

## Subsequent user measurement in the same session

The architect corrections were committed locally as `bdba9b6`. The user then resolved D3's rail terminals. Revision v0.9.11 moves **only D3.R** from H_RX_VDD to VDD; the op-amp supply remains separate. D3.S-to-R42 is now supported by a 1.2 ohm component-level reading, with the exact R42 end still selected from IMG_2434. R42's other end already reaches TP4/PIC25. `H_D3_SIGNAL` replaces the overly specific `H_RX_RF_SENSE` name. Its role is not measured.

The [Nexperia BAV99 pin table](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf), page 2, makes a GND/signal/VDD clamp consistent with the selected candidate and these connections. This is functional inference, not a new fitted-manufacturer identification. The closed E02 record remains visible; E06/I01 retain signal-function/identity questions.
