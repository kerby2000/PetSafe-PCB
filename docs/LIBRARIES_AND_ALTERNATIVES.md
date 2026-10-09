# Current KiCad libraries and package qualifications

Current schematic v0.9.31 uses KiCad 10.0.5, the connected KiCad MCP server, **149 catalog entries / 154 physical-device symbol units / 351 physical pads**, and **22 stock plus four authorized datasheet device definitions**. Five stock PWR_FLAG annotations declare existing source paths without adding physical parts. The project and KiCad 10 global tables register PetSafe_Datasheet; all embedded symbol graphics/pins match their registered sources. 148 footprints are assigned candidates; only LED1 remains blank. [Current component audit](../evidence/completion_audit.csv) and [pin crosswalk](../evidence/pin_crosswalk.json) supersede older catalog totals and arbitrary connector numbering.

Stock graphics and pin numbers are retained. U1/U5 and subsequently U6/Q8 were explicitly authorized for MCP datasheet-symbol construction. The symbol library is portable through `${KIPRJMOD}`. Candidate pinout correctness is distinct from fitted identity and actual board wiring. [The prior library narrative](history/cleanup_v0928/docs/LIBRARIES_AND_ALTERNATIVES.md) preserves intermediate authoring details and older package guesses.

## Library choices

| References | Library symbol | Reason / status |
|---|---|---|
| U4 | `MCU_Microchip_PIC16:PIC16F18855-xSO` | Exact SOIC family symbol; default SOIC-28W footprint. |
| U2 A/B/C | `74xGxx:74LVC2G14` | Standard multi-unit Schmitt inverter, value `SN74LVC2G14DBV?`, SOT-23-6 footprint. This preserves separate readable gates and supply unit. The exact monolithic `SN74LVC2G14DBV` also exists. |
| U3 A/B/C | `Amplifier_Operational:Opamp_Dual` | Standard generic dual op-amp with matching 1-8 pin functions; value remains SGM8542XS. No modified or custom op-amp symbol. |
| Q1 | `Transistor_FET:Q_PMOS_GSD` | v0.9.9: FMOS3401A candidate, matching manufacturer R1A marking and SOT-23 G1/S2/D3 pinout. Photo R=gate, L=source, single S=drain. Original NPN hypothesis withdrawn. Exact fitted maker unconfirmed. |
| Q2, Q7 | `Transistor_BJT:BC847`, `Transistor_BJT:BC857` | Standard family symbols; values preserve the B/C gain-bin candidates. |
| Q3/Q4/Q5/Q6/Q11 | `Transistor_BJT:Q_PNP_BEC` | Standard generic PNP with B=1, E=2, C=3; value MMBTA55? preserves the uncertain 2H identification. |
| D1/D3 | `Diode:BAV99` | A7 marking candidates; D3 marking now confirmed by the user. D3 rail terminals are user-confirmed (L GND, R VDD); exact R42 end is photo-selected. D1 still has an isolated branch. Exact fitted maker remains unproved. |
| D2 | `Connector_Generic:Conn_01x03` | Unidentified 4P part; in-circuit readings support series junctions R -> S -> L. L=1/R=2/S=3 remain bookkeeping. User maps R-C20 lower, L-ANT2/R46 upper, S-R46 lower; R46 is empty. Exact part/ratings unknown; prior rail-clamp ties remain withdrawn. |
| LED1 | `Device:LED_Dual_AAKK` | User-confirmed red/green dual emitter, 1.5 x 1.5 mm body; colour-to-pin mapping and footprint remain provisional. |
| S1 | `Switch:SW_Push` | Four physical switch pads map to two repeated footprint pad numbers; see measured-body evidence below. |
| R/C/L/Y/TP | `Device:R`, `Device:C`, `Device:C_Polarized`, `Device:L`, `Device:Crystal`, `Connector:TestPoint` | Existing conventional library parts. C5 is modeled positive on H_RF_VDD and negative on GND, retaining user/photo polarity evidence. |
| U1 | `PetSafe_Datasheet:S-1200B45-M5T1` | MCP-created from ABLIC Rev.6 page 5: 1 VIN, 2 VSS, 3 ON/OFF, 4 NC, 5 VOUT. B option has active-high enable. The fitted part remains a strong identification candidate, not a measured fact. |
| U5 | `PetSafe_Datasheet:MX512H` | MCP-created from Mixic Rev.1.2 page 2: 1 VCC, 2 INA, 3 INB, 4 VDD, 5 OUTB, 6/7 GND, 8 OUTA. Logic/motor supplies and both ground pins retained. |
| U6 | `PetSafe_Datasheet:S-812C33AMC` | MCP-created from ABLIC Table 5; C2N product code and measured likely ground support identification. |
| Q8 | `PetSafe_Datasheet:SIL3724A` | MCP-imported standard generic N/P graphics with manufacturer-verified 1 G_N, 2 S_P, 3 G_P, 4 D_P, 5 S_N, 6 D_N. Fitted maker unconfirmed. |
| D4/D5 | `Device:D_Zener` | Standard unidirectional avalanche symbol, value SD05? / TVS 5V. Semtech maps 5U to SD05. SOD-323 candidate footprint; ICSP and ground routes are photo-derived. |
| D6 | `Device:D_Zener` | G3 supports MMSZ5228BS? / 3.9V, but PZU2.4B / 2.4V remains an alternative. Standard SOD-323 candidate footprint; D6 routing and polarity are measured (A GND, K VPP); breakdown is unverified. |
| J connectors / empty pads | `Connector_Generic` family | Unknown pitches and empty package identities stay unspecified. These entries preserve the source catalog. |

