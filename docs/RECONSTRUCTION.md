# PetSafe functional reconstruction, v0.8

The deliverable is one editable KiCad schematic sheet with all 150 entries in the original main-board catalog. It uses wires inside functional blocks and labels between blocks. The 150 entries include named pads, test points and unpopulated footprints; they are not 150 fitted components. The separate PIR daughterboard appears in the photos, but only its main-board connector and interface are modeled here.

The user's instruction to make calculated guesses governs this revision. The imported v0.1 documents requested a measurement-first workflow; those documents are historical reference, not instructions overriding the current task. The original ZIP, photographs, capture and source model remain available for comparison.

## Follow-up identity review

The [corrected marking report](U6_Q8_MARKING_UPDATE.md) supersedes the historical WN23/372A interpretation. Sharp photos read C2NM and 3724A. U6 is a strong ABLIC S-812C33AMC 3.3 V regulator candidate; Q8 is a complementary N/P MOSFET with SIL3724A as a datasheet candidate. U6 ground is supported by user resistance readings, while input/output and some Q8 copper routing remain inferred.

## How to read the drawing

- `H_*` names identify inferred inter-block nets. A name without this prefix is not a measurement claim: local wiring also contains hypotheses.
- `?` marks candidate identities, pin roles and estimated values. An unknown unmarked capacitor remains `?` unless a useful conventional starting value has been selected.
- All 29 original `VISUAL_LOCAL` fragments remain joined in the new model. Their source photographs remain in `original_visual_fragments` in the JSON. Even these fragments are photographic evidence, not continuity results.
- New links carry individual evidence classes; some pairwise GPIO connections are now user-reported multimeter checks. `evidence/proposed_nets.csv` distinguishes each proposed net and the original fragments it contains. Merging several visual fragments into one net is an inference.
- Open pins mean unresolved; they do not carry fabricated no-connect flags. No power flags were added just to silence ERC.
- U2/U3 have separate functional and supply units; Q8 has separate N/P units on this same A2 sheet. There are 20 stock definitions from the installed KiCad 10 libraries plus four user-authorized datasheet definitions, all placed or replaced through the KiCad MCP server. Library pin numbers are mapped to photographed pad IDs in `evidence/pin_crosswalk.json`.
- U1 and U5 now have datasheet-derived symbols created through MCP after explicit user authorization. Their 13 numbered pins and standard footprints were checked. U6/Q8 now have datasheet-backed candidate symbols; their 11 pins and stock package footprints are checked independently in the native netlist.
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
| D3 / A7 | BAV99 series dual diode candidate | User-confirmed A7; manufacturer marking match. | Board orientation and clamp routes remain inferred. |
| D2 / 4P | Unidentified three-terminal part | Zetex FMMT2907R is an exact code/package lead, not a verified identity. | Numbered stock placeholder; all three guessed clamp ties withdrawn. |
| Q8 / 3724A | SIL3724A? complementary N/P MOSFET | Strong device-type match: MCC datasheet explicitly shows mark and six-pin map. | Fitted manufacturer unconfirmed; external copper connections inferred. |
| U6 / C2NM | ABLIC S-812C33AMC-C2NT2x, 3.3 V regulator | Strong C2N code/package match; pin1=C/R3 supported by low resistance to ground. | Rail voltage and input/output routing unverified; RT9818 withdrawn. |

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
| U6 | R3=1 VSS (probe C), R2=2 VIN (B), R1=3 VOUT (A), L1=4 NC, L2=5 NC |
| Q8 | T3=1 G_N, T2=2 S_P, T1=3 G_P, B1=4 D_P, B2=5 S_N, B3=6 D_N |

KiCad requires numerical reference endings. C1A/C2A/U6A are C101/C102/U106 in the native file, with the original reference in a property and visible value. GND/GND_RF/VDD/VREF/ANT1/ANT2/BATP/BATN are TP101 through TP108. This is reference normalization, not additional physical components.

## Functional decisions and calculations

### H01 - main supply

