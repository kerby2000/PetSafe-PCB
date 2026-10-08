# PetSafe functional reconstruction, v0.4

The deliverable is one editable KiCad schematic sheet with all 150 entries in the original main-board catalog. It uses wires inside functional blocks and labels between blocks. The 150 entries include named pads, test points and unpopulated footprints; they are not 150 fitted components. The separate PIR daughterboard appears in the photos, but only its main-board connector and interface are modeled here.

The user's instruction to make calculated guesses governs this revision. The imported v0.1 documents requested a measurement-first workflow; those documents are historical reference, not instructions overriding the current task. The original ZIP, photographs, capture and source model remain available for comparison.

## Follow-up identity review

The [U6 / Q8 investigation](U6_Q8_INVESTIGATION.html) supersedes the candidate ranking below, while v0.4 retains the same U6/Q8 electrical hypotheses. RT9818A-33PB is now the leading named U6 candidate; a complementary N/P MOSFET pair is the leading Q8 role. The U6 crosswalk below is the current placeholder mapping, **not conventional SOT-23-5 numbering**: for the photographed three-lead right side, conventional numbers are R3=1, R2=2, R1=3, L1=4, L2=5. The old LDO role assignments cannot be carried into a supervisor replacement. Conditional Q8 pin numbering and comparison parts are recorded separately.

## How to read the drawing

- `H_*` names identify inferred inter-block nets. A name without this prefix is not a measurement claim: local wiring also contains hypotheses.
- `?` marks candidate identities, pin roles and estimated values. An unknown unmarked capacitor remains `?` unless a useful conventional starting value has been selected.
- All 29 original `VISUAL_LOCAL` fragments remain joined in the new model. Their source photographs remain in `original_visual_fragments` in the JSON. Even these fragments are photographic evidence, not continuity results.
- Every added link is provisional. `evidence/proposed_nets.csv` distinguishes each proposed net and the original fragments it contains. Merging several visual fragments into one net is an inference.
- Open pins mean unresolved; they do not carry fabricated no-connect flags. No power flags were added just to silence ERC.
- U2 and U3 have separate functional and supply units on this same A2 sheet. There are 21 stock definitions from the installed KiCad 10 libraries plus two user-authorized datasheet definitions, all placed or replaced through the KiCad MCP server. Library pin numbers are mapped to photographed pad IDs in `evidence/pin_crosswalk.json`.
- U1 and U5 now have datasheet-derived symbols created through MCP after explicit user authorization. Their 13 numbered pins and standard footprints were checked. U6 and Q8 still use numbered placeholders because identity is unresolved; these do not assert that the fitted parts are connectors.
- [LIBRARIES_AND_ALTERNATIVES.md](LIBRARIES_AND_ALTERNATIVES.md) records stock symbols, package choices and Western alternatives. The fitted identities remain in the reconstruction. Selecting an alternative does not authorize changing the board pin map.

## Identity candidates

Confidence describes identification, not confidence in every connected wire. Primary sources are linked in [SOURCES.md](SOURCES.md).

