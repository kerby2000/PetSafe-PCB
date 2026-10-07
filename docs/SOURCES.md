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
| U6 alternative | [Richtek RT9818](https://www.richtek.com/assets/product_file/RT9818/DS9818-12.pdf) | Voltage-supervisor family exists in a five-pin package. The WN association comes from historical Richtek marking material [mirrored here](https://www.rom.by/files/Richtek_Marking_Code.PDF); it is a lead, not an exact identification. |
| Native format | [KiCad schematic format](https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/) | Embedded library, symbol units, wires, junctions, instances and labels. Native validation uses the installed 10.0.5 CLI. |

## Photographs used for circuit decisions

| Photo | Main content |
|---|---|
| IMG_2430 | U1/PPEK, regulator capacitors and empty option network |
| IMG_2431, IMG_2432 | U2/C14R, Q8/372A, D1, RF drive resistors |
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
