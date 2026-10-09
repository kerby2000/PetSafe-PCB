# Current circuit interpretation

Schematic v0.9.32, 2026-10-09. This is the current interpretation, not a chronological log. The [previous narrative](history/cleanup_v0928/docs/RECONSTRUCTION.md) is archived; older requests there are superseded. Use [the checklist](FINISHING_CHECKLIST.html) for remaining questions.

## Power and references

BATTERY+ is the raw positive terminal before Q1. User continuity puts Q1.L, U5/MX512H pin4 and the input sides of L1/L2 on VSYS. Printed VDD is the distinct logic rail, including U5 pin1, PIC20 and V063/V064. VREF is the printed reference point, PIC4/RA2 and the confirmed receiver bias node. GND includes BATTERY (-). The Q1 PMOS/reverse-polarity role remains a candidate interpretation; source, gate and rail operating voltages are unmeasured.

L1 = 1.4 uH and L2 = 2.2 uH are user LCR readings. Their output branches are separate: H_RF_VDD after L1 and H_LDO_IN after L2. Conditions and exact magnetic parts/ratings remain unspecified. H_RX_VDD and H_PIR_VDD are descriptive local branches, not additional independently measured power supplies.

U1 uses a datasheet-derived S-1200B45 symbol. U6/C2NM supports S-812C33AMC. U6 pin5 is externally tied to pin2/VIN at 1 ohm, although internally NC in the candidate; pin4 is supported unused. R37.1 receives VDD and R37.2 reaches the U6 input branch. U6A is empty, with current native reference U106 and pins **3 input / 2 output / 1 GND**. Its output shares the fitted U6 output and produces a retained ERC conflict. Its regulator symbol does not identify an absent device.

## PIC, button and interfaces

All PIC pads have modeled local nets. PIC21/RB0 reaches TP16/Q2.S; the old VREF association was explicitly withdrawn after TP16-VREF measured 0.8 Mohm. PIC2/C25, PIC14/TP11 and PIC18/TP17 still need their onward connections or operating roles assessed. C26 reaches PIC3/RA1 with R28/R29/TP7. C25/C26 have common ground ends; C39/PIC4 belongs to VREF.

R41 is 330 ohm and its model1/right end reaches **J1 VPP**. Its model2 end joins H_BUTTON/R40.2/C35.1. The former isolated H_R41_FREE node is obsolete. R40's other end is ICSP_DAT/PIC28. S1 currently uses stock SW_Push: physical upper row TL/TR maps to native pin1/GND; lower BL/BR to native pin2/H_BUTTON. Internal common pairs and pressed/released behavior remain inferred. Old four-native-pin connector numbering is superseded.

J1 square/VPP end is pin1, then VDD2, GND3, DAT4 and CLK5. D6 routing and polarity are measured: anode GND, cathode VPP, about 0.7 V forward, OL reverse. Its G3 marking does not establish breakdown or ICSP compatibility. D4/D5 use photo-supported 5U/SD05 TVS candidates.

J3 is pin1 PIR supply, pin2 raw signal to R38, pin3 GND. Empty U7.1/2/3 map to J3.3/2/1. The PIR-to-PIC route is resolved; Q2 candidate pin functions and operating behavior remain qualified. Unsupported R33 and its assumed raw-signal pull-up have been withdrawn after photo review and user inspection. The separate PIR board's internal circuit is outside this main-board drawing.

Q9/J6/R35/R36/TP10 are DNP options in the PIC block. Q9's NPN symbol expresses a possible driver role; no fitted identity is claimed. J6.2/R36.1's onward role remains unknown.

## RF excitation and tuning

Q8/3724A uses a SIL3724A N/P MOSFET candidate. Its centre B2/native5 ground and outer-drain join have evidence. The source-supply interpretation and gate-drive headroom remain qualified; a 10-ohm measured path is not a proven copper short. C6 is in parallel with C5 across H_RF_VDD/GND by photo-supported reconstruction. C5 is 470 uF / 16 V; C6 is unmeasured.

The [IMG_2431 trace review](RF_TRACE_REVIEW.html) establishes PIC13/TP3/R10.1/R6.2/R7.1/D1.S on RF_MONITOR_PAD. D1.R/native2 joins R7.2/C9.1/U2.1 (H_RF_IN_A); D1.L/native1 retains R6.1/C8.1/U2.3 (H_RF_IN_B). The prior H_RF_CONTROL/H_D1_FREE nodes are retired. These are photo-supported connections combined with the earlier measured PIC13-to-TP3 destination, not new meter readings. With the BAV99/U2 candidates, this is consistent with opposite charge/discharge delays at the two gate-driver inputs. Actual switching timing, dead time and Q8 gate headroom are unmeasured.

Five PIC tuning controls are mapped. Q3 in-circuit readings are L->R 2.3 V and L->S latest 0.48 V (earlier 0.35 V), with all other directions OL. This does not confirm the PNP candidate or justify a MOSFET substitution; isolated-device identification remains optional under E04. The modeled PNP emitter-at-GND/nonnegative-GPIO arrangement is not an ordinary forward-operated PNP switch; device type/orientation, ground assignment or RF switching role needs review. Finish one Q3/R13/C10/C11/C12 cell, including V107 and antenna continuation, before extrapolating by symmetry. Seven measured capacitor-midpoint OL exclusions must remain separate constraints. C49 is an empty rear option now connected ANT2-to-GND; it does not establish the other antenna paths.

## Receiver

U3.5/R22.2 is VREF; R22.1 is GND. U3.6 reaches R23.1; R23.2 joins C40.1 and R42.1 at measured low resistance, retaining the independent TP4/PIC25/R44.1 association. The old R23-VREF and C40-to-output assumptions are withdrawn. Q7 supply-switch behavior and selected transistor terminals remain inferred, supported by photo traces and the 11.2 kohm R18/R19 path.

D3.L is GND, D3.R is VDD via V082 and D3.S reaches R42 at 1.2 ohm (model2/photo-selected end). Its rail association is resolved; its signal function and exact maker remain qualified. D2.R (photo upper-left) reaches C20 lower; D2.L reaches ANT2/R46 upper; D2.S reaches empty R46 lower. Diode readings support R -> S -> L junctions in circuit, without uniquely identifying the 4P device.

C23.2 and R25.1 form a series junction still named H_RX_DETECT. It **continues through R25** to RX_STAGE_LINK/R48; it is not an unconnected detector output. R47.2 and C42.2 also join that stage-link node, with R47.1 at U3.1/R27 and C42.1 photo-supported GND. R47/C42 are DNP. Receiver transfer function, bias and candidate-device behavior remain to be checked; net names alone do not justify additional wires.

## Completion criteria

The model and native drawing agree on 83 net partitions. Native geometry has zero dangling wire ends or pinless wire fragments. Zero unassigned pads and the retained U6 pin4 NC do not certify all onward routes. Five stock power-source declarations now resolve the undriven-input checks without changing physical partitions. Only the user-retained U6/U6A output conflict remains. No ERC exclusion or new NC was introduced. R33 and its two assumed endpoints have been removed; all retained physical pad memberships and mappings are unchanged.

Topology, device behavior, 44 ceramic values, LED footprint/channel map and remaining geometry are tracked separately. A routed PCB, actual layer stack, firmware and powered validation are separate milestones. [Recorded measurements](MEASUREMENTS.md) are user evidence; [library choices](LIBRARIES_AND_ALTERNATIVES.md) retain candidate qualifications.
