# PetSafe PCB reverse engineering

Working reconstruction of the PetSafe PPA19-16811 main board, **100-1339 R03 A**. All 150 catalog entries are drawn on **one A2 KiCad 10 sheet**, with wires within functional blocks and named nets between them. Entries include test pads and unpopulated options.

Start with [the offline overview](index.html), [the current completion checklist](docs/FINISHING_CHECKLIST.html), or [the printable status](output/pdf/PetSafe_completion_status.pdf). Open [the native schematic](schematic/PetSafe_1001339.kicad_sch) in KiCad 10. The [single-sheet PDF](output/pdf/PetSafe_single_sheet.pdf) and SVG are native KiCad exports.

## Current status

Schematic revision **v0.9.17**; C26-RA1 wiring resolved from user annotation **2026-10-09**. See [review response](docs/ARCHITECT_REVIEW_RESPONSE.md). The model and native file agree on 83 net partitions. All PIC pads have modeled local connections, but some remote destinations and circuit roles remain uncertain. There is **no routed KiCad PCB**, confirmed layer stack, or powered functional validation.

| Remaining work | Current state |
|---|---|
| Open physical pads | 19: 6 on populated entries, 13 on empty options; C26 and all U7 pads now mapped |
| Other incomplete connections | 2 isolated labels, plus inferred receiver/RF/PIR branches |
| Values | 44 fitted ceramic values; L1/L2 type and value |
| Footprints | 147/150 assigned; C5, S1 and LED1 geometry missing |
| ERC | 26 findings: 19 open pins, 2 isolated labels, 5 undriven power inputs |
| Libraries | 20 stock definitions and 4 authorized custom candidate definitions in use |

The checklist gives every known issue a stable ID, supporting evidence, next useful check and closure criterion. **A question mark, an assigned footprint, or zero open PIC pads does not measure overall completeness.** D2's local destinations are now mapped: R-C20 lower, L-ANT2/R46 upper, S-R46 lower. R46 remains unpopulated; D2 exact identity remains unknown. D3 rail association is closed by the user measurement: D3.R to V082/VDD, D3.L to GND. D3.S-to-R42 is 1.2 ohm; the exact resistor pad remains photo-selected. U3 pin 5 is now measured on VREF (1 ohm). J3 pin 3 is measured GND (1 ohm), while pin 2 reads 290 kohm to GND. J3 pin 2 now reaches R38 K/right at 1 ohm, U3 pin 6 reaches R23 B/left at 1 ohm, and R22 E/right reaches GND at 1 ohm. The old R23-VREF and J3 role guesses remain removed; R23 C/right now joins C40 lower and R42 upper at 1 ohm each. The old C40 detector-output connection has been removed; R42.1 retains the earlier TP4/PIC25 remote association.

The [finishing photo guide](docs/FINISHING_MEASUREMENTS.html) records all five batches. TP16-to-TP11/TP17 each read 400 kohm; both direct links are rejected. U7.1/2/3 now map to J3.3/2/1. PIC21/RB0 now joins TP16/Q2.S. The user explicitly withdrew PIC21-VREF after TP16-VREF measured 0.8 Mohm; the earlier C25 PIR candidate check is cancelled. The user annotation now resolves C25 to PIC2/RA0 and C26 to PIC3/RA1, sharing GND. C26 joins R28/R29/TP7; both capacitance values remain unknown. Clear surface traces are resolved from photos first. Bench requests are reserved for hidden continuations, ambiguous contacts/pin functions or conflicting evidence. Resolve signal paths first, then recover frequency-sensitive capacitor values with the LCR meter, check operating voltages and remaining package details, and finalize the sheet with explicit measured/assumed component evidence. These batches do not cover every remaining circuit question. Completed D2, D3 and via tests must not be repeated.

## Power names