Selected path: battery positive -> L2 -> U1, with EN tied to its input and nominal 4.5 V output distributed as H_VDD. C1=1 uF and C2=4.7 uF are design starting values, not recovered markings. ABLIC permits small ceramic input/output capacitors; the larger proposed output bulk value also supports the MX512H logic-supply decoupling requirement. The original U1.R2/R1.2/C3.2 fragment is retained, but R1/R2/C3/C4 are empty option footprints. Pin 4 is NC for the identified regulator, not an invented feedback input. Ground pads across blocks are provisionally unified.

### H02/H03 - controller, programming and battery sense

PIC power, crystal and ICSP functions come from the 28-pin datasheet. The two photographed crystal fragments are retained. The visible oscillator marking is 20 MHz. C30/C31=18 pF are provisional: equal 18 pF capacitors give 9 pF in series, and approximately 3 pF stray would yield a 12 pF effective load. The crystal's actual specified load is unknown.

R3=R4=330 kohm suggests battery sensing: Vout=VBAT/2 and I=VBAT/660 kohm, approximately 3 V and 9.1 uA at a hypothetical 6 V battery. No ADC pin is assigned solely from this calculation. ICSP mapping is inferred from datasheet functions and the named header pads. Remaining GPIOs are open rather than arbitrarily numbered.

### H04/H05/H06 - motor, discrete interface and button

U5 retains separate logic and motor supplies. The datasheet application has at least 4.7 uF logic decoupling; C34 is proposed as local 100 nF, supported by the proposed C2 bulk capacitor. C33=1 uF is a starting motor-supply bypass value. Motor A/B, button pull-up/debounce, and Q1 interface wiring are plausible arrangements, not recovered hidden tracks. R44=15 kohm is conditional on reading its mark as EIA-96 `18C` (150 x 100). R41 is nominal 330 ohm from the user-confirmed 331 marking (33 x 10^1); this resolves the prior ambiguous reading.

### H07/H08/H09 - RF excitation

U2's Schmitt outputs drive the gates of the 3724A N/P MOSFET candidate through R8/R9=220 ohm. Normal transistor symbols replace the numbered placeholder. The selected source rails and shared drains form a plausible push-pull driver into R5 and the antenna. D-E=2 ohm supports joined drains and S-G=2 ohm supports the N-source ground return. E-F=400 kohm refutes the proposed C6 upper-pad/output tie, so that wire has been removed and C6.1 remains unresolved after F-P=10 ohm and F-G=300 kohm supported a supply-related node without establishing the exact path. L1/C5 and the P-source rail remain a proposed supply filter.

D1 is a BAV99 candidate; its shaping network, LED polarity/common connections and spare R10 monitor routing remain low-confidence choices.

### H10/H11/H12 - receiver

R26=120 kohm and R48=5.6 kohm form the selected first-stage non-inverting feedback pair; R24=120 kohm and R23=5.6 kohm form the second. Each nominal low-frequency gain is 1+120/5.6 = 22.43; their ideal product is about 503 (54 dB). With the SGM8542's approximately 1.1 MHz gain-bandwidth, a simple gain/GBW estimate gives roughly 49 kHz per stage. That is an estimate, not proof of the operating carrier frequency or filter response. Unknown feedback capacitors can reduce bandwidth further.

R21/R22 retain a provisional bias hypothesis. In v0.8 the user identifies R28/R29 free ends and TP7 on RA1; those ends are no longer tied to the other guessed bias nodes. The purpose of this GPIO-controlled/shared reference remains unresolved. Input/interstage coupling, clamp orientation, C19/C20/C21/C22/C23/C40 functions and the output detection path are low-confidence. R29=15 kohm is conditional on the `18C` reading. Both stages have explicit feedback and input bias paths; this makes the chosen hypothesis electrically interpretable without pretending that the photos uniquely establish it.

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

The corrected C2NM marking supports an S-812C33AMC regulator: R37 feeds pin2 VIN, C36 bypasses the input, pin3 VOUT feeds C37 and the PIR rail, and pin1 VSS is ground. The user reports C/R3 to G at 2.7 ohm, B/R2 at 34 kohm and A/R1 at 4.2 kohm; shorted tips later read 0.5 ohm. C is likely ground, with contact resistance uncertainty. 3.3 V is the candidate rating, not a measured voltage. NC4/5 remain open in the drawing because their board ties are unknown.

