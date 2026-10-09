# Current circuit interpretation

This document describes v0.9.15. [The completion checklist](FINISHING_CHECKLIST.html) is the authoritative list of known unresolved work. [Earlier reasoning](history/README.md) is preserved as history, including rejected guesses.

## What is established

All 150 catalog entries are represented on one A2 sheet. Twenty stock and four authorized custom symbol definitions provide the selected pin maps. All 352 physical pad identifiers have library-number crosswalks. The native netlist matches 83 modeled net partitions; this is a file-consistency result, not proof of every board connection.

The user supplied multimeter continuity, resistance readings, clear component markings and dimensions. Visible traces and approximate front/rear photo registration provide additional evidence. A via touching a surface copper region can support a local association; its appearance cannot establish a buried net or prove a four-layer stack.

## Power path

BATTERY+ reaches Q1's single physical pad (native pin 3). Q1.L (native pin 2) supplies VSYS, which reaches MX512H pin 4 and the supply sides of L1/L2. The user confirmed these associations and that raw battery and VSYS are distinct. TP14/R43.2 remain on the raw side; the previous Q1.L-R43.2 join was explicitly rejected.

The R1A marking matches the Formosa FMOS3401A PMOS candidate, with gate 1/source 2/drain 3. Reverse-polarity protection is a supported interpretation; exact maker and gate operation remain unverified. Photo label `S` means **single pad**, not source.

Board VDD/TP103 is the separate logic rail and feeds MX512H pin 1/VCC. VREF/TP104 is separate again: user reports connect PIC4/RA2/V035 and R21.2/V071. PIC21/RB0/V026 was explicitly withdrawn from VREF in v0.9.16 and now reaches TP16/Q2. U3.5 and R22 D/left/model2 are now measured to VREF at 1 ohm. Other VREF bias branches remain individually qualified; the R23 tie was rejected. GND includes BATTERY (-). Candidate regulator outputs of 4.5 V and 3.3 V are datasheet ratings, not measured board voltages.

## Controller, motor and controls

Every PIC pad has a local modeled net. User continuity resolves RC4/RC5 to H-bridge INA/INB and all five tuning-control inputs: RC6-R13, RA3-R14, RA4-R15, RA5-R16, RC0-R11. RC1 reaches R18 via V053-V070; the old VREF join is rejected. RC2 reaches TP3. The [complete PIC table](../evidence/pic_gpio_status.csv) distinguishes each evidence basis.

Some connected PIC nodes still lack a known remote role, notably PIC2/C25, PIC14/TP11 and PIC18/TP17. R41.1 is isolated and neutrally named H_R41_FREE. The button already reaches PIC28 through R40; the free R41 end may instead be supply, bias or control. S1 common pairs remain provisional. J1 square-pad end is VPP: native pins 1 VPP,2 VDD,3 GND,4 DAT,5 CLK, supported by IMG_2437/2439. D6 routing/polarity is measured in v0.9.20; exact D6 breakdown/type and J5 A/B orientation remain uncertain.

## RF drive and antenna tuning

U2/C14R supports a dual Schmitt inverter. Q8/3724A supports a complementary MOSFET candidate. V113/V115 ground its centre B2/native5; V114 is U2.T2 ground, not Q8. Earlier low-resistance readings support the joined outer Q8 pads. C6-to-output was rejected by a 400 kohm result; its 10 ohm reading toward the opposite centre pad is not proof of a direct wire.

The five control inputs are mapped. ANT2 now has confirmed continuity to D2.L and R46's upper pad; capacitor-midpoint continuations are still incomplete. Seven OL readings reject a simple shared-midpoint assumption; no broad pair sweep remains queued. Capacitor values and transistor orientations still constrain the circuit interpretation. D1.R is also a local isolated node.

## Receiver and PIR interface

D2's three local routes are resolved by user reports: R (upper-left/native2) to C20's lower end/model2 at 1 ohm; L (upper-right/native1) to ANT2 and R46 upper/model1; S (single lower/native3) to R46 lower/model2. R46 is empty, so these last two nodes remain separate. S-ANT2 reads OL; S-GND 700 kohm and S-VREF 1.32 Mohm establish no direct rail connection. The six diode readings support series junctions R -> S -> L in circuit, with R46 as an unpopulated shunt option across S-L. Exact 4P identity, ratings and package numbering remain uncertain. Existing C20/C19/R28/U3.3 links on RX_A_PLUS are still hypotheses beyond the measured D2-C20 pair.

The 11.2 kohm V064-V070 measurement fits nominal R19 + R18 and supports the Q7 supply-switch hypothesis. Q7 terminal selection remains photo/circuit inference. User now confirms D3.R reaches board VDD through V082 and D3.L is GND. Only D3.R is moved off H_RX_VDD. D3.S-to-R42 reads 1.2 ohm; photo selects R42.2, with R42.1 already mapped to TP4/PIC25. The node is neutrally named H_D3_SIGNAL; its operating function is unknown. Op-amp feedback, coupling and bias branches are still partly inferred. TP6/C18.2 and U3.5/C18.1 are separate sides of a capacitor.

