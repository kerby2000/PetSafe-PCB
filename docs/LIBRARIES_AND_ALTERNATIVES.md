# KiCad 10 libraries and device alternatives

Revision 0.9.9 uses the existing KiCad MCP Server and the installed KiCad 10.0.5 at `%LOCALAPPDATA%/Programs/KiCad/10.0`. Both its Python backend (`pcbnew.GetBuildVersion()`) and native CLI reported 10.0.5. The MCP created the blank native schematic and placed all 150 components plus five additional units from standard libraries. The checked-in routing adapter reconnects those stock symbols and adds the block frames and annotations. Native KiCad checks the resulting connectivity. MCP PDF/SVG export was also exercised successfully.

The user authorized U1/U5 after vendor files could not be found, and subsequently authorized U6/Q8 datasheet reconstruction. MCP `create_symbol`, `register_symbol_library` and `replace_schematic_component` created and installed U1/U5 from the manufacturer pin tables. The other 20 definitions retain unmodified KiCad stock artwork and numbering. `tools/templates/mcp_standard_placements.kicad_sch` is the MCP placement output; `evidence/library_placements.json` is the replay manifest. `evidence/pin_crosswalk.json` maps all 352 photographed pads to their library pin numbers. Pin mapping can be provisional even when the underlying part symbol is exact.

## Library choices

| References | Library symbol | Reason / status |
|---|---|---|
| U4 | `MCU_Microchip_PIC16:PIC16F18855-xSO` | Exact SOIC family symbol; default SOIC-28W footprint. |
| U2 A/B/C | `74xGxx:74LVC2G14` | Standard multi-unit Schmitt inverter, value `SN74LVC2G14DBV?`, SOT-23-6 footprint. This preserves separate readable gates and supply unit. The exact monolithic `SN74LVC2G14DBV` also exists. |
| U3 A/B/C | `Amplifier_Operational:Opamp_Dual` | Standard generic dual op-amp with matching 1-8 pin functions; value remains SGM8542XS. No modified or custom op-amp symbol. |
| Q1 | `Transistor_FET:Q_PMOS_GSD` | v0.9.9: FMOS3401A candidate, matching manufacturer R1A marking and SOT-23 G1/S2/D3 pinout. Photo R=gate, L=source, single S=drain. Original NPN hypothesis withdrawn. Exact fitted maker unconfirmed. |
| Q2, Q7 | `Transistor_BJT:BC847`, `Transistor_BJT:BC857` | Standard family symbols; values preserve the B/C gain-bin candidates. |
| Q3/Q4/Q5/Q6/Q11 | `Transistor_BJT:Q_PNP_BEC` | Standard generic PNP with B=1, E=2, C=3; value MMBTA55? preserves the uncertain 2H identification. |
| D1/D3 | `Diode:BAV99` | A7 marking candidates; D3 marking now confirmed by the user. Physical orientation and external clamp routes remain inferred. |
| D2 | `Connector_Generic:Conn_01x03` | Unidentified 4P part. Stock numbered placeholder with L=1/R=2/S=3 as bookkeeping only; no functional assignment. Prior BAV99 clamp ties withdrawn. |
| LED1, S1 | `Device:LED_Dual_AAKK`, `Switch:SW_Push_Dual` | Stock four-pin symbols; photographed pad mapping remains provisional. |
| R/C/L/Y/TP | `Device:R`, `Device:C`, `Device:C_Polarized`, `Device:L`, `Device:Crystal`, `Connector:TestPoint` | Existing conventional library parts. C5 polarity is inferred from the selected rail topology. |
| U1 | `PetSafe_Datasheet:S-1200B45-M5T1` | MCP-created from ABLIC Rev.6 page 5: 1 VIN, 2 VSS, 3 ON/OFF, 4 NC, 5 VOUT. B option has active-high enable. The fitted part remains a strong identification candidate, not a measured fact. |
| U5 | `PetSafe_Datasheet:MX512H` | MCP-created from Mixic Rev.1.2 page 2: 1 VCC, 2 INA, 3 INB, 4 VDD, 5 OUTB, 6/7 GND, 8 OUTA. Logic/motor supplies and both ground pins retained. |
| U6 | `PetSafe_Datasheet:S-812C33AMC` | MCP-created from ABLIC Table 5; C2N product code and measured likely ground support identification. |
| Q8 | `PetSafe_Datasheet:SIL3724A` | MCP-imported standard generic N/P graphics with manufacturer-verified 1 G_N, 2 S_P, 3 G_P, 4 D_P, 5 S_N, 6 D_N. Fitted maker unconfirmed. |
| D4/D5 | `Device:D_Zener` | Standard unidirectional avalanche symbol, value SD05? / TVS 5V. Semtech maps 5U to SD05. SOD-323 candidate footprint; ICSP and ground routes are photo-derived. |
| D6 | `Device:D_Zener` | G3 supports MMSZ5228BS? / 3.9V, but PZU2.4B / 2.4V remains an alternative. Standard SOD-323 candidate footprint; ICSP and ground routes are photo-derived. |
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

