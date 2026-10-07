# PetSafe PCB reverse engineering - v0.3

One editable **A2 KiCad 10 sheet**, with all 150 main-board catalog entries grouped into functional blocks. Wires connect parts within blocks; named nets connect blocks. This revision uses the installed **KiCad 10.0.5** and **KiCad MCP Server**, with **22 unmodified stock symbol definitions and zero custom symbols**.

## Follow-up investigation (2026-10-08)

[U6 / Q8 investigation](docs/U6_Q8_INVESTIGATION.html) ranks RT9818A-33PB as U6's leading named candidate and a complementary MOSFET pair as Q8's leading circuit role. It documents the mirrored U6 placeholder numbering, conditional Q8 pin map, and standard-library Western comparison parts. The native v0.3 circuit remains unchanged; H14 must not be treated as an established LDO circuit. U1/U5 vendor files or links are still pending.

## Open the result

- `index.html`: zoomable offline viewer, searchable inventory and photo links.
- `schematic/PetSafe_1001339.kicad_pro`: open the single native schematic in KiCad 10.
- `output/pdf/PetSafe_single_sheet.pdf`: one-page vector drawing.
- `docs/LIBRARIES_AND_ALTERNATIVES.md`: library choices, missing-symbol requests, footprints and Western alternatives.
- `docs/RECONSTRUCTION.md`: circuit hypotheses, identifications and calculations.
- `docs/SOURCES.md`: manufacturer documents and photograph provenance.

Stock symbols are embedded, so the drawing displays without a custom library. Standard KiCad 10 libraries support editing and updating. The previous custom library is archived in `reference/v02/` and is not registered in the active project.

## What is complete and what remains provisional

All 150 catalog entries, 352 photographed pads and 29 original visual fragments are retained. The native KiCad 10.0.5 netlist matches all 81 authored net partitions. All 26 original photos retain their checksums. The schematic is a functional reconstruction from photographs and datasheets, not a continuity-verified production design.

U1 (probable S-1200B45) and U5 (MX512H) use explicitly numbered stock placeholders pending vendor/SnapEDA symbols. U6 and Q8 remain unidentified numbered placeholders. No missing custom symbols were fabricated. U3 uses KiCad's generic dual op-amp with its actual SGM8542XS value and pinout.

Western alternatives are documented separately: **MCP6002-I/SN** for SGM8542 and **DRV8212PDSGR** for an MX512H redesign. The motor driver has a different package and pinout; it has not been substituted into the reconstructed board. Both alternatives have standard KiCad symbols and footprints. Pin-compatible does not mean electrically interchangeable.

ERC retains **80 findings**: 63 unresolved pins, 14 isolated pin labels and three undriven power checks. There are no off-grid endpoints or dangling wire ends. Placeholder pins are passive, so they provide less electrical checking than exact IC symbols. No artificial no-connect or power flags hide missing evidence. Exact GPIO assignments, some filter routes/values and several device identities remain open. PIR daughterboard internals and a routed PCB are outside this revision.

## Repository contents

- `input/PetSafe_KiCad_RE_v01.zip`: untouched user archive.
- `reference/v01/`, `reference/v02/`: historical files and retired custom-symbol workflow.
- `photos/originals/`: unchanged originals; `photo-atlas-v01.html` retains the original atlas.
- `evidence/reconstruction.json`: observed values, proposed circuit and library choices.
- `evidence/pin_crosswalk.json`: photographed pad IDs mapped to stock library numbers.
- `evidence/library_placements.json`: replayable MCP component placement requests.
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
