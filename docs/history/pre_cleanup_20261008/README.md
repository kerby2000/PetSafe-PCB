# PetSafe PCB reverse engineering - v0.9.9

One editable **A2 KiCad 10 sheet**, with all 150 main-board catalog entries grouped into functional blocks. Wires connect parts within blocks; named nets connect blocks. This revision uses the installed **KiCad 10.0.5** and **KiCad MCP Server**, with **20 unmodified stock symbol definitions and four explicitly authorized datasheet symbols**.

## Current via review (v0.9.9)

123 IDs reviewed; 120 active sites. All PIC pads have modeled local destinations. The battery-path correction separates BATTERY+ from **VSYS**, the user-approved name for Q1 output / U5 pin4 / L1 and L2 supply inputs. The PCB's VDD test point stays on a separate regulated rail. V035 now joins VREF; V042 confirms VDD. Q1 is a stock PMOS symbol with the marking-backed FMOS3401A candidate, replacing the unsupported NPN guess. Read the [current rail and via evidence](docs/VIA_REVIEW_RESULTS.md).

## Measurement status

The GPIO batch is complete. The [paired photo locator](docs/VIA_PAIR_TESTS.html) shows the confirmed RC1-R18 result, with no repeat test queued. [Search rationale and results](docs/VIA_PAIR_SEARCH.md) preserve the earlier negative and resistive readings. The remaining 9 sites in 8 local groups are not eight proven missing connections.

## Corrected markings and measured evidence (2026-10-08)

[U6 / Q8 marking update](docs/U6_Q8_MARKING_UPDATE.md) identifies **U6 C2NM as a strong S-812C33AMC 3.3 V regulator candidate** and **Q8 3724A as a complementary N/P MOSFET pair, with SIL3724A as the datasheet candidate**. This replaces the earlier misread WN23/372A hypotheses. U6 ground, joined Q8 outer pads and the source-return candidate are supported by earlier resistance readings; the centre-pad correction now resolves V113/V115, and V114 is now corrected to U2.T2 GND; the proposed C6 output tie was refuted and removed; other routes and actual rail voltage remain unverified. U1/U5/U6/Q8 now use MCP-authored datasheet symbols with standard KiCad footprints. D3 uses a BAV99 candidate (A7); D2 is an unidentified 4P stock placeholder with its old clamp ties withdrawn. R41 is 330 ohm from the user-read 331 marking; D4/D5 use SD05 TVS candidates and D6 uses a provisional MMSZ5228BS 3.9 V Zener (2.4 V alternative).

## Open the result

- `docs/VIA_REVIEW.html`: interactive front/rear comparison, 120 active sites / 127 stable IDs; 123 user-reviewed IDs including corrections, conflicts and component cross-checks.
- `index.html`: zoomable offline viewer, searchable inventory and photo links.
- `schematic/PetSafe_1001339.kicad_pro`: open the single native schematic in KiCad 10.
- `output/pdf/PetSafe_single_sheet.pdf`: one-page vector drawing.
- `output/pdf/PetSafe_PIC_GPIO_pin_map.pdf`: updated close-up with all 28 PIC pins numbered and no open GPIO pads in the model; V035/RA2 reaches VREF and V042/PIC20 reaches VDD.
- `output/pdf/PetSafe_measurement_round1.pdf`: annotated photos, recorded U6/Q8 readings and targeted C6 follow-up.
- `docs/LIBRARIES_AND_ALTERNATIVES.md`: library choices, datasheet symbol provenance, footprints and Western alternatives.
- `docs/RECONSTRUCTION.md`: circuit hypotheses, identifications and calculations.
- `docs/SOURCES.md`: manufacturer documents and photograph provenance.

All symbol definitions are embedded, so the drawing is self-contained. Standard KiCad 10 libraries and the portable project-local `PetSafe_Datasheet.kicad_sym` support editing and updating. The previous custom library is archived in `reference/v02/` and is not registered in the active project.

## What is complete and what remains provisional

