# Response to the independent review

2026-10-09 | v0.9.30 | Reviewed snapshot: `6ae4eaa` / v0.9.28; immediate working baseline: `f830b3a` / v0.9.29.

The [review as supplied](2026-10-09_independent_review_6ae4eaa.md) is preserved byte-for-byte; its hash and the original photographs inspected are in [the audit record](../../evidence/architect_review_v0930.json). The review is a logical audit, not new bench evidence. The intervening v0.9.29 cleanup changed no electrical partitions, so its electrical findings remained applicable.

## Changes made

Reinspection of **IMG_2431** establishes a photo-supported RF source path that the previous drawing omitted. No new meter readings were requested or invented. The [photo trace view](../RF_TRACE_REVIEW.html) shows the relevant contacts; the original image is unchanged.

| Physical endpoint | Previous model | Corrected model and evidence |
|---|---|---|
| R6 upper/model2 and R7 upper/model1 | Isolated common `H_RF_CONTROL` | `RF_MONITOR_PAD`: TP3 downward trace reaches R6 upper; the horizontal copper joins the common D1/R7 upper branch. Earlier user V049 evidence supplies PIC13/RC2 to TP3. |
| D1 single upper/native3 | `H_RF_IN_A` | `RF_MONITOR_PAD`, the common R6/R7 input. |
| D1 paired-right/native2 | Singleton `H_D1_FREE` | `H_RF_IN_A`: downward trace to U2 top-right/native1 and the R7-lower/C9-upper branch. |
| D1 paired-left/native1 | `H_RF_IN_B` | Retained at R6-lower/C8-upper/U2 top-left/native3. |

With the BAV99 and dual Schmitt-inverter candidates, this is consistent with different rising/falling delays at the two driver inputs. This is an **application inference**; neither diode identity, switching frequency, dead time nor adequate Q8 turn-off has been measured. The preserved net name `RF_MONITOR_PAD` is historical; its role is now a candidate excitation source, not a measured monitor-only input.

The resulting model has **83 partitions**, with the two obsolete local nets retired. All other physical-pad partitions are unchanged. The isolated-label ERC finding is removed by an actual traced connection. No new power flags, ERC exclusions or no-connect declarations were added.

## Finding-by-finding disposition

| Review finding | Disposition | Remaining work |
|---|---|---|
| P0 tuning transistor polarity/orientation | Accepted. All five device evidence fields and the sheet note explicitly flag the PNP emitter-at-GND interpretation as provisional. IMG_2433 shows Q3 paired-right/R13 and single-pad/C10 local copper; those joins do not need repeating. No PNP-to-NPN substitution or antenna net merge. | Constrain one Q3 cell's device polarity/base first; then its hidden antenna continuation. In-circuit diode tests do not uniquely identify emitter versus collector. Preserve all seven midpoint OL exclusions. |
| P0 missing RF excitation and D1 singleton | Local routing resolved by the photo correction above; prior measured PIC13/TP3 endpoint retained. | Timing, candidate-device behavior and antenna/load continuation remain open. No local continuity task is needed for these visible joins. |
| P1 receiver/controller path | Accepted as a functional question. IMG_2429/2434 agree with the latest C23/R25/R47/R48 routing. `H_RX_DETECT` is a C23/R25 series junction, not evidence of a missing direct MCU wire. | Evaluate the existing U3.6-R23-R42/TP4/PIC25 interface, Q7 supply and transfer function. Do not resurrect rejected R25-GND, R48-VREF, R23-VREF or C40-output joins. |
| P1 Q8 high-side turn-off | Accepted as a conditional risk. Outer-drain and centre-ground evidence retained; the earlier 10-ohm source-path result remains qualified. | Resolve source-path confidence and measure source/gate waveforms relative to board GND. No cross-conduction is claimed from unpowered data. |
| P1 U1 input/enable | Existing candidate model retained; input/enable tie is plausible. | Actual supply voltage and regulator behavior remain unmeasured. No VSYS/VDD merge or artificial power source. |
| P2 U6A DNP representation | **User explicitly chose to keep the regulator symbol and its documented ERC warning.** Keep all three copper nets and DNP classification. | No claim that the absent device is identified, or that both alternative regulators may be fitted together. |

### U6A correction to the review text

The review's before/after example swaps native pins 1 and 3. The current regulator symbol and physical crosswalk are:

| Physical U6A pad | Current native pin | Existing net |
|---|---|---|
| Single left / L | U106.3 | H_AUX_IN, after R37, shared with U6.2/U6.5 |
| Upper-right / R1 | U106.2 | H_PIR_VDD, U6.3 and J3.1 |
| Lower-right / R2 | U106.1 | GND |

These mappings have not changed. The earlier three-pad connector used different native numbering; dated raw records are retained as history, not reapplied to the current regulator symbol.

## ERC after correction

**Six findings remain:** five undriven power inputs (U1 VIN, U1 VSS, U6 VIN, U5 motor VDD, U3 V+) and the explicitly retained U6/U106 output conflict. Supply-source declarations may eventually address model semantics, but require a separately justified source model. U3 receiver supply behavior is still an electrical question. Zero ERC would not resolve candidate device identity, RF timing or missing capacitances.

## Next work, without repeating visible traces

1. Prepare one **Q3 directional diode-test** photo guide using physical pad names. Start in circuit; only consider device isolation if results are ambiguous. Diode drops constrain base/polarity, not a unique manufacturer or E/C assignment.
2. Resolve only the hidden continuation of that cell's V107 junction. The seven OL comparisons rule out assumed common midpoint buses; do not repeat a bulk via sweep.
3. Review receiver behavior using its existing confirmed controller interface. Select any remote measurement only after establishing a specific unresolved endpoint.
4. Check S1 released/pressed contact behavior if exact switch mapping is needed. Existing R41-to-VPP routing is settled.
5. After unpowered routing/device review, plan a powered rail/gate/receiver session. A multimeter cannot establish switching dead time; a scope is needed for waveform claims. Use PCB GND for an earth-referenced scope ground, not antenna or motor drive nodes.

The **44 ceramic values**, LED footprint/channel map, qualified package dimensions and original-device identities remain separate work. PCB routing, real layer stack, PIR daughterboard internals and firmware are later reproduction scope. The [current checklist](../FINISHING_CHECKLIST.html) remains the active issue register; this response does not falsely close those items.

## Validation

KiCad 10.0.5 native export/ERC, physical-to-native partition comparison, preserved measurement/negative-evidence contracts, original-photo hashes, HTML data/links and PDF inspection are recorded in `evidence/validation.json`, `evidence/architect_review_verification.json`, `evidence/current_review_verification.json` and `evidence/visual_review.json`. The live assertions verify the RF correction, unchanged other partitions and unchanged U6A crosswalk; historical checkpoints remain frozen.
