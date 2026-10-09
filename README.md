# PetSafe PCB reverse engineering

Current schematic and review: **v0.9.29**, 2026-10-09. PetSafe PPA19-16811 main board, **100-1339 R03 A**. All 149 catalog entries, including test pads and empty options, are on one A2 KiCad 10 sheet.

Open [the current overview](index.html), [the completion checklist](docs/FINISHING_CHECKLIST.html), [the native schematic](schematic/PetSafe_1001339.kicad_sch), or [the schematic PDF](output/pdf/PetSafe_single_sheet.pdf). The [printable status](output/pdf/PetSafe_completion_status.pdf) includes the remaining questions and PIC map. The [measurement page](docs/FINISHING_MEASUREMENTS.html) preserves completed results; **no active bench batch is waiting for the owner**.

## Current state

| Area | Status |
|---|---|
| Drawing | One A2 sheet, 149 entries / 154 symbol units, normal local wires and named inter-block nets |
| Physical pads | 350 assigned to modeled local nets, one supported intentional NC at U6 pin4; zero unassigned pads |
| Connectivity check | 85 model/native net partitions agree; this checks file consistency, not every physical assumption |
| ERC | Seven retained findings: five undriven power inputs, U6/U6A output conflict, isolated H_D1_FREE label |
| Values | 44 fitted ceramic values unknown; C5 470 uF / 16 V; L1 1.4 uH / L2 2.2 uH readings recorded |
| Packages | 148/149 candidates assigned; LED1 remains blank; exact fit and pin maps remain qualified |
| Libraries | 22 stock definitions plus four explicitly authorized datasheet candidate definitions |
| Hardware | No powered functional validation, confirmed layer stack or routed KiCad PCB |

This cleanup corrects active documentation and symbol evidence metadata. **No electrical connections, values or footprint assignments changed.** The earlier [Pro review checkpoint](docs/reviews/2026-10-09_pro_review_v0.9.28.md) and its ZIP remain frozen at v0.9.28 / commit `6ae4eaa`. An independent Pro review has been prepared, not yet received.

## What remains to finalize the schematic

1. **Resolve the remaining functional paths.** One complete Q3 tuning cell; RF excitation at R6/R7; D1 and local-only PIC nodes; remaining receiver/PIR hypotheses. Agent traces original photos and checks existing measurements first. Request one targeted hidden-connection or device-behavior test only when it distinguishes explicit alternatives.
2. **Verify candidate devices and operating behavior.** Q1/Q8 and tuning-transistor pin roles, D2 identity, D6 breakdown/ICSP compatibility, S1 contacts and actual rail/gate voltages. Use existing markings and recorded tests first. Keep equivalent candidates explicit. Plan focused device/contact checks and then an appropriate powered session on the original hardware.
3. **Recover the required capacitor values.** 44 fitted ceramic values remain unknown. C5 is 470 uF / 16 V; L1 1.4 uH and L2 2.2 uH readings are already recorded. Prioritize antenna/RF/receiver capacitances after topology. Record LCR conditions and avoid assigning a parallel-network reading to each individual capacitor.
4. **Finish symbols and physical assignments.** LED1 footprint and red/green channel mapping; motor lead orientation. C5 lead pitch and S1 pad fit/3D height remain qualified. Use the measured LED1 1.5 mm square, C5 diameter 6.33 mm/height 16 mm and S1 6 mm body/overall height. Seek the missing pad map or pitch; do not repeat body measurements.
5. **Document optional and later reproduction work.** Empty option values/roles, J6 onward role, actual layer stack, daughterboard internals, firmware and a routed PCB. Retain DNP gaps and distinguish them from fitted circuits. These are not missing physical pad assignments; agree reproduction scope separately from finishing the main-board schematic.

Zero open pads does not mean every signal source, remote destination or candidate device function is established. Seven ERC findings are not seven missing wires. See the [maintained question register](evidence/remaining_work.json) for the evidence, owner/agent actions and closure criteria for each issue.

## Settled facts

- C49 is connected ANT2-to-GND and remains a DNP option; TP9 was removed as unsupported.
- All 351 physical pads are represented: 350 have modeled local nets and U6 pin4 is a supported NC. This does not prove all onward paths.
- R41 is 330 ohm and reaches VPP. D6 polarity/routing, D2 local terminals and D3 rail terminals are resolved.
- PIC21 reaches TP16/Q2, not VREF. J3/U7 and C25/C26 routes are resolved; U6 pin5 is externally tied to VIN.
- C5 is 470 uF / 16 V, diameter 6.33 mm and height 16 mm. L1/L2 read 1.4/2.2 uH; measurement conditions remain unspecified.
- R8 is 0603 by measured body; C11 supports 1206. LED1 is red/green in a 1.5 mm square body. S1 body/actuator dimensions are recorded.

Raw BATTERY+ is before Q1; **VSYS** is Q1's output, U5 pin4 and the common input sides of L1/L2. Printed **VDD** is the separate regulated logic rail/U5 pin1. Printed **VREF** and **GND** keep their PCB names. L1/L2 filter outputs are separate. Actual voltages are unmeasured.

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