U6/C2NM supports S-812C33AMC; the supervisor guess based on WN23 is withdrawn. User confirms V067 to J3.1/red PIR supply. User now measures J3.3-GND at 1 ohm and J3.2-GND at 290 kohm. Pin3 is ground. The next batch establishes pin2 to R38 K/right/model1 at 1 ohm and the other R38 end at 10 kohm; this agrees with the marked 10k value. The R33 branch, Q2/R39 interface and Q2/TP16 onward route remain independently qualified. The former ground/raw assignments are withdrawn. U6 external branches and the Q2 interface remain partly inferred. The separate PIR board's internal circuit is outside this main-board reconstruction.

## Reading uncertainty

Unconnected physical pads, isolated labels, incomplete onward routes, candidate identities, unmarked values and package geometry are different gaps. The checklist covers all of these, with exact open-pad and capacitor lists. Do not remove a question mark merely because a symbol exists or a plausible typical circuit can be drawn. Record deliberate assumptions explicitly if exact identity or value cannot be recovered.

## Architect review findings, 2026-10-09

The missing U3.5 DC return is resolved: U3.5-VREF and U3.5-R22 D/left each read 1 ohm. The R22 E/right/model1 end reads 10 kohm to U3.5 and is now directly measured to GND at 1 ohm. Both R23 ends read 270-289 kohm to U3.5, rejecting the old R23-VREF tie. R23 B/left/model1 is now measured to U3.6 at 1 ohm; C/right/model2 is 5.6 kohm away, agreeing with its marking. R23.2 is now measured to C40 lower/model1 and R42 upper/model1 at 1 ohm each. C40 no longer belongs to the old inferred C23/R25 detector-output grouping. The earlier R42.1-TP4/PIC25 association remains separately supported by prior user reports. An extra U3.6-to-R22 E/GND reading of 400 kohm establishes no direct ground join. R23 C to both C18 ends and TP6 reads 300/400/600 kohm, rejecting those direct joins. All four batches are complete; see evidence/u3_r23_batch3_20261009.json and evidence/u3_r23_batch4_20261009.json. These in-circuit readings do not replace marked resistor values. Original C18.1 local connectivity is retained on VREF; TP6 stays separate across C18. See evidence/u3_j3_measurements_20261009.json and evidence/u3_j3_batch2_20261009.json. The 400 kohm reading is an in-circuit path, not a new component value.

The modeled PNP tuning cells put their emitters at GND while their bases are GPIO-driven. That is not a conventional forward-operated PNP switch. Resolve Q3/C10/C11/C12 and its antenna path first; type, orientation, ground association or a junction-switching role may need correction. No automatic NPN substitution is justified. C11/C12 currently share both nodes: an in-circuit LCR result would be an effective parallel-network value, not individual capacitances.

H_RF_CONTROL lacks an excitation source, H_RX_DETECT lacks a downstream detector destination and Q2/TP16 now reaches PIC21/RB0 by user correction (v0.9.16). H_BAT_SENSE already has a series path through R4 to PIC24; its function and confidence require review, not necessarily another wire.

Q8's P-channel source is modeled on filtered VSYS while its U2 driver uses VDD. Turn-off cannot be established from a gate-to-ground level alone. After passive routing, measure source and gate relative to GND and compute VGS. The 6.0V/4.5V example in the architect review is illustrative, not a board measurement; the fitted device and actual waveforms remain unverified.

## U7 and PIR route follow-up, v0.9.16

The user measured the three corresponding physical columns of J3 and the empty U7 footprint as connected. The square pad is at opposite ends, so the local schematic numbering is U7.1-J3.3/GND, U7.2-J3.2/H_PIR_RAW, U7.3-J3.1/H_PIR_VDD. No numeric resistance was supplied for these pairs; U7 stays DNP. All three former U7 open pads are resolved.

B18 TP16-TP11 and B19 TP16-TP17 each read 400 kohm. These are rejected direct connections, not new 400k components. TP16 still needs its controller destination; the next candidate is PIC2/RA0 at the right end of C25. The Q2-to-TP16 and C25-to-PIC2 local traces are already visible; only their possible hidden interconnection requires the meter. Evidence: `evidence/pir_batch5_u7_20261009.json`.

The subsequent user report identifies PIC21/RB0 as TP16's destination, and Q2's upper-right pad as the R38 interface. Those local transistor traces are accepted from the photo. The new PIC21 report conflicts with the implication of the older PIC21/V026/VREF mapping: no net merge is made until TP16-to-VREF is checked. The C25 candidate B20 is cancelled. See `evidence/pic21_tp16_followup_20261009.json`.