| Ref / visible mark | Working identity | Confidence and reason | Remaining alternative or limitation |
|---|---|---|---|
| U1 / PPEK | ABLIC S-1200B45-M5T1x, 4.5 V LDO | Strong. Manufacturer Rev.6 page 23 explicitly maps PPE to this SOT-23-5 part; fourth character is lot code. Pinout also fits input/output capacitor fragments. | Exact environmental suffix is not recoverable from this mark. Actual rail voltage and routing remain unmeasured. |
| U2 / C14R | TI SN74LVC2G14DBV, dual Schmitt inverter | Strong. Manufacturer ordering table lists C14R for the six-lead DBV package. Two outputs fit the two 220-ohm resistors near Q8. | Package orientation is inferred from the photographed pin-one dot. This is not a single-gate five-pin device. |
| U3 / SGM8542XS | SGMICRO dual op-amp | Strong; readable full marking and standard eight-pin dual-op-amp arrangement. | External signal path and filter values remain hypotheses. |
| U4 / PIC16F18855 | Microchip PIC16F18855, 28 pins | Strong, supplied capture and photograph. | Peripheral pin select means a typical application cannot establish the board's GPIO map. |
| U5 / MX512H | Mixic dual-input H-bridge | Strong, readable marking and manufacturer pin diagram. | J5 A/B order and MCU control destinations are not visible enough to establish. |
| Q2 / 1FW56 | BC847B NPN | Good candidate; Nexperia identifies 1F plus a manufacturing-site character. | Manufacturer, lot interpretation and physical orientation still need corroboration. |
| Q7 / 3GW54 | BC857C PNP | Good candidate; Nexperia identifies 3G plus a manufacturing-site character. | Switched receiver supply role is inferred. |
| Q1 / R1A | MMBT3904-class NPN | Tentative. Common NPN function and 1A-family marking are compatible. | Current Diodes datasheet does not uniquely establish the full R1A mark. Keep exact identity provisional. |
| Q3/Q4/Q5/Q6/Q11 / 2H | MMBTA55/FMMTA55-family PNP | Plausible. Taitron's manufacturer catalog lists MMBTA55 with 2H marking. Five repeated cells suggest switched capacitance. | PBSS5140T is another PNP candidate; the short code is not globally unique. Neither exact part nor B/C/E orientation is certain. |
| D1 / A7 | BAV99 series dual diode | Good candidate. Nexperia lists A7 and the expected SOT23 dual-series topology. | Photo-to-pin orientation remains inferred. |
| D2/D3 | Dual clamp networks | Low confidence, role-based placeholders. | Diode arrangement and polarity need better evidence; no exact product is asserted. |
| Q8 / 372A | Dual/complementary RF switching device | Function-level candidate only: paired 220-ohm drives from U2 support two switching inputs. | Dual BJT and complementary MOSFET arrangements both remain possible. No package-compatible exact ID was established. B3 as RF output is particularly weak; power pads remain open. |
| U6 / WN23? | Five-pin auxiliary LDO, selected drawing hypothesis | Low confidence. Capacitors C36/C37 and the local interface suggest a small rail circuit. | WN also appears in historical Richtek marking material for RT9818A-33PB, a voltage supervisor. Supervisor topology would invalidate the selected LDO pin roles. No 3.3 V output is claimed. |

## Physical pad mapping

Original physical identifiers are kept so an identity correction does not silently renumber the evidence.

| Device | Proposed photographed-pad to datasheet-pin map |
|---|---|
| U1 | L1=1 VIN, L2=2 VSS, L3=3 EN, R1=5 VOUT, R2=4 NC |
| U2 | T1=3 2A, T2=2 GND, T3=1 1A, B1=4 2Y, B2=5 VCC, B3=6 1Y |
| U3 | 1 OUTA, 2 -A, 3 +A, 4 VSS, 5 +B, 6 -B, 7 OUTB, 8 VDD |
| U5 | 1 logic VCC, 2 INA, 3 INB, 4 motor VDD, 5 OUTB, 6/7 GND, 8 OUTA |
| Q1/Q2 and tuning PNPs | R=base, L=emitter, S=collector, provisional |
| Q7 | L=base, R=emitter, S=collector, provisional |
| D1 | L=pin 1/anode 1, R=pin 2/cathode 2, S=pin 3/midpoint, provisional |
| U6 | Selected LDO orientation only: R1=VIN, R2=GND, R3=EN, L1=OUT, L2=NC. These are not established RT9818 functions. |

KiCad requires numerical reference endings. C1A/C2A/U6A are C101/C102/U106 in the native file, with the original reference in a property and visible value. GND/GND_RF/VDD/VREF/ANT1/ANT2/BATP/BATN are TP101 through TP108. This is reference normalization, not additional physical components.

## Functional decisions and calculations

### H01 - main supply

Selected path: battery positive -> L2 -> U1, with EN tied to its input and nominal 4.5 V output distributed as H_VDD. C1=1 uF and C2=4.7 uF are design starting values, not recovered markings. ABLIC permits small ceramic input/output capacitors; the larger proposed output bulk value also supports the MX512H logic-supply decoupling requirement. The original U1.R2/R1.2/C3.2 fragment is retained, but R1/R2/C3/C4 are empty option footprints. Pin 4 is NC for the identified regulator, not an invented feedback input. Ground pads across blocks are provisionally unified.

