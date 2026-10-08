# PetSafe PCB reverse engineering - v0.6

One editable **A2 KiCad 10 sheet**, with all 150 main-board catalog entries grouped into functional blocks. Wires connect parts within blocks; named nets connect blocks. This revision uses the installed **KiCad 10.0.5** and **KiCad MCP Server**, with **20 unmodified stock symbol definitions and four explicitly authorized datasheet symbols**.

## Corrected markings and measured evidence (2026-10-08)

[U6 / Q8 marking update](docs/U6_Q8_MARKING_UPDATE.md) identifies **U6 C2NM as a strong S-812C33AMC 3.3 V regulator candidate** and **Q8 3724A as a complementary N/P MOSFET pair, with SIL3724A as the datasheet candidate**. This replaces the earlier misread WN23/372A hypotheses. U6 ground, joined Q8 drains and the N-source return are supported by resistance readings; the proposed C6 output tie was refuted and removed; other routes and actual rail voltage remain unverified. U1/U5/U6/Q8 now use MCP-authored datasheet symbols with standard KiCad footprints. D3 uses a BAV99 candidate (A7); D2 is an unidentified 4P stock placeholder with its old clamp ties withdrawn. R41 is 330 ohm from the user-read 331 marking; D4/D5 use SD05 TVS candidates and D6 uses a provisional MMSZ5228BS 3.9 V Zener (2.4 V alternative).

## Open the result

- `index.html`: zoomable offline viewer, searchable inventory and photo links.
- `schematic/PetSafe_1001339.kicad_pro`: open the single native schematic in KiCad 10.
- `output/pdf/PetSafe_single_sheet.pdf`: one-page vector drawing.
- `output/pdf/PetSafe_measurement_round1.pdf`: annotated photos, recorded U6/Q8 readings and targeted C6 follow-up.
- `docs/LIBRARIES_AND_ALTERNATIVES.md`: library choices, datasheet symbol provenance, footprints and Western alternatives.
- `docs/RECONSTRUCTION.md`: circuit hypotheses, identifications and calculations.
- `docs/SOURCES.md`: manufacturer documents and photograph provenance.

All symbol definitions are embedded, so the drawing is self-contained. Standard KiCad 10 libraries and the portable project-local `PetSafe_Datasheet.kicad_sym` support editing and updating. The previous custom library is archived in `reference/v02/` and is not registered in the active project.

## What is complete and what remains provisional

All 150 catalog entries, 352 photographed pads and 29 original visual fragments are retained. The native KiCad 10.0.5 netlist matches all 81 authored net partitions. All 26 original photos retain their checksums. The schematic is a functional reconstruction from photographs and datasheets, not a continuity-verified production design.

U1 (probable S-1200B45) and U5 (MX512H) now use datasheet-derived symbols created through MCP at the user's request. Their standard footprints are SOT-23-5 and SOIC-8 3.9 x 4.9 mm / 1.27 mm pitch. No custom footprint was needed. U6 and Q8 now have candidate datasheet pin maps, including both Q8 MOSFET units on this sheet. U3 uses KiCad's generic dual op-amp with its actual SGM8542XS value and pinout.

Western alternatives are documented separately: **MCP6002-I/SN** for SGM8542 and **DRV8212PDSGR** for an MX512H redesign. The motor driver has a different package and pinout; it has not been substituted into the reconstructed board. Both alternatives have standard KiCad symbols and footprints. Pin-compatible does not mean electrically interchangeable.

ERC retains **86 findings**: 65 unconnected pins, 14 isolated pin labels, five undriven power checks and two undriven motor-control inputs. There are no off-grid endpoints or dangling wire ends. No artificial no-connect or power flags hide missing evidence. The 65 open pads include 27 on DNP entries and 38 others, including two internally open U6 pins with unresolved external ties. Exact GPIO assignments, some filter routes/values and candidate identities remain open. PIR daughterboard internals and a routed PCB are outside this revision.

See [remaining completion items](docs/RECONSTRUCTION.md#remaining-completion-items-v05). No further symbol files are needed for the current chosen candidates; a complete hardware-verified circuit still requires resolving hidden wiring and values.

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

See [the searchable finishing checklist](docs/FINISHING_CHECKLIST.html) and [the next annotated checks](output/pdf/PetSafe_next_checks.pdf). The user has an LCR meter and multimeter. Start with the six D2 diode-mode readings, C5 sleeve text/dimensions and one resistor body measurement; use small LCR rounds afterward. All 45 fitted capacitor values remain unknown or estimated.
