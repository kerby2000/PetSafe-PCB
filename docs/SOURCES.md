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
| Q1 | [Formosa FMOS3401A Rev.C](https://www.formosams.com/upload/product/Mosfets/FMOS3401A_REV_C.pdf), saved as FMOS3401A_REV_C.pdf | Page 5 explicitly lists R1A, 3401 and R1 markings and shows SOT-23 PMOS pin functions. Fits Q1 photo/power path; exact fitted maker unproved. Earlier MMBT3904 NPN hypothesis withdrawn in v0.9.9. |
| Tuning Qs | [Taitron semiconductor catalog](https://www.taitroncomponents.com/docs/2007%20Semiconductor%20Catalog.pdf) | Manufacturer table lists MMBTA55 / 2H / PNP. Exact fitted manufacturer is unknown. |
| Tuning alternative | [Nexperia PBSS5140T](https://assets.nexperia.com/documents/data-sheet/PBSS5140T.pdf) | Alternative PNP candidate; short-code identification remains ambiguous. |
| D1 | [Nexperia BAV99](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf) | A7 marking, SOT23 dual-series diode and pin map. Current Diodes-branded BAV99 uses a different marking; do not use that to prove A7. |
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


## U6 / Q8 and diode marking sources


- [ABLIC S-812C](https://www.ablic.com/en/doc/datasheet/voltage_regulator/S812C_E.pdf), saved as S812C.pdf: printed p8 Table1 C2N = S-812C33AMC 3.3 V; p11 Table5 pins 1 VSS, 2 VIN, 3 VOUT, 4/5 NC for A variant.
- [ABLIC MP005-A package](https://www.ablic.com/en/doc/package/MP005-A.pdf), saved as ABLIC_MP005-A.pdf: PDF p5 three product-code characters, fourth assembly month, dot positions assembly year/week. Supports C2NM interpretation; M's exact month not decoded.
- [MCC SIL3724A manufacturer PDF, Chipdip mirror](https://static.chipdip.ru/lib/761/DOC050761871.pdf), saved as SIL3724A.pdf: p1 explicit 3724A marking, N/P pair, pin diagram and SOT23-6L dimensions. Same primary document was read via Mouser; direct Mouser download returned HTML, which was replaced with this valid PDF.
- [Nexperia BAV99](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf), saved as BAV99.pdf: A7 marking and dual-series topology support D3 (user-confirmed A7) and D1. D2's later diode measurements support this topology R -> S -> L, but its 4P marking does not establish BAV99 identity. Pins 1=A1, 2=K2, 3=K1/A2 must not be confused with current placeholder/photo numbering.
- **Withdrawn D4-D6 candidate:** [Diotec 1N4148WS](https://diotec.com/tl_files/diotec/files/pdf/datasheets/1n4148ws.pdf), saved as 1N4148WS.pdf: T4/W2 mark and SOD-323F switching diode. Earlier photos were misread as T4; newer 5U/G3 readings supersede that guess. The PDF is retained as source history.
- New user photographs are copied unchanged to photos/user_updates/ and checksummed separately in evidence/user_evidence_2026-10-08.json. Measurements and the 0.5-ohm shorted-probe clarification are recorded in evidence/measurement_plan.json. The original 26-image manifest is unchanged.

## Diode marking sources

- [Semtech SD05/SD12, manufacturer PDF mirrored by TME](https://www.tme.eu/Document/7ef0e55cabc749c01c5f7eae977e91a5/SD05.pdf), saved as SD05.pdf: page 6 5U marking; pages 1-2 unidirectional SOD-323 TVS with 5 V standoff. D4/D5 candidate.
- [Diodes MMSZ5228BS](https://www.diodes.com/datasheet/download/MMSZ5228BS.pdf), saved as MMSZ5228BS.pdf: page 2 G3 = 3.9 V SOD-323 Zener. D6 provisional first candidate.
- [Nexperia PZUxB](https://assets.nexperia.com/documents/data-sheet/PZUXB_SER.pdf), saved as PZUXB_SER.pdf: page 2 G3 = PZU2.4B 2.4 V SOD323F. D6 alternative; the marking is not unique.
- New D4/D5/D6 user images are preserved in photos/user_updates. Q8 D-E=2 ohm and S-G=2 ohm support joined drains/ground source. E-F=400 kohm refutes direct C6/output copper; F-P=10 ohm and F-G=300 kohm support a supply-related C6 node, with exact path unresolved.



## Current evidence boundaries

The [independent review of 6ae4eaa](reviews/2026-10-09_independent_review_6ae4eaa.md) was received on 2026-10-09 and is preserved unchanged. It is a logical review, not new bench data. The [v0.9.30 response](reviews/2026-10-09_review_response_v0.9.30.md) records the original-photo RF correction, remaining uncertainties, user choice to retain U6A's regulator symbol and correction of the review's swapped U106 pin1/pin3 example. Photo hashes and before/after net membership are in `evidence/architect_review_v0930.json`.

See [recorded measurements](MEASUREMENTS.md), [circuit interpretation](RECONSTRUCTION.md) and [library alternatives](LIBRARIES_AND_ALTERNATIVES.md). Q1 uses the R1A/FMOS3401A candidate above; exact fitted maker and gate operation remain unverified. D2/4P now has a probable series-diode topology from user measurements, but no exact part identification. The [Zetex FMMT2907R](https://media.digikey.com/pdf/Data%20Sheets/Zetex%20PDFs/FMMT2907(A).pdf) marking-only PNP lead is downgraded because its simple junction pattern does not match the observed directed series path. External in-circuit paths remain a caveat. The original dated citations, historical candidates, package audits and event-by-event reports are preserved in [the archived source register](history/pre_cleanup_20261008/docs/SOURCES.md). All saved datasheets have hashes in `evidence/datasheet_manifest.json`. Datasheets establish candidate properties, not board connectivity.
