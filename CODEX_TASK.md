# Current project handoff - 2026-10-08

Read AGENTS.md, README.md and evidence/remaining_work.json first. Schematic v0.9.9; documentation cleanup-1. Repository https://github.com/kerby2000/PetSafe-PCB. Local branch codex/single-sheet-reconstruction. Preserve the user's local schematic/PetSafe_1001339.kicad_pro and ignored schematic/.history/.

Current status is derived by tools/current_state.py. Run tools/build.ps1 followed by tools/refresh_review.ps1 (Python requirements installed; PYTHONUTF8=1). Do not edit generated HTML or status metrics alone. Latest electrical contracts are in tools/verify_v099_review.py; completion coverage in tools/verify_current_review.py. Older scripts/reports are historical, not the current work queue.

The power-path action is finished: BATTERY+ -> Q1 single/native3; Q1.L/native2 -> VSYS -> U5.4 and L1/L2 supply sides. VDD and VREF are separate printed board test points. Q1 is a stock PMOS FMOS3401A? candidate, not the old NPN. Never short across Q1/L1/L2. Keep all user negative evidence, including rejected Q1.L-R43.2 and RC1-VREF joins. The model's 83 partitions and all earlier measured routes remain unchanged by documentation cleanup.

Every known uncertainty has an ID, next check and closure criterion in remaining_work.json. Do not declare the schematic or PCB finished: 10 populated-entry open pads, 18 DNP open pads, 3 isolated labels, partly inferred branches, 44 ceramic values, L1/L2 values and 3 blank footprints remain. Zero open PIC pads only means each has a local modeled net. D3/V082 terminal identification is the first priority. Current docs record the unverified J3.2/.3 roles rather than inferring ground from wire colour.

Original photos/ZIP and chronological records are preserved. No routed PCB exists. No powered functional or rail-voltage readings supplied. Previous file:// browser automation was policy-denied; do not bypass with another browser or localhost. HTML can be inspected as source/data and opened for the user.