Q2 is a proposed NPN input stage with base resistance, pull-down and collector pull-up. J3 power/ground/signal assignments remain inferred; daughterboard internals are not traced. D4/D5 carry SD05 5 V TVS candidates; their lower pads are now photo-traced to PIC pins 27/28 respectively. Their opposite pads now join photo-matched VSS-associated rear copper (v0.8). D6 is a provisional MMSZ5228BS 3.9 V Zener, with PZU2.4B as a 2.4 V alternative; both routes remain unresolved. These candidate identities and polarities are not electrically verified.

## Validation and limits

Native KiCad 10.0.5 exports one A2 sheet with 150 references, 155 symbol units and 352 physical pads. The final native pin partitions match all 89 modeled nets. All 29 original visual fragments and all 26 original photo checksums are retained. Twenty stock definitions and four project-local definitions match their registered library graphics and pins. Manufacturer pin-table contracts independently check U1/U5/U6/Q8 in the exported netlist.

ERC reports 65 open findings: 46 unconnected pins, 11 isolated labels, five undriven power checks and three undriven inputs (two motor and LED common). No off-grid endpoints, dangling wire ends or unintended multi-pin net merges remain. U6 and Q8 unpowered resistance readings are recorded; C6 exact path remains unresolved. Functional tests, voltage measurements, completion of GPIO tracing, physical PCB reconstruction and firmware recovery remain undone.

## Remaining completion items, v0.8

All 150 main-board catalog entries are represented. **No further exact-symbol files are missing for the confidently identified ICs.** U1/U5 are now completed from datasheets through MCP. U6/Q8 candidates are also implemented. The remaining work is identity confirmation, values and hidden connectivity:

| Parts / area | Remaining uncertainty | Current working choice |
|---|---|---|
| U6, C2NM | VIN/VOUT board connections and operating voltage | S-812C33AMC? pin map implemented; pin1 ground supported by resistance. |
| Q8, 3724A | Fitted maker and external source/drain connections | SIL3724A? implemented, drain join and ground return supported by resistance; C6 measured as supply-related; exact path unresolved. |
| D3 / A7 | Physical orientation and clamp routing | BAV99 series-dual candidate supported by user-confirmed A7. |
| D2 / 4P | Identity, pin functions and routing | FMMT2907R is a code/package lead only; numbered stock placeholder with all three pads open. |
| D4/D5/D6 | Diode type, polarity and connections | SD05 TVS / MMSZ5228BS Zener candidates assigned; D4/D5 lower pads photo-traced to ICSP clock/data; D4/D5 opposite pads now join photo-supported ground; the two D6 pads remain unresolved. |
| LED1 / S1 | LED emitter configuration/polarity; switch common pairs | Standard symbols present, physical mapping provisional. |
| Q1/Q2/Q7 and repeated 2H transistors | Candidate identity and orientation | Existing stock BJT symbols; identity strength varies and is documented above. |
| L1/L2, unmarked capacitors | Bead versus inductor, capacitance and package sizes | Standard passive symbols present. Proposed decoupling values are estimates; RF filter/tuning values remain unknown. C27 lacks a circuit role; C41 now shunts the TP4/RB4 net to photo-supported ground. |
| PIC and block interfaces | Exact GPIO destinations and hidden tracks | 9 PIC pads remain open after five user GPIO destinations in v0.8; remote roles remain partly inferred. See pic_gpio_user_mapping.json. |
| PIR daughterboard | Internal components and routes | Only the J3 interface is represented; daughterboard internals are outside the current main-board revision. |

The 46 open physical pins include 24 on unpopulated/DNP entries; the other 22 include named test pads and two internally open U6 pins. They are not 46 missing parts. U7/U6A/Q9 and other DNP entries do not require identifying a fitted chip. The machine-readable list is `evidence/completion_status.json`. Further photo/datasheet inference can continue without a broad measurement campaign. A completely confirmed schematic cannot be claimed from missing identity, value and buried-trace evidence.

