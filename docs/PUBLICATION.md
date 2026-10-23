# Prototype publication preparation — draft, not a release

This prepares a public description of **PetSafe microchip cat-flap reverse engineering and a working ESP32 remote-button retrofit**. Firmware **0.1.0** and schematic **0.9.52** retain their own versions. `prototype-v0.1.0` is only a proposed project release name; no tag, GitHub release or Pages site is created by this task.

## Demo

[Short silent bench excerpt](../photos/publication/remote-button-bench-excerpt.mp4) (11.7 seconds, 720p H.264) comes from seconds 28–39.7 of the supplied demonstration. The remote command is off-screen in this excerpt. It documents the bench prototype, not the final installed supply, measured latch feedback or AI prey recognition. This small derivative provides a working demo link in the review PR; it is not the 264 MB original recording.

The full 39.7-second silent derivative is retained **locally, outside the repository** for later release/discussion attachment. Its monitor view includes a private chat and desktop content, so it is not approved for public distribution in its present form. Metadata removal alone does not redact visible information. The supplied audio version is not used or cleared for publication; no soundtrack is included in the public excerpt. Raw MOV/JPEG originals remain local and unchanged.

The three new publication photographs are cropped/resized JPEG derivatives with EXIF, XMP, GPS, capture-time, device and comment metadata removed. No circuitry is synthesized, painted over or reconstructed. The installed close-up excludes the wider room/balcony; the other two views document internal placement and cable routing. No person/context/wider-room photos are included. A source/derivative hash and transformation map is retained locally outside Git and contains no location metadata.

