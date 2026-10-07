# PetSafe 100-1339 R03 A — reverse engineering v0.1

## What this package is

A photographic atlas, a native KiCad **initial capture**, an observed-part inventory, and a targeted continuity worksheet for Sergey's PetSafe PPA19-16811. It is **not a complete or electrically verified schematic** and is not a manufacturable replacement-board design.

Open `index.html` for the photographs and searchable inventory. Open `schematic/PetSafe_1001339.kicad_pro` in KiCad (8 or later is the intended target), then the root schematic. Symbols are embedded and also supplied as a local symbol library. There are six child sheets. No external symbol library is required to display the captured symbols.

## Current evidence

- 150 catalog entries: observed designators, test points, named-pad aliases and empty footprints. This is NOT a count of 150 fitted electronic parts.
- 29 short, locally visible net fragments encoded in the schematic.
- Zero continuity-confirmed nets; 290 modeled pads remain unresolved in this revision.
- Known ICs: U4 PIC16F18855; U5 MX512H; U3 SGM8542XS. U1/U2/U6 and several short-marked devices remain unidentified.
- Unmarked capacitor values are UNKNOWN. Empty footprints are DNP, not zero-ohm links.
- The separate PIR daughterboard is included in the source photographs but is **not reconstructed** yet.

## Photograph outputs

`front_registered.png` combines a perspective-rectified overview with registered detail photographs. Each output pixel is taken from a selected source; there is no inpainting or invented copper. Seams are visible where the selected source changes. `front_source_ids.png` and `front_registration.json` record provenance.

`back_unrectified.png` is the sequential rear mosaic. `back_mirrored_registered.png` aligns the rear to the front for comparison. This is approximate registration, NOT a dimensional or electrical measurement. `back_readable.png` restores readable rear orientation. Full-size JPEG companions support the browser atlas. The original JPEG uploads are included byte-for-byte under `photos/originals/` with SHA-256 checksums.

The compact ZIP omits the large PNG mosaics; full-resolution JPEG companions and original photos are included. Lossless PNG front/rear mosaics are provided separately in the chat. Stitching scripts regenerate PNG outputs from the original photos.

## Layer count

Unconfirmed. The rear looks like a broad copper plane and numerous signal routes disappear at vias without a visible rear track. This raises the possibility of inner routing layers, rather than establishing a two-layer stackup. It is not photographic proof of a four-layer stackup. Electrical endpoint reconstruction is possible without knowing the physical layer used by each net.

## How evidence is represented

`VISUAL_LOCAL`: a short trace is visible in a specific source photograph. This is weaker than continuity confirmation and can be corrected.

`CANDIDATE_NOT_CONNECTED` / `HYPOTHESIS`: plausible relationship recorded outside the schematic. No wire is drawn for it.

`UNRESOLVED_NOT_NC`: the symbol pin is left open because its connection is not known. There are no no-connect flags to make these uncertainties disappear.

Known package pins use datasheet numbering. Unknown ICs/transistors use physical pad IDs; their source-photo orientation is recorded. Passive pin 1 is left/top and pin 2 right/bottom in the cited upright detail photo; this is a reconstruction convention, not a verified PCB-footprint pad numbering system. Multiple photographic ground pads are not silently collapsed into one electrical node.

## Validation performed

`evidence/validation.json` records balanced/native-file structural parsing, existence of child sheets, unique catalog references, matching symbol pins, valid model endpoints and the absence of fabricated no-connect flags. **KiCad is not installed in the execution environment: the native editor has not opened the files, and native ERC/netlist export were not run.** SVG previews are independently generated from the same data; they are not KiCad renderings.

## Continue the work

Start with `docs/MEASUREMENTS.md` and fill `evidence/measurements_round1.csv`. `CODEX_TASK.md` gives the continuation task. The immediate goal is reconstructing the original board, not choosing an ESP32 retrofit circuit.

The generators run with Python 3. `build_reconstruction.py`, `generate_kicad.py` and `validate_structure.py` use the standard library. Photo tools additionally use Pillow, NumPy and OpenCV. Do not overwrite manual KiCad edits blindly: the JSON/CSV model and the generator must be updated in parallel before regenerating.