The conflict is now resolved: TP16-to-VREF = 0.8 Mohm, and the user explicitly calls PIC21-VREF a mistake. PIC21 moves to H_PIR_SIG / TP16 / Q2.S. V026 retains its earlier PIC21 association; its obsolete V071/VREF grouping is removed. V035/RA2 and V071/R21 remain on VREF. No further PIR-to-PIC routing check is required; earlier pending/C25 instructions in this chronological record are superseded.

## v0.9.17 - C25/C26 controller connections

v0.9.17 user-annotated photo: C25 right pad/model1 -> PIC2/RA0; C26 right pad/model1 -> PIC3/RA1. Left pads/model2 are common, retaining earlier V029-GND evidence. No new numeric resistance or capacitance supplied. C26 joins the existing RA1/R28/R29/TP7 net, separate from RA0 and VREF. The supplied image is preserved at `photos/user_updates/C25_C26_PIC_mapping_20261009.png`; structured evidence: `evidence/c25_c26_mapping_20261009.json`. C26 is removed from the unresolved-pad list. The native drawing groups the three PIC input capacitors beside RA0/RA1/RA2 with direct wires and a shared GND return. No new rail, component value or meter reading is inferred.

## v0.9.18 - C6 parallel with C5

v0.9.18: C6 is reconstructed in parallel with C5 from the user proposal and photos IMG_2431/IMG_2432. C6 upper pad/model1 joins the C5-positive supply copper (H_RF_VDD, after L1); lower pad/model2 joins GND. Photo-supported, not a new meter-confirmed connection. C6 capacitance remains unknown. Earlier 400 kohm output exclusion and 10 ohm Q8-supply-path reading are retained; the latter does not independently prove Q8 source wiring. Structured evidence: `evidence/c5_c6_parallel_20261009.json`. This resolves C6.1 in the working reconstruction without claiming a new continuity measurement. Q8 identity/supply-path and gate-drive qualifications remain under E03.

## v0.9.19 - receiver option footprints and interstage junction

v0.9.19 user annotated local copper: R47 left -> U3.1/R27 right; R47 right + C42 lower + R25 lower + R48 right share RX_STAGE_LINK. C42 upper -> GND inferred from continuous copper beside U3.4 in IMG_2429/2434. R25-GND and R48-VREF old assumptions withdrawn. R47/C42 remain DNP. No meter reading supplied. The grounded C42 upper pad is agent photo inference; the other new joins come from the user annotation. See [structured evidence](../evidence/r47_c42_routing_20261009.json). Empty R47 does not short U3 output to this junction, and empty C42 does not ground it.

## v0.9.20 - D6 and U6 open-pad results

v0.9.20: U6.5-U6.2 measured 1 ohm (B28). User annotation also joins physical L2/native5 to R37 upper/model2 and empty U6A single/native1. U6.4/L1 marked NC by user and appears as an isolated surface stub in original photos. Candidate pin5 is internally NC but externally tied to VIN; pin4 remains unused. v0.9.20 B22-B27: upper photo contact V -> GND, lower W -> VPP, each 1 ohm. B29 red V/black W about 0.7V; B30 reverse OL. Supports A=V/GND (pin2), K=W/VPP (pin1). G3 identity and Zener breakdown remain unverified; no 3.9V measurement. Recorded readings and probe definitions: [batch results](../evidence/d6_u6_open_pad_results_20261009.json). TP9 has no established physical location and is under inventory review.

## v0.9.21 - J6/Q9 option and button routing

v0.9.21 annotated photo: J6 left/model1 joins Q9 single/native3 and R36 right/model2. J6 right/model2 joins R36 left/model1. PIC26/RB5-TP10-R35 upper; R35 lower-Q9 paired-left; paired-right via V021 is GND. All J6/Q9/R35/R36 options remain DNP. R36 left/J6 right onward rail is not established by this annotation.

v0.9.21 user annotated S1 upper-right to C35 upper/model2 (GND via prior V018); lower-right to C35 lower/model1, R40 lower/model2 and R41 left/model2. User explicitly confirms R41 right/model1 reaches J1 VPP/MCLR. Correct physical-to-native switch mapping TL=1, TR=3, BL=2, BR=4. Top-row/bottom-row common pairs remain a tactile-switch hypothesis; released/pressed behavior has not been measured.

See [annotated routing record](../evidence/j6_q9_button_routing_20261009.json). J6 numbering is a documented local convention: left hole 1, right hole 2; no fitted connector pinout is claimed.

## v0.9.22 - U6A option fully mapped

v0.9.22 user annotated U6A option: single left pad/model L/native U106.1 joins U6 pin5 and the existing input node after R37; upper-right/model R1/native2 joins J3.1 (red PIR wire); lower-right/model R2/native3 joins GND. All three external pads mapped, option remains DNP. User called the input VDD; retain VDD -> R37 (22 ohm) -> H_AUX_IN because the annotation ends at U6 pin5 and prior B28 confirms pin5-pin2, not a bypass across R37. No fitted IC identity or voltage measurement implied.

See [three-pad routing evidence](../evidence/u6a_three_pad_routing_20261009.json). U106 is the KiCad reference for PCB marking U6A.
