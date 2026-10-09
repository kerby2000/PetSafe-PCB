# Current circuit interpretation

This document describes v0.9.11. [The completion checklist](FINISHING_CHECKLIST.html) is the authoritative list of known unresolved work. [Earlier reasoning](history/README.md) is preserved as history, including rejected guesses.

## What is established

All 150 catalog entries are represented on one A2 sheet. Twenty stock and four authorized custom symbol definitions provide the selected pin maps. All 352 physical pad identifiers have library-number crosswalks. The native netlist matches 83 modeled net partitions; this is a file-consistency result, not proof of every board connection.

The user supplied multimeter continuity, resistance readings, clear component markings and dimensions. Visible traces and approximate front/rear photo registration provide additional evidence. A via touching a surface copper region can support a local association; its appearance cannot establish a buried net or prove a four-layer stack.

## Power path

BATTERY+ reaches Q1's single physical pad (native pin 3). Q1.L (native pin 2) supplies VSYS, which reaches MX512H pin 4 and the supply sides of L1/L2. The user confirmed these associations and that raw battery and VSYS are distinct. TP14/R43.2 remain on the raw side; the previous Q1.L-R43.2 join was explicitly rejected.

The R1A marking matches the Formosa FMOS3401A PMOS candidate, with gate 1/source 2/drain 3. Reverse-polarity protection is a supported interpretation; exact maker and gate operation remain unverified. Photo label `S` means **single pad**, not source.

Board VDD/TP103 is the separate logic rail and feeds MX512H pin 1/VCC. VREF/TP104 is separate again: user reports connect PIC21/RB0/V026, PIC4/RA2/V035 and R21.2/V071. Other VREF bias branches remain hypotheses. GND includes BATTERY (-). Candidate regulator outputs of 4.5 V and 3.3 V are datasheet ratings, not measured board voltages.

## Controller, motor and controls

Every PIC pad has a local modeled net. User continuity resolves RC4/RC5 to H-bridge INA/INB and all five tuning-control inputs: RC6-R13, RA3-R14, RA4-R15, RA5-R16, RC0-R11. RC1 reaches R18 via V053-V070; the old VREF join is rejected. RC2 reaches TP3. The [complete PIC table](../evidence/pic_gpio_status.csv) distinguishes each evidence basis.

Some connected PIC nodes still lack a known remote role, notably PIC2/C25, PIC14/TP11 and PIC18/TP17. R41.1 is isolated and neutrally named H_R41_FREE. The button already reaches PIC28 through R40; the free R41 end may instead be supply, bias or control. S1 common pairs remain provisional. J1 square-pad end is VPP: native pins 1 VPP,2 VDD,3 GND,4 DAT,5 CLK, supported by IMG_2437/2439. D6 routing and J5 A/B orientation still need resolution.

## RF drive and antenna tuning

U2/C14R supports a dual Schmitt inverter. Q8/3724A supports a complementary MOSFET candidate. V113/V115 ground its centre B2/native5; V114 is U2.T2 ground, not Q8. Earlier low-resistance readings support the joined outer Q8 pads. C6-to-output was rejected by a 400 kohm result; its 10 ohm reading toward the opposite centre pad is not proof of a direct wire.

The five control inputs are mapped, but capacitor-midpoint continuations and ANT2 are not complete. Seven OL readings reject a simple shared-midpoint assumption; no broad pair sweep remains queued. Capacitor values and transistor orientations still constrain the circuit interpretation. D1.R is also a local isolated node.

## Receiver and PIR interface

The 11.2 kohm V064-V070 measurement fits nominal R19 + R18 and supports the Q7 supply-switch hypothesis. Q7 terminal selection remains photo/circuit inference. User now confirms D3.R reaches board VDD through V082 and D3.L is GND. Only D3.R is moved off H_RX_VDD. D3.S-to-R42 reads 1.2 ohm; photo selects R42.2, with R42.1 already mapped to TP4/PIC25. The node is neutrally named H_D3_SIGNAL; its operating function is unknown. Op-amp feedback, coupling and bias branches are still partly inferred. TP6/C18.2 and U3.5/C18.1 are separate sides of a capacitor.

U6/C2NM supports S-812C33AMC; the supervisor guess based on WN23 is withdrawn. User confirms V067 to J3.1/red PIR supply. The model's J3.2 ground and J3.3 raw-signal roles, U6 external branches and Q2 interface need cross-checking. Wire colour alone does not establish a role. The separate PIR board's internal circuit is outside this main-board reconstruction.

## Reading uncertainty

Unconnected physical pads, isolated labels, incomplete onward routes, candidate identities, unmarked values and package geometry are different gaps. The checklist covers all of these, with exact open-pad and capacitor lists. Do not remove a question mark merely because a symbol exists or a plausible typical circuit can be drawn. Record deliberate assumptions explicitly if exact identity or value cannot be recovered.

## Architect review findings, 2026-10-09

U3.5 currently has only C18.1 on its net, so the reconstruction lacks an intentional DC bias-current return. Check the existing R23/R22 bias-facing pads using IMG_2434 and V079/V080; measure resistive paths separately. Preserve separation across C18 and add no invented resistor.

The modeled PNP tuning cells put their emitters at GND while their bases are GPIO-driven. That is not a conventional forward-operated PNP switch. Resolve Q3/C10/C11/C12 and its antenna path first; type, orientation, ground association or a junction-switching role may need correction. No automatic NPN substitution is justified. C11/C12 currently share both nodes: an in-circuit LCR result would be an effective parallel-network value, not individual capacitances.

H_RF_CONTROL lacks an excitation source, H_RX_DETECT lacks a downstream detector destination and Q2/TP16 lacks a modeled controller connection. H_BAT_SENSE already has a series path through R4 to PIC24; its function and confidence require review, not necessarily another wire.

Q8's P-channel source is modeled on filtered VSYS while its U2 driver uses VDD. Turn-off cannot be established from a gate-to-ground level alone. After passive routing, measure source and gate relative to GND and compute VGS. The 6.0V/4.5V example in the architect review is illustrative, not a board measurement; the fitted device and actual waveforms remain unverified.