### H02/H03 - controller, programming and battery sense

PIC power, crystal and ICSP functions come from the 28-pin datasheet. The two photographed crystal fragments are retained. The visible oscillator marking is 20 MHz. C30/C31=18 pF are provisional: equal 18 pF capacitors give 9 pF in series, and approximately 3 pF stray would yield a 12 pF effective load. The crystal's actual specified load is unknown.

R3=R4=330 kohm suggests battery sensing: Vout=VBAT/2 and I=VBAT/660 kohm, approximately 3 V and 9.1 uA at a hypothetical 6 V battery. No ADC pin is assigned solely from this calculation. ICSP mapping is inferred from datasheet functions and the named header pads. Remaining GPIOs are open rather than arbitrarily numbered.

### H04/H05/H06 - motor, discrete interface and button

U5 retains separate logic and motor supplies. The datasheet application has at least 4.7 uF logic decoupling; C34 is proposed as local 100 nF, supported by the proposed C2 bulk capacitor. C33=1 uF is a starting motor-supply bypass value. Motor A/B, button pull-up/debounce, and Q1 interface wiring are plausible arrangements, not recovered hidden tracks. R44=15 kohm is conditional on reading its mark as EIA-96 `18C` (150 x 100). R41's marking is insufficiently clear to assign a numerical value.

### H07/H08/H09 - RF excitation

The selected U2 mapping gives two Schmitt outputs through R8/R9=220 ohm to Q8's two upper outer pads. The supply unit and bypass capacitor are drawn explicitly. D1 is a BAV99 candidate; its shaping network remains speculative. Q8 is left as a physical-pad block because choosing a specific transistor pair would invent pin functions. B3 -> R5 -> antenna is a low-confidence proposed continuation. Q8's other supply/output pads remain unresolved, so the RF power stage is not a complete executable circuit.

L1/C5/C6 are treated as an RF supply filter, and LED1 as a two-channel indicator. LED polarity, common connections and spare R10 monitor routing are low-confidence working choices.

### H10/H11/H12 - receiver

R26=120 kohm and R48=5.6 kohm form the selected first-stage non-inverting feedback pair; R24=120 kohm and R23=5.6 kohm form the second. Each nominal low-frequency gain is 1+120/5.6 = 22.43; their ideal product is about 503 (54 dB). With the SGM8542's approximately 1.1 MHz gain-bandwidth, a simple gain/GBW estimate gives roughly 49 kHz per stage. That is an estimate, not proof of the operating carrier frequency or filter response. Unknown feedback capacitors can reduce bandwidth further.

R21/R22 create a provisional half-supply bias; R28 supplies the first input's DC return and R29 the second input's DC return. Input/interstage coupling, clamp orientation, C19/C20/C21/C22/C23/C40 functions and the output detection path are low-confidence. R29=15 kohm is conditional on the `18C` reading. Both stages have explicit feedback and input bias paths; this makes the chosen hypothesis electrically interpretable without pretending that the photos uniquely establish it.

Q7 is proposed as a receiver supply switch, with R18 feeding its emitter and R20 in series after its collector. Q7/R20's two sides are separate nets; no resistor has been accidentally shorted by sharing a label.

### H13 - antenna tuning

Five repeated PNP-controlled branches are selected. Their capacitor groupings follow front/rear placement:

| Switch | Top capacitor | Other front capacitor | Rear capacitor |
|---|---|---|---|
| Q3 | C10 | C11 | C12 |
| Q4 | C13 | C14 | C15 |
| Q5 | C16 | C29 | C38 |
| Q6 | C43 | C44 | C45 |
| Q11 | C46 | C47 | C48 |

Selected topology is Ctop in series with (Cfront || Crear). The rear photo suggests a branch via and common broad plane, but does not prove this network. Its effective capacitance is Ctop*(Cfront+Crear)/(Ctop+Cfront+Crear), or 2C/3 for equal values. Three in parallel would give 3C; three in series would give C/3. These materially different alternatives remain recorded, not silently discarded.

