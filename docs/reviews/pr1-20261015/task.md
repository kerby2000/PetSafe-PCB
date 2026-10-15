# Codex task — finish the PetSafe topology audit and simplify the repository

**Repository:** `kerby2000/PetSafe-PCB`  
**Existing PR:** #1 — `https://github.com/kerby2000/PetSafe-PCB/pull/1`  
**Reviewed baseline:** schematic v0.9.44, commit `06e7809163db8660d268cfa20962bd2dddf420a1`  
**Expected working branch:** `codex/architect-review-522d235`

## Objective

Implement the architect’s review, rather than returning another proposed plan. Correct the supported R39 connection error, make the repository immediately understandable, and identify the exact remaining topology/device-model uncertainties using existing evidence.

The finished repository should clearly show **the actual PCB, the current schematic, and what is still unresolved**. This task is about connection correctness and an honest completion assessment, **not capacitor-value selection or replacement-PCB design**.

Complete everything possible without new bench work. A genuinely unresolved device or hidden connection should remain a specific, documented exception; it should not block unrelated corrections and cleanup.

## 1. Establish the starting point

Read `AGENTS.md`, the current `README.md`, `evidence/remaining_work.json`, and the architect’s review. Consult individual historical records only when needed to resolve a particular claim.

Check the current local worktree and PR head before editing. The commit above is the reviewed snapshot, not an instruction to reset the repository. If the branch has advanced, inspect the relevant changes and do not undo a later correction or repeat an already completed task. Preserve unrelated local edits; do not reset, force-push, or rewrite history.

Use the existing KiCad MCP/native installation and repository tools. Capture the starting schematic revision, normalized net memberships, ERC findings, and any pre-existing build failure. If a tool is genuinely unavailable, identify the missing validation precisely; do not replace a native-validation claim with a text-only check.

Primary working files are:

- `evidence/reconstruction.json`, `evidence/pin_crosswalk.json`, `evidence/proposed_nets.csv` and the existing measurement/photo records;
- `schematic/PetSafe_1001339.kicad_sch`, the configured placement template/layout sources, and `output/PetSafe_netlist.xml`;
- `evidence/remaining_work.json`, the existing current-state generators and live verification scripts.

Retain the existing source/generation ownership. Do not change only a generated CSV, HTML page or exported netlist and leave its source inconsistent.

## 2. Commit A — correct R39’s endpoint, with a bounded electrical diff

### Finding to verify against the original

At the reviewed baseline, the model contains:

```text
PIR_BASE:  Q2.R; R38.2; R39.1
H_PIR_SIG: Q2.S; TP16.1; U4.21
VDD:       ...; R39.2; ...
```

The physical crosswalk maps `Q2.R` to native `Q2.1`, `Q2.S` to `Q2.3`, and `Q2.L` to `Q2.2`. With the current candidate NPN symbol, these are base, collector and emitter respectively. The physical label `S` means **single pad**, not MOSFET source.

Reinspect **`photos/originals/IMG_2425.jpg`**. The R39 terminal nearest TP16 has visible continuous copper to TP16; TP16 also reaches Q2’s single terminal. The architect’s finding is that R39 is an output pull-up, not a base pull-up.

Original photo SHA-256:

```text
8dbfb5bc465138ddbc884c13677737045250d0249b7df5238c9db49ff090eb8b
```

A supporting crop is supplied in the task package as `references/PetSafe_R39_photo_evidence.png`. Use the original as the authority. Check for any later explicit contradictory measurement before applying the correction; the baseline base-side association was described as inferred.

### Exact change

```text
Remove R39.1 from PIR_BASE.
Add R39.1 to H_PIR_SIG.
Keep R39.2 on VDD.
Keep R39 = 10k and all Q2 physical-to-native mappings unchanged.
```

Result:

```text
PIR_BASE:  Q2.R; R38.2
H_PIR_SIG: Q2.S; TP16.1; U4.21; R39.1
```

**Do not merge the base and collector nets.** This is one terminal moving between existing nets, not a connection between those nets.

Update the electrical source, native schematic, relevant template/layout metadata and generated evidence consistently. Add a short correction record identifying the source photo and the superseded inference. Preserve original photos, numeric readings and chronological records.

### Acceptance checks

Resolve physical aliases through the current crosswalk, and verify the exported native netlist:

```text
SAME:      R39.1, TP16.1, Q2.3, U4.21
SAME:      Q2.1, R38.2
DIFFERENT: R39.1 versus Q2.1
SAME:      R39.2 and the printed VDD node
```

For this commit, compare normalized physical-pad partitions before and after. After omitting `R39.1` from both comparisons, all remaining partitions must be identical. Compare actual membership, not only names or counts.

At the reviewed baseline, this change is expected to preserve the 82-net count and the one retained ERC conflict. Do not hard-code those historical totals as permanent acceptance criteria. Investigate any unexpected difference.

Run the existing build/review commands and visually inspect the PIR region in the native-rendered schematic. Preserve the starred capacitor estimates and all other electrical decisions.

If the original photo is genuinely ambiguous or conflicts with later evidence, leave this endpoint unresolved and explain the exact conflict. Only then propose **one** power-off resistance check: R39’s terminal nearest TP16 to TP16. Do not ask for a fresh PIR sweep.

## 3. Commit B — make the repository clear, without changing connectivity

Keep current working paths unless a change is necessary. Improve navigation before moving files. Do not restructure the entire repository or break the existing build to make it look tidy.

### README and overview

Give `README.md` and the current overview these prominent entry points:

| Entry | Required content |
|---|---|
| **Schematic** | A visible current preview, PDF link and editable KiCad project/schematic link. |
| **Physical PCB** | Front and rear photographs. Label any mirrored/registered image as an approximate comparison aid. |
| **Open items** | A compact current table and a GitHub-readable Markdown view. |
| **Evidence and rebuild** | Existing build commands, source records and one clear history link. |

Start with board identity, schematic revision and a brief statement of present scope. Move lengthy restoration narratives, superseded investigations and repeated measurement explanations out of the landing-page prose, while preserving access to their source records.

The repository does not yet contain a routed reproduction PCB. Say so explicitly. **Do not create an empty or speculative `.kicad_pcb` just to claim the PCB is present.** Photographic board documentation and a routed CAD board are different deliverables.

Retain the one-sheet schematic and its functional grouping. Regenerate a readable preview from the native file. Avoid unrelated aesthetic changes.

### One authoritative open-item register

Continue using `evidence/remaining_work.json`. Generate a Markdown view such as `docs/OPEN_ITEMS.md` from it using the existing review tooling. Keep the current HTML view; do not maintain parallel hand-written issue lists.

For each item, show:

| Field | Meaning |
|---|---|
| ID / area | Preserve existing IDs; put R39 under E07. |
| Category | Copper connection, physical pin mapping, device function/rating, operating behaviour, or reproduction/package. |
| Known | The specific established facts. |
| Unresolved claim | Exactly what is not established; use component/pad names where applicable. |
| Next Codex action | What can be decided from current photos, measurements, datasheets or model checks. |
| Owner input | None, one specific future check, or deferred by owner. |
| Closure evidence | What would actually resolve the claim. |

Do not force the register to retain exactly nine open groups if justified findings change that count. Do not turn a deferred question into a resolved fact. Show accepted limitations separately from closed findings.

### Correct these stale active descriptions

Check the latest branch before changing them:

- `docs/RECONSTRUCTION.md` starts at v0.9.43 in the reviewed snapshot despite the current schematic being v0.9.44.
- `H_PIR_RAW` still refers to an R33 branch after R33 was removed from the active reconstruction.
- R40’s description still calls S1 common pairs inferred, although the S1 record documents completed contact measurements.
- `remaining_work.json` contains an old U6A numbering account in `photo_supported_summary`. Keep that dated account as history, not the active pin map. The current regulator crosswalk is **U106.3 input, U106.2 output, U106.1 ground**.
- Update active R39/Q2 descriptions after Commit A. Do not retain the disproved base-pull-up account as current interpretation.

### Acceptance checks

This cleanup commit must change **no electrical memberships, pin mappings, component values or population choices**. Update source descriptions and regenerate dependent outputs rather than manually patching generated pages. Check relative links, current revision labels and consistency between the Markdown/HTML open-item views.

Preserve original photos, raw readings and explicit negative results. Keep historical documents recognisably historical; do not rewrite the original measurements to remove a contradiction.

## 4. Commit C — audit physical evidence independently of the schematic

Extend the existing audit with a small evidence-coverage pass. Do not build another framework, database or dashboard.

The question is **whether the captured net partition is justified by the PCB evidence**, not merely whether JSON, CSV and KiCad agree.