| Name | Meaning |
|---|---|
| BATTERY+ | Printed BATTERY (+), before Q1 |
| VSYS | User-approved name after Q1; U5/MX512H pin 4 and the supply sides of L1/L2 |
| VDD | Printed VDD test point, regulated logic supply; U5 pin 1 / VCC |
| VREF | Printed VREF test point and confirmed PIC/bias connections |
| GND | Printed GND and BATTERY (-) |

L1/L2 share VSYS on their supply sides; their opposite ends are separate filter branches. H_RF_VDD, H_LDO_IN, H_RX_VDD and H_PIR_VDD are descriptive local branch names, not additional confirmed independent power sources. Actual rail voltages are not yet measured.

## Evidence and navigation

- [Current circuit interpretation](docs/RECONSTRUCTION.md), [measurements](docs/MEASUREMENTS.md), [sources](docs/SOURCES.md), and [library choices / alternatives](docs/LIBRARIES_AND_ALTERNATIVES.md).
- [Front/rear via viewer](docs/VIA_REVIEW.html), [via-pair results](docs/VIA_PAIR_TESTS.html), [current via summary](docs/VIA_REVIEW_RESULTS.md), and [numbered PIC photo](output/pdf/PetSafe_PIC_GPIO_pin_map.pdf).
- [Per-component audit](evidence/completion_audit.csv), [all modeled nets](evidence/proposed_nets.csv), [PIC evidence table](evidence/pic_gpio_status.csv), and [maintained question register](evidence/remaining_work.json).
- [Investigation history](docs/history/README.md). Historical claims and counts are not current instructions or outstanding measurements.

The original ZIP is in `input/`. Original photographs and their checksums are preserved. User reports, photo-derived copper and typical-application hypotheses remain distinct. A source datasheet validates a candidate symbol's pin map, not the fitted part's identity or board wiring. Western alternatives are redesign options, not silent substitutions.

## Reproduce and maintain

Use KiCad **10.x** (validated with 10.0.5), PowerShell and Python 3. Install `tools/requirements.txt` in a Python environment. Author schematic changes with the connected [KiCad MCP server](https://github.com/mixelpixx/KiCAD-MCP-Server); preserve stock library graphics and normal pin numbering. Four project-local symbols are registered using `${KIPRJMOD}`.

```powershell
$env:PYTHONUTF8 = '1'
python -m pip install -r tools/requirements.txt
./tools/build.ps1 -Python python
./tools/refresh_review.ps1 -Python python
```

`build.ps1` exports the existing native file, runs ERC and checks model/netlist partitions and footprints. It does not overwrite native edits. `-Regenerate` explicitly rebuilds from the saved MCP placement template and routing adapter; use it only when those sources are synchronized. `refresh_review.ps1` regenerates current documentation/status and checks electrical regressions and question coverage. Both commands fail on execution or validation errors; the documented outstanding ERC findings are retained.

For electrical edits, keep `evidence/reconstruction.json`, `evidence/library_layout.json`, `evidence/library_placements.json`, the MCP template, native schematic and routing adapter consistent. For documentation updates, maintain `evidence/remaining_work.json`; shared metrics are derived by `tools/current_state.py`. The live electrical suite is `tools/verify_evidence_contracts.py`; `verify_current_review.py` derives current counts and validates active/closed issues. `test_review_progress.py` exercises issue closure and capacitor recovery using in-memory fixtures only. `verify_cleanup_snapshot.py` checks the immutable 522d235 cleanup baseline; versioned suites such as `verify_v099_review.py` remain historical. Generated outputs should be rebuilt, not edited alone.

Local KiCad history, lock files, caches, QA renders and export ZIPs are ignored. No generated artifact is a fabrication release. Repository: [kerby2000/PetSafe-PCB](https://github.com/kerby2000/PetSafe-PCB).

## Completion milestones

**Topology complete:** supported populated-component and block-interface connections, compatible candidate functions, and individually documented exceptions. **Value/package complete:** required values and geometry recovered, with exact maker/ratings distinguished from equivalent choices. A routed PCB is separate. Signal paths take priority over perfecting C5/S1/LED1 footprints.
