# Source register

Manufacturer pinouts and application examples establish plausible functions, not photographed board connectivity. Accessed 2026-10-07 and 2026-10-08. Key PDFs are saved under `datasheets/`; SHA-256 checksums are in `evidence/datasheet_manifest.json`.

| Ref | Primary source | What it supports |
|---|---|---|
| U1 | [ABLIC S-1200 Rev.6.0](https://www.ablic.com/en/doc/datasheet/voltage_regulator/S1200_E.pdf), saved as S1200.pdf | Page 5 SOT-23-5 pins; page 23 marking PPE = S-1200B45-M5T1x with fourth-character lot code; typical regulator application. |
| U2 | [TI SN74LVC2G14](https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf), saved as SN74LVC2G14.pdf | Page 3 DBV six-pin top view; ordering addendum lists C14R; dual Schmitt inverter function. |
| U3 | [SGMICRO SGM8541/8542/8544](https://www.sg-micro.com/rect/assets/537cce2c-8022-4ea6-97f4-6524851a35e8/SGM8541_SGM8542_SGM8544.pdf), saved as SGM8542.pdf | Dual op-amp pinout, 2.1-5.5 V supply, approximately 1.1 MHz gain-bandwidth. |
| U4 | [Microchip PIC16(L)F18855/75 DS40001802H](https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/PIC16%28L%29F18855-75-Data-Sheet-40001802H.pdf) | 28-pin package, power, oscillator and ICSP pins; configurable peripherals. |
| U5 | [Mixic MX512H Rev.1.2, manufacturer PDF mirrored by Chipdip](https://static.chipdip.ru/lib/203/DOC045203539.pdf), saved as MX512H.pdf | Eight-pin H-bridge map; separate logic/motor supplies; application circuit and at least 4.7 uF logic decoupling. Mirror filename/title is less useful than the MX512H content. |
| Q2 | [Nexperia BC847x datasheet](https://assets.nexperia.com/documents/data-sheet/BC847X_SER.pdf) | BC847B marking 1F plus manufacturing code; NPN B/E/C pinout. |
| Q7 | [Nexperia BC857C product information](https://www.nexperia.com/products/bipolar-transistors/general-purpose-and-low-vcesat-bipolar-transistors/single-bipolar-transistors/single-bipolar-transistors-100-v/BC857C.html) | BC857C PNP with 3G marking plus manufacturing code. |
| Q1 | [Diodes MMBT3904](https://www.diodes.com/datasheet/download/MMBT3904.pdf) | Candidate NPN function and pinout only. Current marking information does not prove the photographed complete R1A code. |
| Tuning Qs | [Taitron semiconductor catalog](https://www.taitroncomponents.com/docs/2007%20Semiconductor%20Catalog.pdf) | Manufacturer table lists MMBTA55 / 2H / PNP. Exact fitted manufacturer is unknown. |
| Tuning alternative | [Nexperia PBSS5140T](https://assets.nexperia.com/documents/data-sheet/PBSS5140T.pdf) | Alternative PNP candidate; short-code identification remains ambiguous. |
| D1 | [Nexperia BAV99](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf) | A7 marking, SOT23 dual-series diode and pin map. Current Diodes-branded BAV99 uses a different marking; do not use that to prove A7. |
| U6 withdrawn WN hypothesis | [Richtek RT9818](https://www.richtek.com/assets/product_file/RT9818/DS9818-12.pdf) | Voltage-supervisor family exists in a five-pin package. The WN association comes from historical Richtek marking material [mirrored here](https://www.rom.by/files/Richtek_Marking_Code.PDF); it is a lead, not an exact identification. |
| Native format | [KiCad schematic format](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/) | Embedded library, symbol units, wires, junctions, instances and labels. Native validation uses the installed 10.0.5 CLI. |

## Photographs used for circuit decisions

| Photo | Main content |
|---|---|
| IMG_2430 | U1/PPEK, regulator capacitors and empty option network |
| IMG_2431, IMG_2432 | U2/C14R, Q8/3724A (sharper follow-up), D1, RF drive resistors |
| IMG_2433, IMG_2442 | Repeated tuning cells and corresponding rear capacitor/via arrangement |
| IMG_2429, IMG_2434 | U3, feedback resistors, receiver components |
| IMG_2435 | U6, Q2 and daughterboard interface |
| IMG_2436, IMG_2437 | PIC, oscillator, programming area and battery-divider resistors |
| IMG_2438 | Motor driver, Q1 and pushbutton |
| IMG_2421 and overview photos | Separate PIR daughterboard context; its internal circuit is not reconstructed |

Full provenance remains in the original component model and photo manifest. Existing image registration is an approximate alignment, not a dimensioned board or a verified layer-stack reconstruction. No exact schematic of this board was adopted from an unrelated product.

## KiCad 10 rebuild and Western alternatives (2026-10-08)

- [KiCad MCP Server](https://github.com/mixelpixx/KiCAD-MCP-Server): already installed and connected. Used for standard-library searches, blank schematic creation, all 150 component placements, extra units, footprint inspection and PDF/SVG export.
- [Microchip MCP6001/2/4 DS20001733L](https://ww1.microchip.com/downloads/aemDocuments/documents/MSLD/ProductDocuments/DataSheets/MCP6001-1R-1U-2-4-1-MHz-Low-Power-Op-Amp-DS20001733L.pdf): page 1 pinout, pages 3-4 operating range, current, offset and bandwidth; SOIC package drawings. Saved as MCP6002.pdf.
- [TI DRV8212P Rev. A](https://www.ti.com/lit/ds/symlink/drv8212p.pdf): page 4 pin functions and exposed pad, page 5 recommended operating conditions, typical application and package drawing. Saved as DRV8212P.pdf. Preferred motor-driver redesign candidate because MX512H advertises a 3 A peak.
- [TI DRV8837 Rev. F](https://www.ti.com/lit/ds/symlink/drv8837.pdf): alternative lower-current driver; its separate supplies, sleep input and WSON package differ from MX512H. Saved as DRV8837.pdf.

Library existence and footprint names were verified against the user's installed KiCad 10 libraries through MCP, not inferred from online search results. See LIBRARIES_AND_ALTERNATIVES.md for compatibility boundaries.

## Historical U6 / Q8 investigation (superseded marking interpretation)

- [Richtek RT9818 DS9818-12](https://www.richtek.com/assets/product_file/RT9818/DS9818-12.pdf), saved as `RT9818.pdf`: page 3 top-view package numbering and reset/supply/NC functions.
- [Richtek marking information, mirrored by Jotrin](https://www.jotrin.it/userfiles/downloadfile/202003111510585708.pdf), saved as `Richtek_Marking_2008.pdf`: actual document MI-080418, printed C-39 / PDF page 39 maps RT9818A-33PB to WN-. This is the inspected local marking source for the follow-up.
- [ROHM BD45/BD46 Rev.007, mirrored by RS](https://docs.rs-online.com/7ad0/0900766b8161bcad.pdf), saved as `BD45_BD46.pdf`: page 1 five-pin map and page 3 WN = BD46281, 2.8 V, 100 ms CMOS detector. Secondary U6 candidate.
- [Diodes DMC3071LVT](https://www.diodes.com/datasheet/download/DMC3071LVT.pdf) and [DMC2053UVT](https://www.diodes.com/datasheet/download/DMC2053UVT.pdf), saved under those names: page 1 complementary-pair pin maps, TSOT26 packages and C71 / AR2 markings. Topology comparisons only.
- [SYNC Power SPP3437](https://www.syncpower.com/datasheet/SPP3437.pdf), saved as `SPP3437.pdf`: pages 1-2 show 37 marking but a single P-channel device with multiple drain pins, not the leading two-gate hypothesis.

The [investigation report](U6_Q8_INVESTIGATION.html) separates manufacturer facts from new photo interpretations and the earlier native v0.3 circuit. Those hypotheses were retained in v0.4; v0.5 supersedes them with the new photographs and sources below. The derivative crops are reproducible from crop bounds/rotations in `evidence/u6_q8_investigation.json`; source photographs remain untouched.

## Authorized datasheet symbols, v0.4 (2026-10-08)

- ABLIC S1200.pdf page 5 / Table 3 provides the five-pin SOT-23-5 map. The internally open pin 4 may be tied to VIN/VSS. The B option uses active-high ON/OFF; the 45 option is nominally 4.5 V.
- Mixic MX512H.pdf page 2 provides the eight-pin functions; the truth table supports tri-state outputs in standby. Page 9 gives SOP-8 nominal 3.9 x 4.9 mm body, 6.0 mm overall span and 1.27 mm pitch, matching the selected stock narrow SOIC footprint.
- Actual MCP authoring requests, user authorization and footprint choices are preserved in `evidence/datasheet_symbol_authoring.json`. The MCP library writer retains a legacy generator-version metadata string; creation, native export and checks used installed KiCad 10.0.5.

## Corrected markings and diode candidates, v0.5

- [ABLIC S-812C](https://www.ablic.com/en/doc/datasheet/voltage_regulator/S812C_E.pdf), saved as S812C.pdf: printed p8 Table1 C2N = S-812C33AMC 3.3 V; p11 Table5 pins 1 VSS, 2 VIN, 3 VOUT, 4/5 NC for A variant.
- [ABLIC MP005-A package](https://www.ablic.com/en/doc/package/MP005-A.pdf), saved as ABLIC_MP005-A.pdf: PDF p5 three product-code characters, fourth assembly month, dot positions assembly year/week. Supports C2NM interpretation; M's exact month not decoded.
- [MCC SIL3724A manufacturer PDF, Chipdip mirror](https://static.chipdip.ru/lib/761/DOC050761871.pdf), saved as SIL3724A.pdf: p1 explicit 3724A marking, N/P pair, pin diagram and SOT23-6L dimensions. Same primary document was read via Mouser; direct Mouser download returned HTML, which was replaced with this valid PDF.
- [Nexperia BAV99](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf), saved as BAV99.pdf: A7 marking and dual-series topology support D3 (user-confirmed A7) and D1. D2 was withdrawn after user-confirmed 4P.
- **Withdrawn D4-D6 candidate:** [Diotec 1N4148WS](https://diotec.com/tl_files/diotec/files/pdf/datasheets/1n4148ws.pdf), saved as 1N4148WS.pdf: T4/W2 mark and SOD-323F switching diode. Earlier photos were misread as T4; newer 5U/G3 readings supersede that guess. The PDF is retained as source history.
- New user photographs are copied unchanged to photos/user_updates/ and checksummed separately in evidence/user_evidence_2026-10-08.json. Measurements and the 0.5-ohm shorted-probe clarification are recorded in evidence/measurement_plan.json. The original 26-image manifest is unchanged.

## Sharp 5U / G3 photographs and final measurements

- [Semtech SD05/SD12, manufacturer PDF mirrored by TME](https://www.tme.eu/Document/7ef0e55cabc749c01c5f7eae977e91a5/SD05.pdf), saved as SD05.pdf: page 6 5U marking; pages 1-2 unidirectional SOD-323 TVS with 5 V standoff. D4/D5 candidate.
- [Diodes MMSZ5228BS](https://www.diodes.com/datasheet/download/MMSZ5228BS.pdf), saved as MMSZ5228BS.pdf: page 2 G3 = 3.9 V SOD-323 Zener. D6 provisional first candidate.
- [Nexperia PZUxB](https://assets.nexperia.com/documents/data-sheet/PZUXB_SER.pdf), saved as PZUXB_SER.pdf: page 2 G3 = PZU2.4B 2.4 V SOD323F. D6 alternative; the marking is not unique.
- New D4/D5/D6 user images are preserved in photos/user_updates. Q8 D-E=2 ohm and S-G=2 ohm support joined drains/ground source. E-F=400 kohm refutes direct C6/output copper; F-P=10 ohm and F-G=300 kohm support a supply-related C6 node, with exact path unresolved.

## Latest direct readings: D2, D3 and R41

User reports D2=4P, D3=A7 and R41=331 (nominal 330 ohm). These supersede the older ambiguous photo readings. D3 is supported by Nexperia BAV99 page 2. D2 remains unidentified: [Zetex FMMT2907(A), Issue 3, February 1996](https://media.digikey.com/pdf/Data%20Sheets/Zetex%20PDFs/FMMT2907%28A%29.pdf), page 1, lists FMMT2907R=4P in SOT-23; this is a candidate lead only, without a selected pin map. Local copy: `docs/datasheets/FMMT2907.pdf`. D2 uses an open numbered stock placeholder.

## v0.6 resistor and package audit

[Bourns CRP0603 marking table](https://www.bourns.com/pdfs/CRP0603.pdf), page 3: EIA-96 18=150 and C=100, therefore 18C=15 kohm. Used only for code decoding, not to identify the fitted manufacturer, package or tolerance. Existing photos IMG_2434.jpg (R29) and IMG_2438.jpg (R44) supply the markings. Package-size candidates use relative body/land proportions against neighboring known IC pitches and the installed KiCad 10 stock footprint descriptions. No calibrated dimensional measurements were supplied.

## v0.7 PIC photo tracing

Microchip DS40001802H, page 4 supplies the SOIC pin numbering and port names. Board connections come from IMG_2436/2437/2438 and the overlapping IMG_2435/2434/2433 top-edge photos, not from a typical application. Five GPIO local routes were added. The RC7/TP17-to-R13 continuation is explicitly probable; vias/body-covered routes remain open. User reports C5 470uF/16V, C11 3.2x1.5mm, R8 1.6x0.77mm. These reports supersede conflicting photo estimates.

## v0.8 continuity and front/rear via evidence

User 2026-10-08 replies confirm both multimeter and visible traces for the GPIO destinations in `evidence/pic_gpio_user_mapping.json`; no numerical resistances supplied in this round. RP7 is interpreted as TP7 from IMG_2434. R13 free-end geometry uses IMG_2433; R28/R29/TP7 use IMG_2434; TP1/TP2 resistor tracks use IMG_2432. This supersedes the previous RC7-to-R13 speculation.

Registered original mosaics `photos/front_registered.jpg` and `photos/back_mirrored_registered.jpg`, original rear IMG_2439-2443, existing cross-side registration records, and Microchip's SOIC VSS8/VSS19/VDD20 pin identities support the via comparison. Rear is already mirrored; do not mirror twice. Front projection errors up to approximately 46 pixels on the full mosaic require local verification. Detailed manually chosen coordinates and limitations are in `evidence/via_audit.json`.

[Altium plane-rule documentation](https://www.altium.com/documentation/altium-designer/pcb/design-rule-types/plane) explains clearance/antipad versus plane connection as general PCB terminology. It does not identify this board's hidden nets or layer count.


## v0.9 user via review and cross-checks

User assignments and ambiguities are preserved in `evidence/via_user_review.json`; the supplied MX512H application image is preserved unchanged at `photos/user/via_review/MX512H_pin4_supply.png`. No manufacturer source is inferred from the screenshot beyond its displayed application diagram. Site-to-component cross-checks use the original front/rear photographic mosaics and IMG_2431 through IMG_2443; see `via_audit.json` and `v09_net_changes.json`. Rear appearance, user assignment, model hypothesis and held conflicts remain separate. No new per-via ohms or operating voltages were supplied.

## v0.9.1 incremental user corrections

The user supplied 21 site corrections on 2026-10-08, preserved verbatim apart from capitalization/spacing normalization in `via_user_review.json` follow-up corrections. Component-only reports retain earlier ground/supply claims with separate provenance. Pad selections use the existing photos; notably R44.1 at V017 is photo-selected, while R42.1 is explicitly user-supplied. No new per-site resistance, datasheet, part identity or value was supplied. See `v091_net_changes.json` and `VIA_REVIEW_RESULTS.md`.

## v0.9.2 incremental review and clarifications

Nineteen user site entries and the two follow-up answers are preserved in `via_user_review.json`. The user explicitly confirms V077 C19-R29 is GND. The V114 answer repeats the opposite-side second-pin location without confirming or withdrawing the older GND claim. The Q8 photo pad convention and existing datasheet mapping identify centre B2=pin5 and T2=pin2. No new IC identity or pin-number reassignment is inferred. C19/R29, Q7 and tuning-resistor pad selections use IMG_2434/2433; the Q8/C7/C8/C9 area uses IMG_2431 and the registered mosaic. No new per-site ohms supplied.


### 2026-10-08: v0.9.3 user via confirmations

User directly identifies PIC pins 5/6/7/11/13 at V036/V037/V039/V047/V049; V072 at TP6 (not R22.2); V079/V080 at SGM8542 pin5. No new per-site numerical resistance supplied. These supersede candidate associations, not all inferred remote connections. Exact report retained in evidence/via_user_review.json.
