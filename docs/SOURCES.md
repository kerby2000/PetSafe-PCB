# Component/document sources

Datasheet pin functions are separate evidence from the photographed PCB connections.

* U3: SGMICRO SGM8541/SGM8542/SGM8544 manufacturer datasheet, product page https://www.sg-micro.com/product/SGM8542 . The marking and SOIC-8 pin diagram were inspected. Exact top mark in IMG_2429 is SGM8542XS.
* U4: Microchip PIC16(L)F18855/75 data sheet DS40001802H. https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ProductDocuments/DataSheets/PIC16%28L%29F18855-75-Data-Sheet-40001802H.pdf . The 28-pin diagram was inspected. The fitted part is the F, not LF, variant.
* U5: Mixic MX512H manufacturer datasheet, Rev. 1.2, previously identified in this project's analysis. A distributor's document link is available at https://jlcpcb.com/partdetail/Mixic-MX512H/C5119047 . The direct document download was not retrievable during this packaging pass. Pin mapping is retained from the earlier document identification; check its top-view diagram before hardware changes.
* Native KiCad format: https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/ . Native format generation does not constitute an editor-load/ERC test.

No schematic of the exact 100-1339 R03 A board has been adopted. Older PetPorte/PIC16F886 firmware projects use different hardware and must not supply inferred nets or firmware for this board.

Searches for U1's PPEK and other short device marks did not establish sufficiently reliable, package-matching identities. Those fields remain unresolved.