Standard SOT-23, SOT-23-5, SOT-23-6 and SOIC footprints are assigned only for identified/candidate packages. Assignment is a package-family hypothesis, not a measurement of the photographed land pattern. Current assignments use fitted resistor family 0603, anchored by the user R8 full-body measurement; large tuning capacitors use 1206, supported by C11 dimensions. Other bodies remain photo-based estimates. Earlier 0805 family estimates are superseded. Connector pitches and test-pad drills are lower-confidence approximations. Only C5, S1 and LED1 remain unassigned; selecting a stock switch also requires reconciling its common-pad numbering. J1 retains logical pin numbering, so its square-pad/VPP orientation must be reconciled before PCB recreation. See evidence/footprint_evidence.json for every assignment and its basis. U6 SOT-23-5 and Q8 SOT-23-6 are datasheet-based package candidates, not measured land patterns.

The original two exact-symbol requests are now resolved through authorized MCP creation. U1 uses stock `Package_TO_SOT_SMD:SOT-23-5`. U5 uses stock `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm`, matching the nominal package dimensions on MX512H page 9. Pad numbers were checked through MCP. Land-pattern fit on the photographed PCB remains unmeasured. SGM8542 does not need a custom drawing: the stock generic dual op-amp already represents its actual pinout. U6 and Q8 now have datasheet candidate symbols with normal artwork and pin numbering. The old custom library and generator are archived in `reference/v02/`; they are not registered in the active project.

## U6 / Q8 follow-up (2026-10-08)

See [corrected marking and pin maps](U6_Q8_MARKING_UPDATE.md). MCP library search found no exact S-812C or 3724 symbol. U6 was created from ABLIC's pin table; Q8 reuses KiCad's `Q_Dual_NMOS_PMOS_G1S2G2D2S1D1` artwork through MCP import. The six pins match SIL3724A. Actual 3724A fitted manufacturer remains unconfirmed. The earlier RT9818 intermediate symbol was removed after the new photo corrected the marking.

MCP's property writer damaged a nested KiCad 10 property expression during the first Q8 import attempt. The malformed intermediate was removed, the generic base symbol was reimported through MCP, and metadata was repaired with a parsed S-expression. Graphics and pins were not redrawn by hand. Native export and the library audit validate the final result. Authoring details are recorded in `evidence/datasheet_symbol_authoring.json`.

The U1/U5 pin contracts in `evidence/vendor_symbol_requirements.json` are fulfilled. `evidence/datasheet_symbol_authoring.json` records the actual MCP requests and sources. No vendor files were imported. The library URI uses `${KIPRJMOD}`, so the repository is portable. U1 pin 4 is passive and named NC because ABLIC explicitly permits this internally open pad to connect to VIN/VSS; it preserves the existing optional-pad copper. MX512H outputs use tri-state pin types to reflect high-impedance standby. These changes enable additional ERC checks without hiding unresolved nets.

## v0.7 package correction

The user reports R8 approximately 1.6 x 0.77 mm including both metal end caps, confirming the 0603 body-size match. This supersedes v0.6's 0805 fitted-resistor-family estimate; other resistors are revised as provisional 0603 family candidates. C11 approximately 3.2 x 1.5 mm supports its 1206 assignment. C5 value/voltage are now 470uF/16V; its package remains unset pending dimensions.
