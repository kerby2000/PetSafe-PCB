# Investigation history

These records preserve earlier reasoning and its provenance. They are **not current measurement requests or current circuit truth**. Use [the completion checklist](../FINISHING_CHECKLIST.html), [current circuit interpretation](../RECONSTRUCTION.md) and [current measurements](../MEASUREMENTS.md).

- [Pre-cleanup chronological reconstruction](pre_cleanup_20261008/docs/RECONSTRUCTION.md), [source/event register](pre_cleanup_20261008/docs/SOURCES.md), [via history](pre_cleanup_20261008/docs/VIA_REVIEW_RESULTS.md), and [old status JSON](pre_cleanup_20261008/evidence/completion_status.json). Their original relative links were relative to the project before archiving.
- Original supplied capture: `reference/v01/`; earlier authoring: `reference/v02/` at repository root.
- Dated `evidence/v0*_net_changes.json` and `evidence/v0*_verification.json` at repository root are provenance. Earlier verification reports describe their own revision; the live electrical suite is `tools/verify_evidence_contracts.py` with `tools/verify_current_review.py`; versioned suites are historical.
- Earlier U6/Q8 reports document why the WN23 supervisor and 372A interpretations were superseded by C2NM and 3724A. They also contain temporary wiring conflicts later resolved.
- Older round-1/round-2 measurement PDFs are historical prompts. Do not repeat a test just because it appears there. Current via-pair results say the GPIO batch is complete.

Key superseded claims: no measurements supplied; two/eight GPIO pads still open; Q1 as MMBT3904; C6 tied directly to Q8 output; V114 on Q8; Q1.L joined to R43.2; raw battery merged with post-Q1 motor supply. Each is corrected in the current files while its original reasoning remains auditable.

## v0.9.28 narrative cleanup

[Archived summaries](cleanup_v0928/README.md) preserve the pre-v0.9.29 text and its old requests. Original bytes and SHA-256 hashes are recorded in `evidence/cleanup_v0929.json` at repository root. Relative links in these preserved files describe their original location. Current pages correct TP9/C49, R41-VPP, PIC21/TP16, D6 polarity, U6A native numbers, C5 geometry and L1/L2 readings. No measurement history or electrical net was erased.
