# KiCad 10 libraries and device alternatives

Revision 0.3 uses the existing KiCad MCP Server and the installed KiCad 10.0.5 at `%LOCALAPPDATA%/Programs/KiCad/10.0`. Both its Python backend (`pcbnew.GetBuildVersion()`) and native CLI reported 10.0.5. The MCP created the blank native schematic and placed all 150 components plus four additional units from standard libraries. The checked-in routing adapter reconnects those stock symbols and adds the block frames and annotations. Native KiCad checks the resulting connectivity. MCP PDF/SVG export was also exercised successfully.

No active symbol library was drawn from scratch. Stock symbol artwork and pin numbering remain unchanged. `tools/templates/mcp_standard_placements.kicad_sch` is the MCP placement output; `evidence/library_placements.json` is the replay manifest. `evidence/pin_crosswalk.json` maps all 352 photographed pads to their library pin numbers. Pin mapping can be provisional even when the underlying part symbol is exact.

## Library choices

| References | Standard symbol | Reason / status |
|---|---|---|
| U4 | `MCU_Microchip_PIC16:PIC16F18855-xSO` | Exact SOIC family symbol; default SOIC-28W footprint. |
| U2 A/B/C | `74xGxx:74LVC2G14` | Standard multi-unit Schmitt inverter, value `SN74LVC2G14DBV?`, SOT-23-6 footprint. This preserves separate readable gates and supply unit. The exact monolithic `SN74LVC2G14DBV` also exists. |
| U3 A/B/C | `Amplifier_Operational:Opamp_Dual` | Standard generic dual op-amp with matching 1-8 pin functions; value remains SGM8542XS. No modified or custom op-amp symbol. |
| Q1 | `Transistor_BJT:MMBT3904` | Candidate identity; physical orientation still inferred. |
| Q2, Q7 | `Transistor_BJT:BC847`, `Transistor_BJT:BC857` | Standard family symbols; values preserve the B/C gain-bin candidates. |
| Q3/Q4/Q5/Q6/Q11 | `Transistor_BJT:Q_PNP_BEC` | Standard generic PNP with B=1, E=2, C=3; value MMBTA55? preserves the uncertain 2H identification. |
| D1/D2/D3 | `Diode:BAV99` | D1 identification candidate; D2/D3 retain `clamp?`, so their use of this series-diode topology is an assumption. |
| LED1, S1 | `Device:LED_Dual_AAKK`, `Switch:SW_Push_Dual` | Stock four-pin symbols; photographed pad mapping remains provisional. |
| R/C/L/Y/TP | `Device:R`, `Device:C`, `Device:C_Polarized`, `Device:L`, `Device:Crystal`, `Connector:TestPoint` | Existing conventional library parts. C5 polarity is inferred from the selected rail topology. |
| U1 | `Connector_Generic:Conn_01x05` | Temporary numbered placeholder for probable S-1200B45. Functions printed on the sheet: 1 VIN, 2 GND, 3 EN, 4 NC, 5 OUT. Exact vendor symbol requested. |
| U5 | `Connector_Generic:Conn_02x04_Counter_Clockwise` | Temporary numbered MX512H placeholder, actual data-sheet pin numbers retained. Exact vendor symbol requested. |
| U6, Q8 | Stock 1x5 and 2x3 numbered placeholders | Identity unknown. U6 numbers follow the selected LDO hypothesis. Q8 numbers are surrogate indices, **not verified package numbers**. Do not assign a replacement or physical footprint from these indices. |
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

This table matches functions, not physical pad locations. Motor polarity and truth-table behavior still require review before implementing a redesign. U6 and Q8 have no responsibly selected Western replacement yet because their functions are not established. ABLIC S-1200B45 is a Japanese regulator, not a Chinese device needing a geographical substitution.

## Footprints and outstanding library requests

Standard SOT-23, SOT-23-5, SOT-23-6 and SOIC footprints are assigned only for identified/candidate packages. Assignment is a package-family hypothesis, not a measurement of the photographed land pattern. Passive sizes, connector pitches, Q8, U6 and unusual LED/button pads remain unassigned where the photographs do not establish dimensions.

The remaining exact-symbol requests are **S-1200B45-M5T1x** and **MX512H (SOP-8)**. Vendor or SnapEDA files can replace their temporary stock placeholders after checking pin maps. SGM8542 does not need a custom drawing: the stock generic dual op-amp already represents its actual pinout. Q8 and U6 need identity clarification before sourcing exact symbols. The old custom library and generator are archived in `reference/v02/`; they are not registered in the active project.