The [installation guide](BUTTON_BRIDGE.md#installed-placement) explicitly qualifies temporary tape/cardboard, incomplete views of insulation and strain relief, hidden joints and motor/cam clearance. The [power diagram](BUTTON_BRIDGE.md#current-wired-power-direction) follows the owner's 2026-10-23 wiring clarification, not an inference from wire colors.

## Licensing proposal

**Proposal only; no license is installed or changed.** Public GitHub visibility does not grant a uniform open-source license to all files; see [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

| Material | Proposed scope, subject to owner approval |
|---|---|
| Original add-on firmware and original tools | MIT, only for original contributions after checking contributor ownership; preserve third-party notices. |
| Original documentation and owner-authorized publication photos | CC BY 4.0, with creator attribution agreed by the owner. This does not cover quoted vendor material or private originals by implication. |
| Original design/reconstruction contributions | CC BY 4.0 is a proposed documentation/design scope; approval must distinguish these contributions from the manufacturer's design and imported library data. No claim of ownership over the factory circuit. |
| Imported/vendor/historical material | Keep its actual terms and provenance. No blanket MIT label across the repository or source archive. |

Third-party boundaries:

- **TrailCurrent Open Source Contributors**: the symbol and footprint come from [TrailCurrentKiCADLibraries at `fb8b1725b9de036cbeba4093080f277374322d15`](https://github.com/trailcurrentoss/TrailCurrentKiCADLibraries/tree/fb8b1725b9de036cbeba4093080f277374322d15). The [original MIT notice](../schematic/TrailCurrent-LICENSE.txt) is retained. Footprint model path/transform changes and exact-byte hashes are documented in the existing [bridge guide](BUTTON_BRIDGE.md#library-and-supplied-step-model) and model record.
- **Owner-supplied SuperMini STEP**: `ESP32-C6-SuperMini-owner.step` came from `esp32-c6-supermini-1.snapshot.14.zip` with a [CC BY-NC 4.0 notice](../schematic/ButtonBridge.3dshapes/OWNER-MODEL-LICENSE.jpg). The ZIP and STEP header do not identify a creator or source page. Those attribution details remain unresolved; do not guess an author from a similarly named online model. Retain the [license link](https://creativecommons.org/licenses/by-nc/4.0/), notice and existing import/normalization record. This asset and its rendered views are **not MIT**. Before redistributing a tagged bundle, obtain the original creator/source credit or exclude this optional STEP and its renders from a clearly scoped core package. Excluding it does not affect the electrical schematic; the current repository footprint/model reference is unchanged.
- **KiCad library contributors**: libraries use [CC BY-SA 4.0 with KiCad's design exception](https://www.kicad.org/libraries/license/). Designs using library data and redistribution of a library collection are distinct cases. Retain the relevant notices when packaging library material; no new license claim is made for embedded stock definitions.
- **Vendor documents and original product design**: the [source register](SOURCES.md) identifies manufacturer documents and URLs. Those datasheets, trademarks and third-party source records retain their own rights; do not relabel them as original project software or photos.

Suggested owner decision: approve the original-software/documentation/design scopes above, confirm attribution for original photos/contributions, and either provide the STEP creator/source or choose an optional-model exclusion for release packaging. Existing notices and evidence stay intact meanwhile. This is a provenance proposal, not a legal determination about third-party material.

## Draft release description

**Proposed title:** `prototype-v0.1.0 — working PetSafe remote-button retrofit`

This prototype adds local web/API button control to a PetSafe PPA19-16811 microchip cat flap. An ESP32-C6 SuperMini drives a 2N3904 through 4.7 kΩ, with 100 kΩ from base to emitter. The original pushbutton, PIC firmware and motor driver remain in use. The owner reports remote motor/button operation and installation. The API commands a short press; it does not know whether the flap is open, closed or latched.

The repository also contains the qualified schematic reconstruction, original measurement evidence and documented unknowns. Forty-four capacitor values remain estimates, and there is no routed reproduction PCB. Camera/prey recognition and automatic admission are planned, not implemented. Installed USB power is owner-described; current margin, source isolation and long-term behavior remain unqualified.

**Release source:** use the exact validated commit recorded below, only after review/merge and owner approval. Do not tag a moving branch or silently reuse an older validation record for changed content. If the final release commit differs, rerun relevant checks and update this draft before tagging.

## Proposed assets — nothing uploaded as a release

| Asset | Preparation and inclusion rule |
|---|---|
| Source archive | Export tracked source from the validated commit. Full repository history is still needed for historical audits. A GitHub source archive includes existing third-party assets; it is not automatically an unrestricted core package. Resolve the license scope first. |
| Native KiCad project | Project/schematic, project library tables and required local symbols/footprint. Include notices. Optional noncommercial STEP requires attribution clearance or a documented packaging-only omission. |
| Schematic PDF | Native export from the validated commit, with reconstruction/estimated-value qualifications retained. |
| Retrofit guide | Existing `docs/BUTTON_BRIDGE.md` and its referenced public media; no new competing guide/checklist. |
| Demo | Small silent bench excerpt. Prefer a release/discussion attachment for a later full video after visual privacy review/redaction and approval; never upload the original MOV. |
| SHA256SUMS | Generate from the exact approved, assembled assets immediately before publication; no speculative checksums for unbuilt packages. |

Exclude configured firmware, access tokens, Wi-Fi credentials, build directories, raw serial/network logs, local backup bundles and private media originals. An unconfigured binary has networking disabled and is **not a ready-to-use installer**; no binary installer is proposed here. Do not use a recursive working-directory ZIP as the source archive.

## Validation

Reviewed starting point: [`7bf727c4b753d1c0f620ca748917d07ce63623a3`](https://github.com/kerby2000/PetSafe-PCB/commit/7bf727c4b753d1c0f620ca748917d07ce63623a3). Publication-branch validation and its exact commit will be recorded before this PR is delivered. Firmware logic and native electrical files are outside the change scope.

## Hosting and approval boundary

GitHub Pages is optional and remains disabled. If later approved, deploy only an explicitly selected static documentation artifact and test its relative links/media. Do not upload private originals, credentials or arbitrary output/build folders. The ESP32's authenticated HTTP API remains a **local-network service**, never a public Pages backend or internet-facing control service.

Owner approval is required before adopting licenses, publishing a release or enabling Pages. This PR prepares the materials and records unresolved qualifications; it does not perform those actions.

Unofficial independent project; not affiliated with or endorsed by PetSafe or Radio Systems Corporation.
