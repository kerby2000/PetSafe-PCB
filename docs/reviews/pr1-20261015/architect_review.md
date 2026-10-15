# PetSafe PR #1 — independent topology review and Codex task

**Reviewed revision:** v0.9.44  
**Pinned head:** `06e7809163db8660d268cfa20962bd2dddf420a1`  
**PR:** https://github.com/kerby2000/PetSafe-PCB/pull/1  
**Review date:** 2026-10-15  
**Scope:** Main-board connectivity, device-function assumptions, evidence completeness and repository clarity. Not capacitor-value selection or replacement-PCB design.

## Review boundary

This review used the GitHub connector to read the PR metadata, AGENTS.md, README, current connection table, relevant portions of the committed native XML netlist, current pin crosswalk, component inventory, remaining-work register, circuit-consistency review, ERC report and live evidence checker. Original IMG_2425 was re-inspected and its bytes match the pinned repository's original-photo manifest. Other supplied original photographs were inspected as context.

No repository changes or PR review submission were made. No new physical measurements were performed. Native KiCad/ERC was not rerun, and the current schematic PDF was not rendered in this session. Downloading a local repository snapshot was unsuccessful; findings are based on connector-read sources and the original mounted photo, not a locally checked-out full build.

## Verdict

The reconstruction has substantially improved, but there is at least one high-confidence, photo-supported connection error left: **R39.1 belongs on TP16/Q2 collector, not Q2 base**. This can be resolved without changing any capacitor value or transistor identity.

The recorded 82-net agreement and one ERC finding are useful file-consistency checks, not proof that the represented connections match the hardware. Moving R39.1 between the two existing nets would leave the net count unchanged and is not expected to create/remove an ERC finding.

# Finding 1 — R39 is assigned to the wrong Q2 node

**Priority:** High; actual reconstructed connectivity.  
**Confidence:** High, visible continuous surface copper, not a new multimeter result.  
**Source photo:** `photos/originals/IMG_2425.jpg`.  
**Original SHA-256:** `8dbfb5bc465138ddbc884c13677737045250d0249b7df5238c9db49ff090eb8b`.

## Current model and native export

`evidence/proposed_nets.csv` puts:

```text
PIR_BASE:   Q2.R; R38.2; R39.1
H_PIR_SIG: Q2.S; TP16.1; U4.21
VDD:        ...; R39.2; ...
```

The current crosswalk maps Q2.R to native Q2.1 (candidate base), Q2.S to Q2.3 (candidate collector), and Q2.L to Q2.2 (candidate emitter). The native netlist also places R39 pin 1 on `Net-(Q2-B)`, so this is not just a CSV/documentation discrepancy.

## Photograph

In IMG_2425, the R39 terminal nearest TP16 has a visible track straight to TP16. TP16 has another visible track to Q2's single terminal. The other R39 terminal leads to the R37 supply-side region, consistent with the existing VDD association.

The supplied evidence image crops original pixels at `(340,920)-(790,1290)`, rotates them 90 degrees counterclockwise and enlarges them. No traces are painted into the photograph.

## Bounded proposed correction

```text
Remove R39.1 from PIR_BASE.
Add R39.1 to H_PIR_SIG.
Keep R39.2 on VDD.
Keep all Q2 physical-to-native mappings unchanged.
```

Expected result:

```text
PIR_BASE:   Q2.R; R38.2
H_PIR_SIG: Q2.S; TP16.1; U4.21; R39.1
```

**Do not merge the base and collector nets.** This is a single-endpoint reassignment, not a new connection between the two nets.

Under the existing NPN candidate, the corrected circuit is a conventional input resistor plus collector pull-up:

```text
J3.2 -- R38 10k -- Q2 base
                       Q2 collector -- TP16 -- PIC21/RB0
                            |
                         R39 10k
                            |
                         VDD 4.5 V
Q2 emitter -- GND
```