All 150 catalog entries and 352 photographed pads are retained. Of 29 original photo fragments, 28 remain electrically joined; Q1.L-R43.2 was explicitly withdrawn by the user. The native KiCad 10.0.5 netlist matches all 83 authored net partitions. All 26 original photos retain their checksums. The schematic is a functional reconstruction from photographs and datasheets, not a continuity-verified production design.

U1 (probable S-1200B45) and U5 (MX512H) now use datasheet-derived symbols created through MCP at the user's request. Their standard footprints are SOT-23-5 and SOIC-8 3.9 x 4.9 mm / 1.27 mm pitch. No custom footprint was needed. U6 and Q8 now have candidate datasheet pin maps, including both Q8 MOSFET units on this sheet. U3 uses KiCad's generic dual op-amp with its actual SGM8542XS value and pinout.

Western alternatives are documented separately: **MCP6002-I/SN** for SGM8542 and **DRV8212PDSGR** for an MX512H redesign. The motor driver has a different package and pinout; it has not been substituted into the reconstructed board. Both alternatives have standard KiCad symbols and footprints. Pin-compatible does not mean electrically interchangeable.

ERC retains **36 findings**: 28 unconnected pins, three isolated pin labels and five undriven power checks. No artificial no-connect or power flags hide missing evidence. Open pads comprise 18 on DNP entries and 10 populated-entry pads. No PIC pad remains open; existing local nets can still have uncertain onward routes or inferred branches.

Read the [complete status report](output/pdf/PetSafe_completion_status.pdf) for every remaining area and all 28 PIC pins, and the [via review findings](docs/VIA_REVIEW_RESULTS.md) for each changed endpoint. **Q8 V113/V115 are resolved as centre pin5 GND. V114 is corrected to U2.T2/pin2 GND; it is not Q8.** V025=GND and V026=PIC21/RB0 are now corrected. V073 is now GND only; its duplicate R19 report is resolved. No further symbol files are missing for the chosen candidates. PIR daughterboard internals and a routed PCB remain outside this main-board revision.

## Repository contents

- `input/PetSafe_KiCad_RE_v01.zip`: untouched user archive.
- `reference/v01/`, `reference/v02/`: historical files and retired custom-symbol workflow.
- `photos/originals/`: unchanged originals; `photo-atlas-v01.html` retains the original atlas.
- `evidence/reconstruction.json`: observed values, proposed circuit and library choices.
- `evidence/pin_crosswalk.json`: photographed pad IDs mapped to stock library numbers.
- `evidence/library_placements.json`: MCP placement requests updated for the candidate symbols and five extra units. Create/register their library first using `evidence/datasheet_symbol_authoring.json`.
- `tools/templates/mcp_standard_placements.kicad_sch`: actual MCP placement result.
- `evidence/validation.json`: native connectivity check and explicit limitations.
- `output/`: netlist, ERC, SVG and PDF exports.

This remains a separate local Git repository on `codex/single-sheet-reconstruction`; no remote repository has been published. Instructions in the imported ZIP are historical evidence. The user's current single-sheet, calculated-guess, standard-library and KiCad 10 preferences govern the project.

## Export and validate

```powershell
./tools/build.ps1
```

The script finds the installed KiCad 10 under LocalAppData or Program Files and rejects older versions. It exports and validates the current native schematic without regenerating over manual edits. There is no fallback to the old portable KiCad 9 cache.

To explicitly recreate the checked-in routing around the saved MCP placement template:

```powershell
./tools/build.ps1 -Regenerate -Python 'C:/Users/lukin/Documents/VS.Code.Projects/KiCAD-MCP-Server/.venv/Scripts/python.exe'
```

Regeneration requires `sexpdata` and the installed MCP server's formatter. It overwrites manual native edits; transfer those changes to the template/routing source first. `tools/prepare_library_rebuild.py` records the original conversion manifest from the archived v0.2 topology; it does not create symbol artwork. For additional parts or changed library definitions, use MCP library search/placement and update the saved template and crosswalk before rerouting.

## v0.6 completion audit