Resonant total capacitance is C=1/((2*pi*f)^2*L). Neither antenna inductance nor operating frequency is established from these files, so numerical capacitor values and binary weighting are not invented. ANT_A/ANT_B naming, transistor orientation and controller line destinations remain hypotheses.

### H14/H15 - PIR interface

U6 is shown in a generic LDO application with input/output capacitors, explicitly provisional because a voltage supervisor is also a plausible identity. Q2 is an NPN input stage with base resistance, pull-down and collector pull-up. J3's power/ground/signal assignment is inferred; the daughterboard's internal components have not been traced. VREF remains an unassigned named test pad. The untraced D4/D5/D6 and spare footprints are displayed without invented ties.

## Validation and limits

Native KiCad 10.0.5 loaded the schematic and exported one-page A2 vector PDF, SVG and XML netlist. All 150 references and 352 physical pins are retained; 154 drawn symbol units represent the same 150 entries. The validator translates the documented physical-pad crosswalk and compares entire pin-set partitions against the native netlist, checks all 29 original fragments and verifies all 26 source-photo checksums. It found no unintended multi-pin merges or missing proposed net partitions.

ERC has 83 findings: 63 unconnected physical pins, 14 isolated pin labels, four undriven power checks and two undriven motor-control inputs. No off-grid endpoints or dangling wire ends remain. These findings are reported, not excluded by settings. U1/U5 now carry datasheet pin types. The three additional findings versus v0.3 are exposed by those pin types; all 81 net partitions remain unchanged. U6/Q8 placeholder pins remain passive with limited electrical checking. The native file has not been opened in the GUI. Hardware verification, exact layer count, dimensioned footprint placement, routed PCB generation and firmware recovery were not performed.

This is a reviewable reconstruction hypothesis, not a confirmed replacement-board design. The remaining high-value questions are the exact Q8 and U6 identities and the hidden PIC-to-block routes. No broad measurement campaign is required to review the work already completed.

## Remaining completion items, v0.4

All 150 main-board catalog entries are represented. **No further exact-symbol files are missing for the confidently identified ICs.** U1/U5 are now completed from datasheets through MCP. The remaining work is identification, values and hidden connectivity:

| Parts / area | Remaining uncertainty | Current working choice |
|---|---|---|
| U6, WN23 | Function, physical numbering and reset/supply routes | RT9818A-33PB supervisor leads the candidates. The retained old LDO drawing and mirrored placeholder map require revision before a supervisor is inserted. |
| Q8, 372A | Exact device and six-pin assignment | Complementary MOSFET pair leads; DMC3071LVT is only a topology comparison. Three pads remain unresolved. |
| D2/D3 | Internal diode arrangement and polarity | BAV99-style clamp network is an assumption. |
| D4/D5/D6 | Diode type, polarity and connections | Standard diode symbols present; all six pads remain unresolved. |
| LED1 / S1 | LED emitter configuration/polarity; switch common pairs | Standard symbols present, physical mapping provisional. |
| Q1/Q2/Q7 and repeated 2H transistors | Candidate identity and orientation | Existing stock BJT symbols; identity strength varies and is documented above. |
| R41, L1/L2, unmarked capacitors | Ambiguous resistor code, bead versus inductor, capacitance and package sizes | Standard passive symbols present. Proposed decoupling values are estimates; RF filter/tuning values remain unknown. C27/C41 also lack a circuit role. |
| PIC and block interfaces | Exact GPIO destinations and hidden tracks | 19 PIC pads remain open. Net names indicate intended functions, not recovered MCU assignments. |
| PIR daughterboard | Internal components and routes | Only the J3 interface is represented; daughterboard internals are outside the current main-board revision. |

The 63 open physical pins include 27 on unpopulated/DNP entries; the other 36 include named test pads. They are not 63 missing parts. U7/U6A/Q9 and other DNP entries do not require identifying a fitted chip. The machine-readable list is `evidence/completion_status.json`. Further photo/datasheet inference can continue without a broad measurement campaign. A completely confirmed schematic cannot be claimed from missing identity, value and buried-trace evidence.