The electrical interpretation reinforces the photo finding. In the current base-pull-up model, assuming a DC-coupled PIR output between 0 and 3.3 V and VBE approximately 0.7 V, even a 0 V raw signal leaves roughly `(4.5-0.7)/10k - 0.7/10k = 0.31 mA` available to the base. It therefore does not act as an ordinary on/off digital inverter. This conditional calculation is supporting reasoning, not the source of the proposed wire correction.

## Codex action

1. Inspect the original crop and check for any later explicit contradictory measurement. The current R39 inventory text calls its base-side association inferred.
2. Apply only the endpoint reassignment, updating the current model, native drawing, template/layout metadata and evidence view that actually contain this endpoint.
3. Keep original measurements, original photos and historical raw records unchanged. Add a short correction note that supersedes the old inference.
4. Add native-netlist checks:
   - same net: `R39.1`, `TP16.1`, `Q2.3`, `U4.21`;
   - same net: `Q2.1`, `R38.2`;
   - different nets: `R39.1` versus `Q2.1`;
   - same net: `R39.2`, printed `VDD`;
   - all other endpoint memberships unchanged.
5. Run the existing native build and review refresh, then inspect the PIR region in the rendered sheet.

No routine new measurement is needed for the visible track. If the original photo remains genuinely ambiguous after reinspection, use only the R39 terminal nearest TP16-to-TP16 resistance check, not a new PIR sweep.

# Finding 2 — device-function completeness is still distinct from copper completeness

These are largely known qualifications, not newly discovered missing wires:

| Area | Present evidence | Remaining decision |
|---|---|---|
| Q3/Q4/Q5/Q6/Q11 | Corrected ANT2 outer rail, grounded rear returns and mapped control resistors; Q3 directed diode results recorded | PNP identification and B/E/C assignment are not established. A correct copper map plus an incorrect symbol is not a complete electrical reconstruction. |
| U2 | C14R marking candidate; 6.3 V supply and R5 feed supported | Candidate SN74LVC2G14 recommended supply maximum is 5.5 V. Keep the measured rail; do not rewire to 4.5 V merely to satisfy a candidate datasheet. Resolve/qualify identity and ratings separately. |
| D2 | Three external endpoints mapped; reported R -> S -> L junction behavior | Its connector placeholder records copper but not an electrical device model. A measured-series-junction equivalent may be illustrated separately; it must not be silently substituted for a manufacturer identity or remap physical pins. |
| Q1/Q7/Q8 | Supply routes and several junction/voltage results recorded | Selected semiconductor functions, E/C or S/D roles where qualified, and operating states are not all independently established. |
| D6 | Polarity and VPP/GND route established | Reverse breakdown and compatibility with high-voltage programming remain unknown. No breakdown test through the PIC; no unnecessary repeated diode-mode readings. |
| TP11/TP17 | Local connections to PIC14/RC3 and PIC18/RC7 | No evidence proves there are no additional buried branches. Treat as explicit boundary limitations, not proved intentional non-use. |

Q3's PNP emitter-at-GND interpretation is particularly weak under ordinary positive GPIO drive. An ideal switch calculation does not resolve that device question. Compare alternative device-role hypotheses without altering the as-built copper to force one to work. Existing in-circuit readings do not uniquely identify a manufacturer or emitter/collector.

The revised U2 supply also supersedes the *old specific* concern that a 4.5 V driver necessarily leaves Q8's 6.3 V P-channel source inadequately driven high. The current driver supply is 6.3 V and resting VGS(P) was reported as zero. Dynamic non-overlap remains unverified, but the old wrong-rail argument must not be presented as a current established defect.

Respect the owner's current constraints: no oscilloscope work or component lifting requested now, and no repetition of completed batches. Keep these as explicit deferred validation limitations while exhausting useful photo/datasheet analysis.

# Finding 3 — several active descriptions are stale

These are not additional hardware defects, but undermine a clear current-state repository:

- `docs/RECONSTRUCTION.md` opens with v0.9.43 while the PR/native schematic is v0.9.44.
- `evidence/proposed_nets.csv` still describes an R33 branch under H_PIR_RAW even though R33 has been withdrawn from the active inventory and topology.
- The R40 inventory text still says S1 common pairs are inferred; the S1 row and current circuit document describe measured B38-B41 confirmation.
- `remaining_work.json` contains the dated v0.9.22 U6A input/native1 and ground/native3 description in `photo_supported_summary`, whereas the current crosswalk is native3 input, native2 output, native1 ground. Keep the old annotation in historical evidence, but do not surface it as a current pin map.
- README mixes current status with restoration history, capacitor-selection history and repeated measurement narratives. Those details should remain accessible, but not dominate the landing page.

Correct active summaries from the existing current crosswalk and event resolution. Do not delete raw historical records or change measurements to remove apparent contradictions.

# How to close connectivity without a broad new measurement campaign

## Independent evidence-to-net comparison

Extend the existing checker; do not introduce another parallel framework.

Build a small evidence graph from explicit current meter-confirmed joins and independently traced photo joins. A node is a physical terminal/via; an edge means direct copper continuity supported by a specific record or visible trace. Preserve negative results and explicit supersessions.

Then compare that graph to the modeled net partition:

1. A supported same-net edge split between two modeled nets is a missing/wrong connection.
2. A measured distinct-net constraint merged in one modeled net is a short in the reconstruction.
3. Multiple disconnected evidence groups inside one modeled net identify an unsupported join. Report the exact endpoints, not a global percentage.
4. A source component/terminal without an inventory mapping is a coverage issue.
5. A mapped terminal with a candidate pin function is a device-model qualification, not an unassigned wire.

The evidence graph must not be populated by simply reading and trusting the current modeled net memberships; that would repeat the current self-consistency test.

Do not union nets through resistors, coils, semiconductors, closed test switches or DNP footprints. A finite resistance reading is not automatically a copper edge. Keep test configuration, contact quality, fitted antenna and device state attached to ambiguous measurements.

If one modeled net has k disconnected *evidence* groups, at least k-1 justified bridging checks are needed to establish their common membership. Many can be closed from existing photos. Only the unresolved high-value bridges need a new owner measurement. This is how to keep the bench queue short rather than checking every possible pair.

## One independent review of the local copper

R39 is a useful example: the explicit image shows a connection that survived incorrectly in both model and native export. Audit the other inherited local HYPOTHESIS associations against the sharpest original photo, not just the stitched overview. Prioritize transistor base/collector/source/gate nodes, diode common pins, filtered supply branches and receiver feedback junctions.

For each reviewed region, show its current native subcircuit and the original photo side by side. Never paint guessed tracks into a photo. Annotate uncertainties without turning them into circuit facts.

## Functional consistency checks before further hardware tests

Useful without original capacitor values:

- DC bias/return paths for analogue inputs;
- whether switching devices can be both on and off under their available drive voltages;
- signal-voltage ranges and receiver-off states;
- power-domain boundaries and filtered feeds;
- documented connector orientation and physical pin numbering;
- whether every proposed control/measurement path has its modeled source and endpoint.

Use small, separate simulations to falsify hypotheses, not to rewrite the measured board. Exclude DNP devices from simulation. Use the real external antenna/motor/sensor interface conditions where relevant. Model pin order, not ambiguous hidden BAV99 pin-name strings.

# Make the repository easy to understand

Do navigation cleanup first, not a wholesale path migration that breaks the existing build.

The landing page should show, in this order:

1. Board identity, current revision/commit and a plain status: "reconstructed main-board schematic; remaining connectivity/device qualifications listed".
2. Current schematic preview, PDF and editable KiCad link.
3. Actual PCB front/back photo views, with a mirrored overlay explicitly labelled as an aid rather than exact hidden-layer reconstruction.
4. A compact current-open-items table generated from the existing register.
5. Rebuild instructions and one link to historical evidence.