The installed BAV99 symbol has hidden pin-name strings that do not agree with the Nexperia terminology for pins 1/2. Its visible diode geometry and **pin numbers** agree with the datasheet (1 A1, 2 K2, 3 K1/A2). No library modification or pin swapping was made to hide this naming issue.

## Western alternatives

These are engineering candidates, not identifications of the fitted chips. The reconstruction has not been converted into a replacement board.

| Fitted / candidate part | Alternative | Stock KiCad symbol / footprint | Compatibility |
|---|---|---|---|
| SGM8542XS, SOIC-8 | **Microchip MCP6002-I/SN** | `Amplifier_Operational:MCP6002-xSN`; `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | Same eight pin functions and nominal narrow SOIC-8 package. Plausible pin-compatible option, but electrical equivalence is not established. |
| MX512H, SOP-8 | **TI DRV8212PDSGR** | `Driver_Motor:DRV8212P`; `Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm_ThermalVias` | Preferred redesign candidate. Separate logic/motor supplies, two logic inputs, up to 4 A peak. Different package, pinout, exposed ground pad, and sleep control: **requires PCB and control review**. |
| MX512H, lower-current option | TI DRV8837DSGR | `Driver_Motor:DRV8837`; standard WSON-8 footprint | Similar interface, but its 1.8 A headline drive rating is below MX512H's advertised 3 A peak. Do not choose it without establishing motor current margin. |

MCP6002 offers 1.8-6.0 V operation and 1 MHz bandwidth. Against SGM8542's 2.1-5.5 V, 1.1 MHz and 46 uA/amplifier, its typical 100 uA/amplifier increases the receiver's two-channel quiescent load by about **108 uA**. Its 4.5 mV maximum offset versus 3.5 mV also matters in the high-gain chain. The same resistor gain does not guarantee the same receiver threshold or filtering response. Sources: [Microchip DS20001733L](https://ww1.microchip.com/downloads/aemDocuments/documents/MSLD/ProductDocuments/DataSheets/MCP6001-1R-1U-2-4-1-MHz-Low-Power-Op-Amp-DS20001733L.pdf), [SGMICRO datasheet](https://www.sg-micro.com/rect/assets/537cce2c-8022-4ea6-97f4-6524851a35e8/SGM8541_SGM8542_SGM8544.pdf).

DRV8212P covers the inferred battery range with its motor supply and has a 1.65-5.5 V logic supply. Its 4 A figure is a peak rating subject to thermal limits, not a promise of 4 A continuous output on a tiny footprint. MX512H advertises 1.4 A continuous and 3 A peak at 6.5 V; the larger peak margin makes DRV8212P a more useful redesign candidate than DRV8837. Sleep/wake timing, coast/brake behavior, stall current and supply transients remain design checks. Sources: [TI DRV8212P Rev. A](https://www.ti.com/lit/ds/symlink/drv8212p.pdf), [MX512H Rev.1.2](https://static.chipdip.ru/lib/203/DOC045203539.pdf), [TI DRV8837 Rev. F](https://www.ti.com/lit/ds/symlink/drv8837.pdf).

### Motor-driver function cross-reference (redesign only)

| Function | MX512H pin | DRV8212P pin |
|---|---|---|
| Logic supply | 1 VCC | 8 VCC |
| Motor supply | 4 VDD | 1 VM |
| Control A / B | 2 INA / 3 INB | 6 IN1 / 5 IN2 |
| Motor A / B | 8 OUTA / 5 OUTB | 2 OUT1 / 3 OUT2 |
| Ground | 6 and 7 | 4 plus exposed pad (KiCad 9) |
| Sleep | No separate pin | 7 nSLEEP; must be defined, not left floating |

This table matches functions, not physical pad locations. Motor polarity and truth-table behavior still require review before implementing a redesign. DMC3071LVT is a Western Q8 comparison with the same pin functions but a different TSOT package and electrical ratings; it is not an approved replacement. U6 is now an ABLIC Japanese regulator candidate. ABLIC S-1200B45 is a Japanese regulator, not a Chinese device needing a geographical substitution.

## Footprints and completed datasheet symbols

Standard SOT-23, SOT-23-5, SOT-23-6 and SOIC footprints are assigned only for identified/candidate packages. Assignment is a package-family hypothesis, not a measurement of the photographed land pattern. Current assignments use fitted resistor family 0603, anchored by the user R8 full-body measurement; large tuning capacitors use 1206, supported by C11 dimensions. Other bodies remain photo-based estimates. Earlier 0805 family estimates are superseded. Connector pitches and test-pad drills are lower-confidence approximations. Only LED1 remains unassigned. C5 now uses a stock 6.3 mm radial candidate with inferred 2.5 mm pitch; measured can height is 16 mm. S1 now uses `Switch:SW_Push` with `Button_Switch_SMD:SW_SPST_PTS645Sx43SMTR92`: physical TL/TR map to repeated pad1 and BL/BR to repeated pad2, preserving the previous inferred common pairs. The user measured a 6 x 6 x 4 mm body plus 2 mm actuator, about 6 mm overall. The approximately 8 mm photo-estimated pad span supports this candidate 2D land pattern; it does not establish the manufacturer. The stock x43 3D housing is 4.3 mm high, so it is not an exact enclosure model. See `evidence/s1_dimensions_20261009.json` and the [C&K PTS645 family drawing](https://www.ckswitches.com/media/1471/pts645.pdf). J1 numbering is now photograph-reconciled: square pad1=VPP,2=VDD,3=GND,4=DAT,5=CLK. Existing electrical signal destinations are unchanged; pitch/lead geometry remains photo-based. See evidence/footprint_evidence.json for every assignment and its basis. U6 SOT-23-5 and Q8 SOT-23-6 are datasheet-based package candidates, not measured land patterns.

The original two exact-symbol requests are now resolved through authorized MCP creation. U1 uses stock `Package_TO_SOT_SMD:SOT-23-5`. U5 uses stock `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`, matching the nominal package dimensions on MX512H page 9. Pad numbers were checked through MCP. Land-pattern fit on the photographed PCB remains unmeasured. SGM8542 does not need a custom drawing: the stock generic dual op-amp already represents its actual pinout. U6 and Q8 now have datasheet candidate symbols with normal artwork and pin numbering. The old custom library and generator are archived in `reference/v02/`; they are not registered in the active project.

## Current empty-option symbols

Q9 uses stock `Transistor_BJT:Q_NPN_BEC`: L/base1 through R35, R/emitter2 to GND, S/collector3 to J6.1. NPN is an inferred role for an empty footprint.

U6A is native **U106**, using `Regulator_Linear:MCP1700x-330xxTT` only as a regulator role template: **pin3 input, pin2 output, pin1 ground**. The earlier connector numbering is superseded. It is DNP and shares its output with U6, retaining the ERC output conflict; this does not validate simultaneous population or identify an absent original part. No new ERC suppression was added.

C49 remains stock `Device:C`, DNP between ANT2 and GND; both connections are resolved. TP9 is absent from the active inventory after the unsupported original entry was withdrawn.

## Current measured geometry and values

- C5: 470 uF / 16 V, 6.33 mm diameter x 16 mm high. Stock `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` is assigned; 2.5 mm pitch and 0.8 mm drill remain inferred. Its 7 mm housing model is not the measured 16 mm can.
- S1: 6 x 6 x 4 mm body plus 2 mm actuator. Stock SW_Push has two native nodes; physical TL/TR map to pin1, BL/BR to pin2. The four physical pads remain recorded. Stock PTS645 gullwing footprint is a candidate; its x43 height differs from measured about 6 mm. Contact behavior and exact fit remain unverified.
- LED1: red/green, square 1.5 x 1.5 mm. Body dimensions do not establish pad pattern or die numbering; do not substitute an addressable LED footprint just because its body size matches. No vendor symbol/footprint has been supplied.
- R8: 1.6 x 0.77 mm including caps supports 0603; other resistors are provisional family matches. C11 3.2 x 1.5 mm supports 1206.
- L1/L2: 1.4/2.2 uH reported LCR readings, stock `Device:L` and existing 0805 candidates retained. Measurement conditions, magnetic construction, DCR and ratings remain unknown.

See the [measurement summary](MEASUREMENTS.md) and structured dimension records. No repeat body measurements or completed diode/continuity sweeps are requested.
