# Finalization audit — v0.9.31

The active checklist now has 12 current issues. Every previous entry has an explicit disposition in `evidence/finalization_review_v0931.json`. Completed subquestions and prior checklists are preserved under `docs/history/v0.9.30-before-finalization/`, with original-byte hashes. No completed measurement was changed or requested again.

## ERC and library correction

KiCad **10.0.5** reports **one finding**: U6 output/native U106 output share the PIR supply. U106 is the unpopulated U6A regulator option. Its regulator symbol and visible ERC conflict remain at the user's explicit request. It is an ERC error classification in KiCad, not a silently waived warning; no exclusion was added.

Five stock `power:PWR_FLAG` annotations, placed through the KiCad MCP server, describe established or explicitly modeled source paths: GND return, post-Q1 VSYS, post-L2 U1 input, post-R37 U6 input, and post-Q7/R20 receiver supply. The last flag describes intended switched power distribution; it does not establish Q7 identity, turn-on behavior or voltage. Those remain E08/E09. See `evidence/power_source_declarations.json` for each basis. [KiCad documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html) explains power flags and power-input checks across passive components.

The project library table now includes every used library. PetSafe_Datasheet is also registered in the installed KiCad **10.0** user table for standalone schematic opening. The MCP global-registration helper initially selected the obsolete 9.0 configuration; that newly added entry was removed and the 10.0 table corrected explicitly, preserving other settings. All **29 embedded definitions** (including unused retained definitions and PWR_FLAG) match the registered sources; all stock sources are under KiCad 10. The native device netlist uses 22 stock device definitions and four custom candidate definitions; power annotations are not physical catalog entries.

An already-open graphical editor may need reopening through `schematic/PetSafe_1001339.kicad_pro`. Native loading, library matching, ERC and exports were verified; GUI reloading was not observed.

## Connection and inventory audit

- 149 catalog entries, 154 physical-device symbol units, 351 modeled physical pads. Of these, 350 are on local nets and U6 pin4 retains its existing intentional NC.
- No dangling native wire ends; no wire fragments without a physical or source-annotation pin; no singleton modeled net; no isolated label reported by ERC.
- All 83 physical net partitions and the entire physical-to-native pin mapping are unchanged from `ecd683d`. Adding flags did not merge rails, change a transistor pin type or introduce a no-connect marker.
- Four existing default ignored checks remain: single global label, four-way junction, SPICE model and footprint filter. They do not disable dangling-wire, missing-pin or power-input checks. No ERC exclusion is present.
- Every unrecovered ceramic value and blank footprint is covered by an active item. Local-only PIC nodes are explicitly E06, rather than counted as disconnected pins.
- **Newly sharpened inventory risk: R33.** The inherited model claims a fitted 10k pull-up between PIR supply and raw signal. Its cited IMG_2435 establishes R37/R38/R39, but does not locate R33. The old entry is retained with unverified inventory/electrical evidence, pending identification or supported removal. No new observation or measured value is claimed.

These checks establish internal consistency, not invisible copper or correct hardware behavior. `evidence/finalization_audit.json` contains the detailed geometry checks and per-component issue coverage.

## Disposition of each former item

| Item | Current disposition |
|---|---|
| E01 D2 | Local routes complete; remaining identity and ratings consolidated into I01. No additional rail sweep. |
| E02 D3 supply | Resolved; archived. |
| E03 RF/Q8 | Source-path qualification and gate drive remain; C5/C6 parallel wiring removed from the unanswered part. |
| E04 tuning | One Q3 diode-mode batch prepared; polarity/base and hidden antenna links remain. |
| E05 button | Only contact pairing and released/pressed behavior remain. |
| E06 PIC branches | RA0/C25, RC3/TP11 and RC7/TP17 onward destinations remain explicit; RF local wiring is settled. |
| E07 PIR | R33 inventory/assumed pull-up and Q2 behavior remain; J3/U7/U6 external pad mapping is settled. |
| E08 receiver | Supply switching, bias and operating transfer remain; no extra output wire inferred from the old H_RX_DETECT name. |
| E09 power | Rail levels and Q1 control require operating measurements; ERC source declarations are resolved. |
| E10 protection | Only D6 identity/breakdown/ICSP compatibility remain; routing/polarity/connector numbering are settled. |
| I01 identities | Supported equivalents and rating limits; includes D2. Exact manufacturer need not be falsely claimed. |
| I02 interfaces | LED colour/pad map and physical motor lead order remain. |
| V01 values | 44 ceramics and remaining passive-rating qualifications. L1/L2 readings retained. |
| M01 packages | LED footprint is the only blank; exact mechanical reproduction qualifications are separate. |
| D01 empty options | Local pads are mapped; candidate roles and unknown optional values remain documented limitations. J6 is an external empty interface, not proof of an omitted rail. |
| F01 extended scope | PCB/layer stack, PIR daughterboard internals and firmware are deferred, explicitly not completed. |

## Next bench action

Only Q3 is queued: six directional diode-mode measurements on labelled QL/QR/QS pads in the unchanged IMG_2433 photograph. This can constrain polarity and base position; in-circuit readings do not uniquely distinguish emitter and collector. The screen and reply worksheet are `docs/FINISHING_MEASUREMENTS.html`.

The separate R33 question asks for its physical location, not a measurement. Powered rail/waveform, capacitor and interface batches are staged in the active register and are not simultaneous requests.

## Verification

Native build/export, stock symbol/footprint checks, geometric wire audit, historical electrical evidence contracts, active-register coverage, local HTML links/JavaScript syntax and original photo hashes are checked by the build/review tools. The two refreshed PDFs are visually reviewed after rendering. Original photos and raw measurements remain unchanged. No hardware result is synthesized from a passing software check.