For every open item show: physical area, whether it is copper/pin mapping/device role/rating/behavior/package, what is known, the exact unresolved claim, the next agent action, whether bench work is actually required, and closure evidence. Keep the nine existing issue IDs; add R39 under E07 rather than inventing a second issue system.

Add a GitHub-readable Markdown open-items summary from `remaining_work.json`. The existing HTML remains useful locally, but should not be the only way to read current questions on GitHub.

A PCB photo atlas is not a routed PCB. The repo currently has no routed reconstruction. A later placement-only KiCad PCB can help locate components and compare pads, but label it "placement-only / unrouted"; dimensions, drill sizes and hidden copper remain qualified. Do not make original-layer replication a requirement for finishing the main-board electrical schematic.

If a functional overview is added, show the antenna, battery, motor and PIR daughterboard in a clearly external boundary, with documented connector mapping. In particular, the antenna is an external coil between ANT1 and ANT2, not a reason to merge those PCB nets. The reported 500 uH remains qualified by missing test conditions. Do not invent main-board components or silently change the existing board BOM/counts to draw this context.

# Suggested Codex work order

## Commit A — R39 correction only

- Inspect IMG_2425 and resolve any explicit later counter-evidence.
- Apply the one-endpoint correction.
- Update its source references and the existing PIR interpretation.
- Preserve all unrelated partitions, starred capacitor values, C5, DNP choices and semiconductor candidates.
- Add the endpoint-level regression checks above; run the existing native build and refresh. Net count is expected to stay 82, but compare actual memberships rather than forcing a number.

## Commit B — current-state cleanup only

- Shorten README and current overview.
- Generate one Markdown open-items view from the existing JSON.
- Fix the named stale statements without rewriting their raw historical records.
- Mark accepted topology limitations separately from deferred behavior and package work.
- Keep U6A's existing regulator symbol, DNP status, pin map and single ERC conflict as requested.
- Verify that this cleanup changes no net membership.

## Commit C — topology-closure audit

- Add independent photo/meter-evidence coverage to the existing audit.
- Review inherited high-risk local joins from original photos.
- Report only unsupported joins, conflicting assignments, boundary limitations and unresolved device-role claims.
- Propose the minimum specific future probe pairs only when no existing evidence can decide them.
- Do not request scope/isolation work while the owner's deferral remains in force.

## Completion language

Separate these statements:

- **File consistency passed:** model and KiCad agree, intentional warning documented.
- **Copper topology verified:** every in-scope connection has supporting physical evidence and no unresolved contrary evidence.
- **Device model verified:** pin functions/polarities are established sufficiently for the circuit interpretation.
- **Operating behavior checked:** the original assembly agrees with selected predicted states.
- **PCB reproduction ready:** dimensions, package pin maps, routing/stackup and validation exist.

Only the first is currently near fully automated. A documented exception is a legitimate stopping point, but is not proof that the exception is physically resolved. No original capacitor value is required to correct R39 or to audit the copper connections.

## Pinned source index

All paths below are relative to commit `06e7809163db8660d268cfa20962bd2dddf420a1`:

- `README.md`, `AGENTS.md`
- `evidence/proposed_nets.csv`
- `output/PetSafe_netlist.xml`
- `evidence/components.csv`
- `evidence/pin_crosswalk.json`
- `evidence/original_photo_manifest.json`
- `photos/originals/IMG_2425.jpg`
- `evidence/remaining_work.json`
- `evidence/circuit_consistency_v0942.json`
- `docs/RECONSTRUCTION.md`
- `output/erc.json`
- `tools/refresh_review.ps1`, `tools/verify_evidence_contracts.py`

Manufacturer source checked for U2: https://www.ti.com/product/SN74LVC2G14 and TI SCES200O datasheet (1.65–5.5 V recommended VCC). The measured 6.3 V and candidate qualification come from the repository, not an independent reviewer measurement.
