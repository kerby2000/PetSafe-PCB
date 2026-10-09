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

## v0.9.30 remaining-work cleanup

The [previous register](v0.9.30-before-finalization/evidence/remaining_work.json) and [raw measurement queue/results](v0.9.30-before-finalization/evidence/finishing_measurements.json) preserve all prior observations. Old HTML and PDF snapshots retain their original relative-link context. SHA-256 hashes are in `evidence/cleanup_v0931.json` at repository root. The active register now omits completed substeps and duplicates; D2 identity is under I01, empty options are documented scope limitations, and PCB/daughterboard/firmware work is deferred explicitly rather than declared complete. See [the current audit response](../reviews/2026-10-09_finalization_cleanup_v0.9.31.md).

## v0.9.32 Q3 result and R33 withdrawal

[Recorded measurements and inventory correction](q3-r33-v0932.md). Q3 latest forward reading is 0.48 V; its identity remains disputed. The unsupported R33 entry and assumed pull-up were removed.

The user subsequently chose to leave Q3 fitted. Isolated identification is deferred; the next active check is B37 at Q8/C6. This changes the review queue only; see `evidence/q3_deferred_q8_followup_20261009.json`.

## v0.9.33 Q8 supply result

B37 P-F = 1 ohm supports the existing Q8.T2/native2 to C6.1 supply join. The older 10-ohm ambiguity is retired from the active checklist, while both observations remain recorded in `evidence/q8_supply_result_20261009.json` and `docs/MEASUREMENTS.md`. A fresh baseline and stability statement were not supplied. No net or pin mapping changed. Gate drive and fitted identity remain open; Q3 stays fitted by user choice.

## v0.9.34 S1 contact issue E05 closed

[S1 result ledger](../../evidence/s1_contact_results_20261009.json) retains B38-B41, the extra A-C OL report and the closed issue disposition. Same-row pairs read 1 ohm, cross-pair B-D reads OL released and 1 ohm pressed. Existing wiring and native pin mapping are retained. No further electrical contact test is needed; exact footprint fit remains separate under M01.
