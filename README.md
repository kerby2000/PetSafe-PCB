# PetSafe PCB reverse engineering

Current schematic and review: **v0.9.32**, 2026-10-09. PetSafe PPA19-16811 main board, **100-1339 R03 A**. All 148 catalog entries, including test pads and empty options, are on one A2 KiCad 10 sheet.

Open [the current overview](index.html), [the completion checklist](docs/FINISHING_CHECKLIST.html), [the native schematic](schematic/PetSafe_1001339.kicad_sch), or [the schematic PDF](output/pdf/PetSafe_single_sheet.pdf). The [printable status](output/pdf/PetSafe_completion_status.pdf) includes only current questions and closure criteria. The [measurement page](docs/FINISHING_MEASUREMENTS.html) shows the **Q8 supply-path check B37**; completed results are archived.

## Current state

| Area | Status |
|---|---|
| Drawing | One A2 sheet, 148 entries / 153 symbol units, normal local wires and named inter-block nets |
| Physical pads | 348 assigned to modeled local nets, one supported intentional NC at U6 pin4; zero unassigned pads |
| Connectivity check | 83 model/native net partitions agree; this checks file consistency, not every physical assumption |
| ERC | One user-retained U6/U6A output conflict; five source declarations resolved; no missing-library findings or isolated labels |
| Values | 44 fitted ceramic values unknown; C5 470 uF / 16 V; L1 1.4 uH / L2 2.2 uH readings recorded |
| Packages | 147/148 candidates assigned; LED1 remains blank; exact fit and pin maps remain qualified |
| Libraries | 22 stock device definitions plus four datasheet candidate definitions; five additional stock PWR_FLAG annotations |
| Hardware | No powered functional validation, confirmed layer stack or routed KiCad PCB |

The [current finalization audit](docs/reviews/2026-10-09_finalization_cleanup_v0.9.31.md) resolves power declarations and library registration, audits native wire ends and dispositions every earlier issue. Previous reviews are preserved in history. The earlier review ZIP remains frozen at v0.9.28 / `6ae4eaa`.

## What remains to finalize the schematic

1. **Resolve hidden paths and device behavior.** Q3 stays fitted by user choice; isolated identification is deferred. Next is Q8 supply-path check B37. Remaining gaps include three local-only PIC branches, antenna continuations, candidate pin functions, button contacts and operating levels, tracked individually in the checklist.
2. **Recover critical component values.** 44 ceramic values remain. Prioritize antenna/RF/receiver components after topology, accounting for parallel paths in LCR readings.
3. **Finish interface and package mapping.** LED colour/pad assignment and its missing footprint, plus motor lead orientation. Exact package fit, routed PCB/layer stack, daughterboard and firmware are later reproduction work, not extra unfinished main-board wires.

Zero open pads does not mean every signal source, remote destination or candidate device function is established. There are zero dangling native wire ends and no pinless wire islands. Unsupported R33 and its assumed pull-up have been withdrawn after photo review and user inspection. See the [maintained question register](evidence/remaining_work.json) for the evidence, owner/agent actions and closure criteria for each issue.

## History

Resolved investigation is preserved in [history](docs/history/README.md). The active checklist has 12 issues; [every previous item has a disposition](evidence/finalization_review_v0931.json). No physical net partition was changed by this cleanup.

## Evidence and history

- [Current circuit interpretation](docs/RECONSTRUCTION.md), [recorded measurements](docs/MEASUREMENTS.md), [library and package choices](docs/LIBRARIES_AND_ALTERNATIVES.md), [sources](docs/SOURCES.md).
- [Via viewer](docs/VIA_REVIEW.html), [current via summary](docs/VIA_REVIEW_RESULTS.md), [via-pair results](docs/VIA_PAIR_TESTS.html), [component audit](evidence/completion_audit.csv), [modeled nets](evidence/proposed_nets.csv).
- [Investigation history](docs/history/README.md) preserves prior narratives and cancelled requests. Dated raw measurement records remain unchanged; later explicit user corrections supersede earlier hypotheses.

The original ZIP and all 26 photographs are preserved. Candidate datasheets establish symbol pin maps, not fitted-manufacturer identity or board wiring. DNP footprints do not contain assumed jumpers. Western alternatives are redesign candidates, not silent substitutions.

## Reproduce and maintain

Use KiCad 10.x (validated with 10.0.5), PowerShell and Python dependencies in `tools/requirements.txt`. Author schematic changes with the connected [KiCad MCP server](https://github.com/mixelpixx/KiCAD-MCP-Server), keeping the template, layout, physical pin crosswalk and model synchronized.

```powershell
$env:PYTHONUTF8 = '1'
./tools/build.ps1 -Python python
./tools/refresh_review.ps1 -Python python
```

`build.ps1` exports the existing native drawing and checks connectivity, ERC and footprints. `-Regenerate` explicitly rebuilds it from the MCP template and routing adapter; use only when synchronized. `refresh_review.ps1` regenerates current pages and status, checks electrical evidence and detects stale summaries. `remaining_work.json` owns the finishing plan; `current_state.py` supplies shared metrics. Historical versioned checks are not the live acceptance suite.

Local KiCad state, caches, locks and export ZIPs are ignored. Generated outputs are not fabrication releases. Repository: [kerby2000/PetSafe-PCB](https://github.com/kerby2000/PetSafe-PCB).