### Evidence model

Reuse explicit meter-confirmed joins and independently traced photo connections. Each direct connection must identify physical endpoints and its source record or original photo. Keep inferred joins distinguishable from these supported connections.

Do not populate the evidence graph by assuming every modeled net member is connected: that would repeat the existing self-consistency check. If a supported statement currently exists only in prose, encode the relevant endpoint pair with its source, without promoting nearby assumptions along with it.

Respect supersessions: retain old raw records, but do not simultaneously apply withdrawn claims as current constraints.

### Compare the evidence with the model

| Condition | Required output |
|---|---|
| A supported direct join spans two modeled nets | A specific split/wrong-assignment finding. |
| An applicable measured separation is merged in one net | A specific incorrect-merge finding. |
| A modeled net contains unconnected evidence groups | An unsupported-join question naming representative endpoints and missing evidence. This is not automatically proof of an electrical error. |
| A photographed pad/component lacks an inventory mapping | A concrete coverage finding. A gap in reference-number sequence alone is not proof of an omitted part. |
| Copper membership is supported but pin function is uncertain | A device-model qualification, not an unassigned wire. |

Do not treat paths through resistors, antenna windings, semiconductor junctions or a temporarily closed switch as direct PCB copper. Do not bridge DNP footprints. Keep measurement configuration and contact uncertainty attached to ambiguous low-resistance readings.

Check suspicious inherited local joins against the sharpest original close-ups, not only the mosaic. Prioritise transistor terminals, diode common pins, supply/filter boundaries and receiver feedback/bias connections. Reuse the existing photo viewer; provide a local comparison only when it helps explain a finding.

For additional unequivocal photo-supported corrections, make separate bounded changes with source evidence and endpoint-level regression checks. Do not silently fold them into the R39 or documentation-only commits. Where evidence conflicts, record the alternatives instead of choosing the electrically prettier circuit.

### Focus on the remaining device questions

| Area | Useful Codex work now | Do not do |
|---|---|---|
| **Q3/Q4/Q5/Q6/Q11** | Compare candidate device/pin-role interpretations against the corrected antenna topology and recorded diode tests. Flag the disputed PNP model visibly. | Assume a PNP-to-NPN/MOSFET substitution is proved, repeat completed diode tests, or alter antenna nets to make a hypothesis work. |
| **U2** | Reconcile the C14R candidate, measured 6.3 V supply and candidate operating limits using primary manufacturer evidence. | Reconnect U2 to 4.5 V merely to satisfy the assumed part, or treat an absolute maximum as a recommended operating voltage. |
| **D2** | Distinguish the supported external pad map and reported R→S→L junction behaviour from unknown manufacturer identity. Show an equivalent-function explanation separately if helpful. | Silently install a new part identity or change physical numbering to fit a stock symbol. |
| **Q1/Q7/Q8 and receiver** | Check DC paths, bias, polarity and available drive levels against the latest evidence and state-dependent readings. | Reopen the superseded Q1 low-resistance conflict or the old 4.5 V Q8-driver argument as current established defects. |
| **D6** | Keep established polarity/routing separate from unresolved breakdown and programming compatibility. | Test breakdown through the PIC, erase firmware or infer voltage from the G3 marking alone. |
| **TP11/TP17** | Retain supported local PIC routes and explicitly show the unexcluded-hidden-branch limitation. | Add arbitrary destinations or declare these nets proven intentionally unused. |

Small calculations or simulations may help **falsify an interpretation**, but a simulation that works does not establish a hidden connection. Exclude DNP devices from any functional simulation, model actual pin numbers, and keep hypothetical device models separate from the as-built record.

The external battery, motor, antenna and PIR daughterboard may be shown in a clearly labelled context view. Do not add them to the main-board component count. In particular, a coil between ANT1 and ANT2 is not a direct copper join between those PCB nets.

## 5. Measurement policy for this task

Do not request another broad measurement campaign. Existing photographs and recorded readings come first. Scope work and component lifting remain deferred by the owner. Capacitor values are outside this task.

Only propose a new test when you can state the competing alternatives and explain why current evidence cannot distinguish them. For each necessary future check, record the exact physical probe endpoints, mode, power state and the result that would settle the question. Use a labelled original photo when orientation is not obvious.

