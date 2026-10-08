# U6 and Q8: corrected markings, v0.5

The sharper user photographs read **C2NM on U6** and **3724A on Q8**. The earlier WN23 and 372A readings were incorrect. This report supersedes the candidate ranking in the historical U6/Q8 investigation.

## U6: ABLIC S-812C33AMC-C2NT2x, strong candidate

The [ABLIC S-812C datasheet](https://www.ablic.com/en/doc/datasheet/voltage_regulator/S812C_E.pdf), Table 1 on printed page 8, maps product code **C2N** to the **3.3 V S-812C33AMC** in SOT-23-5. The [MP005-A package marking drawing](https://www.ablic.com/en/doc/package/MP005-A.pdf), PDF page 5, specifies three product-code characters followed by an assembly-month character. Thus M is an assembly code; its month has not been decoded here. This is a manufacturer-code match, reinforced by package and ground evidence, rather than a typical-application guess alone.

Table 5 on printed page 11 supplies the pin functions. In the original IMG_2435 photo and measurement guide:

| Probe / original pad | Package pin | Function | User resistance to G |
|---|---|---|---|
| C / R3 | 1 | VSS, ground | 2.7 ohm |
| B / R2 | 2 | VIN | 34 kohm |
| A / R1 | 3 | VOUT | 4.2 kohm |
| L1 | 4 | Internally open NC | Not measured |
| L2 | 5 | Internally open NC, A variant | Not measured |

The user clarified that shorted probe tips now read **0.5 ohm**; the earlier 2-5 ohm baseline varied with contact pressure. C is likely ground. The 2.7 ohm result is not precise proof of a direct copper connection, because it was not measured with an identical stable contact baseline. The very different A/B readings support distinguishing them from ground; resistance does not establish voltage or exact semiconductor identity.

**The RT9818A-33PB supervisor hypothesis is withdrawn.** Its WN code was found in real Richtek marking documentation, but the photographed device does not read WN. Its conventional pin3 ground also conflicts with these readings. The earlier generic LDO drawing used the wrong pin assignment too; v0.5 corrects the assignment from ABLIC Table 5.

The schematic now proposes R37 -> VIN, C36 input bypass, VOUT -> C37/PIR rail and pin1 -> ground. **3.3 V is the candidate rating, not a measured rail voltage.** NC pins remain unwired because no external ties have been established. ABLIC permits tying these internally open pads to VIN/VSS, so the symbol represents them as passive pins named NC.

## Q8: 3724A complementary N/P MOSFET pair

The [MCC SIL3724A manufacturer datasheet, mirrored by Chipdip](https://static.chipdip.ru/lib/761/DOC050761871.pdf), page 1, explicitly shows **3724A**, the six-lead SOT23-6L package, and one N-channel plus one P-channel MOSFET. This substantially strengthens the earlier circuit-role inference from the two 220-ohm drive resistors. The exact fitted manufacturer remains unconfirmed: a matching short marking is not a unique manufacturer logo identification.

| Original photo pad | Pin | Function |
|---|---|---|
| T3 | 1 | N-channel gate |
| T2 | 2 | P-channel source |
| T1 | 3 | P-channel gate |
| B1 | 4 | P-channel drain |
| B2 | 5 | N-channel source |
| B3 | 6 | N-channel drain |

The symbol uses normal KiCad generic N/P MOSFET artwork, imported through MCP and matched to this datasheet pin map. Both units belong to Q8 on the same sheet. The visible value is **SIL3724A?**, preserving uncertainty about the exact fitted part. The footprint is standard KiCad SOT-23-6; physical land-pattern fit remains unmeasured.

The user measured **D-E = 2 ohm**, **S-G = 2 ohm**, and **E-F = 400 kohm**. The low readings support joined drains and the N-source ground return, allowing for probe contact resistance. The 400-kohm result refutes a direct C6 upper-pad/output connection. That proposed wire has been removed; C6.1 is unresolved. The P-source supply and R5 output continuation remain inferred. The follow-up readings are **F-P=10 ohm** and **F-G=300 kohm**. They support a supply-related role for F, but 10 ohm is higher than the roughly 2-ohm direct-connection readings. Contact or series resistance could explain this; the exact path remains unresolved and no 10-ohm resistor is invented. [The annotated guide](../output/pdf/PetSafe_measurement_round1.pdf) records all results. This in-circuit 400-kohm result is not the value of a discrete resistor.

The Diodes **DMC3071LVT** remains a Western comparison with the same pin functions, but different ratings and a TSOT-23-6 package. Its C71 marking does not identify the fitted Q8 and it is not an approved drop-in replacement. U6 is an ABLIC Japanese part; no geographical substitute is needed to draw the fitted candidate accurately.

## D2-D6 candidates

- **D3: BAV99?** The user clearly reads **A7**. [Nexperia BAV99](https://assets.nexperia.com/documents/data-sheet/BAV99.pdf), page 2, supports A7 and the series-dual pin map. Board orientation and clamp routing remain inferred.
- **D2: 4P, unidentified.** The user clearly reads **4P**. The earlier BAV99 assignment and all three guessed clamp connections are withdrawn. The [Zetex manufacturer FMMT2907 datasheet](https://media.digikey.com/pdf/Data%20Sheets/Zetex%20PDFs/FMMT2907%28A%29.pdf), page 1, lists **FMMT2907R = 4P**, a SOT-23 PNP transistor. That is a credible marking/package lead, not proof of the fitted identity or its pin functions. A stock three-pin numbered placeholder retains the photographed pads until the internal junction arrangement and copper routes are established. No transistor pin map is forced onto it.
- **D4/D5: SD05?**, a 5 V unidirectional TVS. The sharper user photos read **5U**, contradicting the earlier T4/1N4148WS guess. [Semtech's manufacturer datasheet](https://www.tme.eu/Document/7ef0e55cabc749c01c5f7eae977e91a5/SD05.pdf), page 6, explicitly maps SD05 to 5U; page 1 specifies SOD-323. Five volts is the working/standoff rating, not its surge clamp voltage. Fitted manufacturer remains unconfirmed. A stock avalanche/Zener symbol is appropriate for this unidirectional TVS; a bidirectional TVS symbol would be wrong.
- **D6: MMSZ5228BS? / 3.9 V Zener**, a provisional first candidate. [Diodes' table](https://www.diodes.com/datasheet/download/MMSZ5228BS.pdf), page 2, maps **G3** to this SOD-323 part. However, [Nexperia PZU2.4B](https://assets.nexperia.com/documents/data-sheet/PZUXB_SER.pdf), page 2, also uses G3 for a **2.4 V** SOD323F Zener. The code does not uniquely establish the voltage or maker. No breakdown voltage was measured.

The cathode bands are visible in the new diode photos. Their mapped board endpoints and external connections remain unresolved; all six D4-D6 pads stay open. These candidates replace the earlier 1N4148WS guess. D2 and D3 are the three-lead parts beside C20 near U3, shown in [the location image](../output/D2_D3_location_v1.png).

The fitted identities, package dimensions and circuit connections have different confidence levels. A symbol pin table can be verified while a board wire remains inferred. See evidence/measurement_plan.json for raw readings and evidence/v05_net_changes.json for the specific revisions to net assignments.

## R41

The user clearly reads **331**: the three-digit resistor code is 33 x 10^1 = **330 ohm**. This is a recovered nominal value, not a multimeter reading; tolerance and power rating are not encoded here. The schematic, inventory and MCP placement template now use 330.
