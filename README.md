# PetSafe PCB reverse engineering - v0.2

One editable KiCad sheet with all 150 entries from the main-board catalog, arranged into functional blocks. Components are wired within each block; net names connect blocks. Identities, values and routes inferred from photographs and datasheets are explicitly marked as hypotheses.

## Open the result

- **`index.html`**: offline viewer with zoom, searchable parts and photo links.
- **`schematic/PetSafe_1001339.kicad_pro`**: native project, validated with KiCad 9.0.7. Open its single schematic.
- **`output/pdf/PetSafe_single_sheet.pdf`**: one-page A0 vector schematic; zoom for individual circuits.
- **`docs/RECONSTRUCTION.md`**: identifications, assumptions, alternate circuits and calculations.
- **`docs/SOURCES.md`**: manufacturer references and source-photo map.

The local symbol library is included and the symbols are embedded. There are no active child sheets. No external library installation is needed to display the circuit.

## Useful findings

U1's PPEK marking strongly matches the ABLIC S-1200B45 4.5 V regulator: the manufacturer maps PPE to the device and the fourth character to a lot code. U2's C14R marking and six leads strongly match the TI SN74LVC2G14 dual Schmitt inverter. The known PIC16F18855, SGM8542 and MX512H are organized into recognizable application circuits. Q8 and U6 remain the principal device-identity uncertainties.

All 29 local visual net fragments from v0.1 are retained. The new native netlist matches all 81 authored net partitions without unintended merges. All 26 original photos match their supplied SHA-256 checksums.

**Electrical status:** this is a working reconstruction, not a continuity-verified circuit. ERC retains 84 findings: 63 unconnected pins, 14 one-ended signal labels, five undriven power checks and two undriven inputs. Exact PIC GPIO mapping, Q8 power pads, U6 identity, capacitor values and several filter/clamp routes remain unresolved. The 150 entries include DNP footprints, pads and test points. PIR daughterboard internals and a routed PCB are not part of this revision.

## Repository contents

- `input/PetSafe_KiCad_RE_v01.zip`: untouched supplied archive.
- `reference/v01/`: historical capture, generators, evidence and instructions.
- `photos/originals/`: unchanged originals; existing registered mosaics retained under `photos/`.
- `photo-atlas-v01.html`: historical photo atlas, clearly labeled as v0.1.
- `evidence/reconstruction.json`: current proposed model, raw observed values and original fragments.
- `evidence/components.csv`, `proposed_nets.csv`, `unresolved_pins.csv`: review tables.
- `evidence/validation.json`: native tool results and explicit limits.
- `output/`: native netlist, ERC, SVG and PDF.

This is a separate local Git repository, initially committed from the archive and then revised on `codex/single-sheet-reconstruction`. The imported documents are evidence and historical context. The user's request for calculated guesses and a single sheet governs this revision.

## Rebuild

Use Python 3 (standard library) and KiCad CLI 9.0.7 or compatible:

```powershell
./tools/build.ps1 -KiCadCli 'C:/Program Files/KiCad/9.0/bin/kicad-cli.exe'
```

The local task also has an ignored portable CLI under `.cache/`; it is not part of the shared project. `tools/single_sheet.py` authors the circuit and layout. `tools/validate_native.py` compares native KiCad connectivity and checks source preservation. `tools/build_review.py` refreshes the offline viewer and inventory.

Do not regenerate over manual KiCad edits without transferring those changes to the generator. Original photo-processing tools are retained separately from the new schematic workflow.