Rank remaining checks by how many important uncertainties they resolve. If a modeled net has several disconnected evidence groups, seek the smallest set of useful bridges between those groups; do not test every pair. A lack of an encoded graph edge is not automatically a reason to ask the owner for a measurement: an existing photo or record may already supply it.

Keep any unavoidable measurement queue in the existing issue register. Present only the next highest-value check for owner action, and continue all nonblocked work.

## 6. Validation and preserved decisions

Use the existing workflow, or its current equivalent if the branch has evolved:

```powershell
$env:PYTHONUTF8 = '1'
./tools/build.ps1 -Python python
./tools/refresh_review.ps1 -Python python
```

Do not run `-Regenerate` against stale templates or overwrite manual schematic work. Synchronise the relevant source/template first.

Validate native export, model/native memberships, measured same/separate-net constraints, physical-to-native mapping, dangling wires and current documentation. Inspect the final rendered schematic, particularly the PIR block and any other altered region. Report checks not run. Do not bypass a browser/tool restriction to claim UI testing.

Preserve:

- All 44 starred capacitor estimates, their qualifications, C5 and unrelated resistor/inductor values.
- The existing U6A/U106 regulator symbol, DNP status, pin mapping and deliberately retained output-conflict ERC finding.
- Established connections and exclusions, including corrected J1/J3/S1, RA0/TP6, TP14/OUTA, R5/U2 supply and ANT2 front-bank routing.
- Original reference identities, photographs and numeric measurements; no guessed replacement components or invented readings.

Do not aim for zero ERC by adding flags/exclusions or changing symbols to hide uncertainty. Keep historical snapshot checks separate from live acceptance. Do not force a net count: verify the intended membership change and absence of unintended changes.

No firmware work, battery conversion, ESP32 integration, fabricated-board routing or layer-count claim belongs in this task. Those remain separate projects or later milestones.

## 7. Deliverables and final response

Produce the actual changes and updated artifacts, not another long planning document:

1. **A corrected native schematic and exports**, with the R39 finding resolved or explicitly blocked by cited contrary evidence, and all additional corrections separately justified.
2. **A clear README/overview and generated `docs/OPEN_ITEMS.md`**, sourced from the existing register, showing the physical PCB and schematic prominently.
3. **One concise closure-audit result** listing concrete unsupported joins, conflicts, device-role uncertainties and accepted boundaries. Reuse the current audit output where possible.
4. **Focused regression checks** for R39 and any other justified correction, plus the existing native validation results.

Commit the work in separately reviewable units: electrical correction, documentation-only cleanup, and audit improvements. Additional electrical corrections should have their own bounded diff. Push to the existing PR branch and update PR #1’s summary with the new revision and remaining uncertainties. **Leave PR #1 open and unmerged; do not approve it on behalf of the independent reviewer.**

Your final reply should give the commit IDs, exact electrical changes, checks actually run, links to the current schematic/PCB views/open items, and the next required owner action—or state that none is requested now.

Distinguish these completion claims:

| Claim | Evidence needed |
|---|---|
| **Files internally consistent** | Native schematic, exported netlist and maintained model agree. |
| **Main-board copper connectivity verified** | In-scope joins have physical support and known exclusions hold; hidden-route exceptions are identified, not silently counted as resolved. |
| **Device model verified** | Physical terminals and device functions/polarities are adequately supported. |
| **Operating behaviour validated** | Appropriate original-hardware operating evidence exists. |
| **PCB reproduction ready** | Geometry, footprints, routing/stackup, assembly interfaces and firmware requirements are addressed. |

Completing this task does not require claiming that all five milestones are complete. A clean repository with corrected supported connections and a short, precise unresolved list is the required outcome. **Do not label the schematic “100% verified” while a disputed device model or unverified hidden branch remains.**

---

### Reference material

This task implements `PetSafe_v0944_PR1_review.md`, based on the pinned v0.9.44 snapshot above. The task package contains that review and the R39 photo crop under `references/`; neither overrides later owner measurements or the current worktree.

Important original evidence remains in the repository: `photos/originals/IMG_2425.jpg`, `evidence/original_photo_manifest.json`, `evidence/pin_crosswalk.json`, `evidence/proposed_nets.csv`, `output/PetSafe_netlist.xml`, `evidence/remaining_work.json`, `evidence/components.csv`, `docs/RECONSTRUCTION.md` and the dated measurement records. Reinspect them rather than copying a reviewer’s conclusion without checking it.