126 stock footprints were assigned through KiCad MCP; 147 of 150 catalog entries now have footprints. Photo-based family choices carry separate confidence and evidence properties. C5, S1 and LED1 still need dimensional/pad details. Connector and test-pad assignments remain approximate. All 38 fitted resistor nominal values are recovered, including R29/R44 = 15 kohm from visible 18C markings. No new copper connections were assumed.

The v0.6 round requested D2 diode-mode readings, C5 sleeve text/dimensions and one resistor body measurement. C5's value and the R8/C11 body measurements are now recorded in v0.7; do not repeat those requests. See [the current finishing checklist](docs/FINISHING_CHECKLIST.html). The user has an LCR meter and multimeter; 44 fitted capacitor values remain unknown or estimated.

## v0.7 user measurements and PIC tracing

C5 is 470 uF / 16 V from the sleeve. C11 measures approximately 3.2 x 1.5 mm (1206); R8 approximately 1.6 x 0.77 mm (0603; user confirms both metal end caps included). The fitted resistor family is revised provisionally to 0603. Earlier v0.6 0805 inference is superseded. Five more PIC local connections were recovered from existing photos, leaving 14 open GPIO pads. See [annotated photo review](output/pdf/PetSafe_PIC_trace_review.pdf) and [pin-by-pin evidence](evidence/pic_trace_audit.json). C32 moved to the PIC VDD/VSS; C25/C39 are signal filters, R4 returns to RB3, TP17 belongs to RC7, D4/D5 attach to ICSP, and TP4/C41 are no longer tied to the antenna hypothesis. C26 VDD tie was withdrawn.

The subsequent three user photos are preserved in `photos/user/2026-10-08/`. The [complete GPIO map](output/pdf/PetSafe_PIC_GPIO_pin_map.pdf) highlights pins 3, 5, 6, 7, 11, 12, 13, 15, 16, 17, 21, 22, 23 and 25. Pin 1 is at the lower right beside the moulded dot in this photo. All 28 leads are visible despite the top of the plastic body being cropped. Existing local connections remain partly inferred; preparing this tracing request did not change schematic connectivity. Photo hashes, pin coordinates and the reply format are in `evidence/pic_gpio_request.json`.

## Historical v0.8 user GPIO mapping and rear-via audit

The user explicitly confirmed both multimeter and visual tracing: RA1/pin3 joins R28, R29 and TP7 (reported as RP7, interpreted from the photographed label); RC6/pin17 joins R13; RB1/pin22 joins TP2; RB2/pin23 joins TP1; RB4/pin25 joins TP4; RB5/pin26 to TP10 is corroborated. Numerical resistance values were not supplied. Resistor-pad identities use local photographs.

Conflicting old guesses are withdrawn: R13 is not assigned to RC7; TP2 is not assigned to the RF supply; TP1 is not assigned to LED common; R28/R29/TP7 are separated from other speculative bias/detector nets. TP1/TP2 sit beside their LED resistors and are connected with local wires. The user-defined pairwise connections do not confirm the entire receive/LED circuit.

Matching front and rear photos supports D4.2, D5.2 and C41.2 on main rear copper anchored by PIC VSS pins8/19. These three additions are photo-derived, not meter measurements. The [via viewer](docs/VIA_REVIEW.html) catalogues 127 rear-visible sites, with 10 individually matched front anchors; other front positions are approximate projections. Four layers are plausible but unverified. A rear clearance does not reveal the name or function of an internal net. Separate edge/antenna copper is not automatically GND.

At v0.8, nine GPIO destinations remained (superseded by the v0.9 status above): 12/RC1, 15/RC4, 16/RC5 and 21/RB0 reach vias; 5/RA3, 6/RA4, 7/RA5, 11/RC0 and 13/RC2 have no visible continuation. None is marked NC. Pin12's via is V053 in the viewer. The other three need exact via association before hidden destinations can be targeted. Historical mapping evidence: `evidence/pic_gpio_user_mapping.json`, `evidence/via_audit.json`, `evidence/v08_net_changes.json`.