## Package and value audit, v0.6

R29 and R44 both read 18C in the original photos (IMG_2434 and IMG_2438 respectively), yielding nominal 15 kohm using EIA-96. This resolves their value question marks without new measurements. 126 stock footprints were assigned using MCP, leaving C5/S1/LED1 for dimensions and pad mapping. FootprintConfidence and FootprintBasis properties retain the distinction between photo estimates and measured geometry. No net partitions were changed. The detailed per-part [completion audit](FINISHING_CHECKLIST.html) separates value, identity, package and routing gaps.

## Superseding v0.7 photo audit

The earlier generic PIC supply and battery-divider interpretation is partly contradicted by visible copper. This section takes precedence over those v0.6 descriptions. New direct GPIO routes: U4.2 to C25 right pad; U4.4 to C39 left pad; U4.24 to R4 lower pad; U4.26 to TP10 and R35 upper pad; U4.18 to TP17, with probable top-edge continuation to R13 upper pad. C32 visibly bridges U4.20 and U4.19, not the PIR rail. R35 is empty: its lower pad/Q9 lower-left are a separate local net.

D4 lower cathode candidate/R32 lower pad connect U4.27; D5 lower cathode candidate/R40 upper pad connect U4.28. Their old R32/PIR-supply and R40/VDD ties are withdrawn. C41 right pad connects TP4; its under-U4 continuation is unknown, so TP4 is removed from the antenna net. C26 no longer has the unsupported VDD tie. C25/C39 no longer have generic 100n bypass values. Ground assignments at their opposite pads and remote interface roles remain inferred.

C5 is 470uF/16V from the user. C11 dimensions support 1206; R8 complete-body dimensions including both metal end caps confirm the 0603 size match, revising the repeated fitted resistor package family provisionally. All 147 assigned footprint files remain standard-library candidates. C5 body/lead geometry, S1 and LED1 remain unassigned.

The v0.7 model has 87 net partitions, 54 open physical pads and 14 open PIC GPIOs. See evidence/pic_trace_audit.json and the annotated PDF. Existing photo resolution is enough for the direct local changes above; unresolved pad exits/top-edge continuations benefit from sharper, overlapping straight-on photos. Hidden copper still may need targeted continuity.

## Superseding v0.8 user continuity and via comparison

This section supersedes conflicting v0.7 guesses above. The user checked both visible copper and multimeter continuity. Recorded mappings are U4.3/RA1 to R28/R29/TP7; U4.17/RC6 to R13; U4.22/RB1 to TP2; U4.23/RB2 to TP1; U4.25/RB4 to TP4; U4.26/RB5 to TP10 corroborated. RP7 in the reply is interpreted as the photographed TP7. Exact ohms were not supplied; resistor free-end pin1 mappings use local photographs.

Removed hypotheses: RC7/TP17 onward to R13, TP2 to RF supply, TP1 to LED common, R28/R29 to the other bias nodes and TP7 to the speculative detector node. Retained local photo trace: RC7 to TP17, with remote continuation unknown. Existing receive feedback/coupling and LED polarity/common remain provisional.

D4.2/V030, D5.2/V027 and C41.2/V025 join the main rear copper without apparent clearance, identified using PIC VSS8/V041 and VSS19/V045 anchors. Added these three photo-supported grounds; C39.2/C26.2 ground estimates are corroborated. VDD20/V042 has rear clearance, as does RC1/V053. The latter remains electrically unidentified. See the [interactive via comparison](VIA_REVIEW.html).

The inventory is 127 visible rear sites with 10 individually matched anchors, not every physical via and not 127 resolved nets. Layer count, hidden power planes and occluded routing are not uniquely recoverable from surface photographs. The user's four-layer hypothesis is retained as plausible, not a confirmed stackup.

GPIOs 12,15,16,21 have reported vias with unknown onward nets. GPIOs 5,6,7,11,13 have no visible continuation; traces/vias under U4 remain possible. None is certified NC.
