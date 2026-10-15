# Physical-evidence closure audit

Generated for **v0.9.45** by `verify_evidence_contracts.py`. Source: [selected independent evidence](../evidence/physical_evidence_review_20261015.json); [machine-readable comparison](../evidence/topology_closure_audit.json).

**0 supported joins split; 0 measured separations merged; 0 photographed pads missing mappings in the reviewed regions.**

227 sourced join observations and 32 separation observations were checked. 19 modeled nets still contain separate evidence groups in this corpus. This is an evidence-coverage result, not a count of proven wrong wires. Existing native checks separately establish file consistency.

## Decisions and specific remaining joins

| Area | Assessment / missing evidence | Action |
|---|---|---|
| E11 / receiver input | D2.R and C20.2 form one supported group. Common membership with C19.1, R28.2 and U3.3 remains inherited; C20.1-to-GND is separately unverified. Neither the 1-ohm D2 result nor expected op-amp function establishes these joins. | One future check, if owner continues: C20 lower metal end to U3 pin3, resistance, battery/programmer disconnected. Near probe resistance supports the hidden input link; kOhm/OL rejects a direct join. It does not settle the other three branches. |
| E11 / U1 supply and enable | U1.L1/VIN and U1.L3/CE share H_LDO_IN in the model. IMG_2430 does not expose the complete path for each left contact, so a common supply assumption remains qualified. | Retain known drawing and explicit exception; do not choose a pin role to manufacture a copper edge. No additional owner request now. |
| E04 / tuning return registration | Each front midpoint is independently visible; exact connection to its corresponding rear capacitor remains a front/rear registration inference. Shared rear ground band is visible. | Keep existing mapping qualified; no all-pairs campaign. A same-index front/rear continuity would settle an individual bridge if later necessary. |
| E11 / other graph gaps | The generated table names all groups without a complete evidence path, including ordinary rail fan-out and PIC/local joins not encoded by this selected pass. They are not automatically hardware defects. | Review existing local/photo/via records before requesting any further test. No claim of complete copper verification. |

The issue register owns owner actions and closure criteria: [OPEN_ITEMS.md](OPEN_ITEMS.md#e11). One staged input-link check is located on the [original-photo probe guide](measurement-images/receiver_input_bridge.svg). Generic graph gaps below are not an all-to-all bench queue.

## Original-photo review

| Region | Source | Finding |
|---|---|---|
| R39/Q2/PIR | [IMG_2425.jpg](../photos/originals/IMG_2425.jpg); [IMG_2435.jpg](../photos/originals/IMG_2435.jpg) | R39 correction independently supported. R38/base and R39/output remain distinct. Q2 function is still a candidate. |
| Receiver/D2/D3 | [IMG_2429.jpg](../photos/originals/IMG_2429.jpg); [IMG_2434.jpg](../photos/originals/IMG_2434.jpg) | Feedback and DNP R47/C42 local copper corroborated. D2.R-C20.2 measured; C20.1 ground and the C19/R28/U3.3 grouping remain inherited, not proved by that one measurement. |
| RF supply/driver | [IMG_2428.jpg](../photos/originals/IMG_2428.jpg); [IMG_2431.jpg](../photos/originals/IMG_2431.jpg) | Separate input branches, output gate resistors, R5 feed and Q8 outer-drain band corroborated. R5 is a boundary; 24/27ohm are not copper. Device ratings do not justify rewiring. |
| Tuning front/rear | [IMG_2433.jpg](../photos/originals/IMG_2433.jpg); [IMG_2442.jpg](../photos/originals/IMG_2442.jpg) | Five front cells and shared ANT2 band visible; rear ground band and separate midpoint islands visible. Exact front-to-rear midpoint correspondence remains dependent on approximate registration. |
| Power and motor | [IMG_2430.jpg](../photos/originals/IMG_2430.jpg); [IMG_2438.jpg](../photos/originals/IMG_2438.jpg) | Local output/filter/option pads reviewed. No additional unambiguous correction found. U1 enable-to-input branch and some rail/pad associations still lack independently encoded direct support. |

## Device interpretation, separate from copper

### E04: Q3/Q4/Q5/Q6/Q11

The stock PNP model remains disputed. With the modeled emitter at ground and a nonnegative PIC base drive through the resistor, ordinary forward-active PNP switching would require a negative base-emitter voltage; the present DC interpretation does not supply it. RF excursions could matter, so this is not proof of another family. Q3 red L to S=0.48V, L to R=2.3V, reverse/other tests OL do not isolate the presumed base junctions at R. An NPN base-at-R candidate is not established either; a MOSFET body-diode interpretation also does not identify gate/source/drain. Preserve copper and the visibly qualified PNP label; no symbol swap.

Sources: [q3_diode_results_20261009.json](../evidence/q3_diode_results_20261009.json), [mmbta55lt1-d.pdf](https://www.onsemi.com/download/data-sheet/pdf/mmbta55lt1-d.pdf).

### E03: U2 rating and Q8 drive

TI lists C14R for the SN74LVC2G14 DBV candidate (packaging addendum); its recommended VCC is 1.65–5.5V, absolute maximum 6.5V. B76 reports 6.3V, and B77 directly measures +1.8V relative to printed VDD. Thus the candidate is 0.8V above recommended maximum; R5=22ohm filters/limits current and does not regulate the rail. Keep the measured feed. Resting Q8 VGS(P)=0 and VGS(N)=+6.3V are consistent with P off/N on under the candidate, but establish no dynamic timing or non-overlap. The old 4.5V-driver complaint is not current.

Sources: [u2_supply_voltage_result_20261014.json](../evidence/u2_supply_voltage_result_20261014.json), [u2_vdd_separation_result_20261014.json](../evidence/u2_vdd_separation_result_20261014.json), [q8_gate_bias_results_20261014.json](../evidence/q8_gate_bias_results_20261014.json), [sn74lvc2g14.pdf](https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf).

### I01: D2 external map versus equivalent junctions

External R(upper-left/native2) reaches C20.2; L(upper-right/native1) reaches ANT2/R46.1; S(single/native3) reaches R46.2. R46 is empty. Directed tests are consistent with a two-series-junction equivalent R --|>|-- S --|>|-- L: 0.6 V each and 1.2 V end-to-end, reverse OL. This is an in-circuit equivalent, not a recovered part identity; the connector placeholder and physical numbering stay. Neither outer D2 pad is a confirmed supply/ground clamp endpoint.

Sources: [d2_diode_20261009.json](../evidence/d2_diode_20261009.json).

### E07: Q2 and corrected R39

R38 feeds Q2.R; R39 now pulls Q2.S/TP16/PIC21 to VDD. For a conditional NPN model with VBE 0.7V, a 3.3V PIR signal through 10 kohm gives about 0.26mA base current, and a 4.5V/10kohm collector pull-up requires at most about 0.45mA. This is a plausible inverter topology, not identification or operating proof. U6A stays DNP, output-conflict symbol retained, and is excluded from any functional interpretation as a fitted regulator.

Sources: [r39_endpoint_correction_v0945.json](../evidence/r39_endpoint_correction_v0945.json), [pic21_tp16_followup_20261009.json](../evidence/pic21_tp16_followup_20261009.json).

### E08: Q7 and receiver

B65/B66 directly support Q7.L-R19.1 and Q7.R-R19.2. Diode results favor a PNP-like base at L, but do not isolate E/C or maker. Later direct QR-QL=0V is consistent with no forward base-emitter bias at rest; TP5=0.066V and VREF=0V were recorded in the red-blinking state. Earlier R19-to-ground readings must not be subtracted as one simultaneous state. Equal 10 kohm R21/R22 imply half-rail VREF only with negligible loading. Visible feedback around both op-amps is supported; detector/input and enabled behavior remain separate questions.

Sources: [q7_r19_join_results_20261014.json](../evidence/q7_r19_join_results_20261014.json), [q7_diode_results_20261014.json](../evidence/q7_diode_results_20261014.json), [q7_direct_bias_result_20261014.json](../evidence/q7_direct_bias_result_20261014.json), [receiver_supply_results_20261014.json](../evidence/receiver_supply_results_20261014.json).

### E09: Q1

Battery positive reaches Q1 single/native3; Q1.L/native2 reaches VSYS and U5.4. R44 reaches Q1.R/native1. The chosen PMOS G/S/D roles remain a candidate; two 6.3V nodes alone do not prove a direct join across Q1. R44=15kohm and rechecked TP14-to-Q1.R 21.4/21.7kohm no longer support the earlier 516 ohm bypass concern. Exact control path behavior remains open; no new wire is inferred.

Sources: [q1_gate_recheck_results_20261015.json](../evidence/q1_gate_recheck_results_20261015.json), [r44_resistance_result_20261015.json](../evidence/r44_resistance_result_20261015.json), [tp14_followup_results_20261014.json](../evidence/tp14_followup_results_20261014.json).

### E10: D6 and programming

Routing and measured polarity are established: anode GND, cathode VPP; forward approximately 0.7V, reverse OL. These do not determine reverse breakdown or compatibility with high-voltage programming. Preserve the qualified symbol and do not apply a breakdown test through the PIC or infer a voltage solely from G3.

Sources: [d6_u6_open_pad_results_20261009.json](../evidence/d6_u6_open_pad_results_20261009.json).

### Accepted E06 boundary; reproduction

PIC14-to-TP11 and PIC18-to-TP17 are valid supported local endpoints. Photos cannot exclude buried branches or establish firmware purpose. No routed PCB, recovered firmware, fully qualified footprints or proven stackup is provided. Battery, motor, antenna and PIR daughterboard remain external assembly context, not added main-board BOM parts.

Sources: [e06_disposition_v0941.json](../evidence/e06_disposition_v0941.json).

## Evidence boundaries

- TP11/TP17: local PIC routes supported; additional hidden branches and firmware purpose remain unexcluded.
- The roughly 5-ohm antenna is an external winding, not PCB copper. The 500-uH report has unspecified frequency and isolation conditions.
- Fitted low-ohm readings retain contact/configuration qualifications. R5 feed pairs are photo-supported with 3.3/4-ohm corroboration, not treated as ideal meter shorts.
- DNP options are not internally bridged. S1 permanent row contacts are supported by B38/B39; its pressed-state closure is not a copper edge.
- Scope work and component isolation remain deferred. Capacitor candidates and values were not revised by this audit.
- Inventory coverage is limited to the explicitly reviewed photo regions; numbering gaps do not establish missing parts.

## Unsupported joins in the encoded corpus

Each brace is a group connected by independent evidence. Separate braces on one modeled net need supporting evidence to justify their common membership. The JSON gives representative bridges; they are evidence-search targets, not automatically tests. No connection is removed solely because an edge has not been encoded.

| Modeled net | Independently supported groups |
|---|---|
| GND | {BATN.1}; {C1.2, C17.2, C19.2, C1A.2, C25.2, C26.2, C28.2, C33.2, C34.2, C35.2, C36.2, C37.2, C40.2, C49.2, C5.2, C6.2, C7.2, C8.2, C9.2, D3.L, GND.1, J3.3, LED1.BL, LED1.BR, Q2.L, Q8.B2, R22.1, R29.2, S1.TL, S1.TR, U1.L2, U2.T2, U6.R3, U6A.R2, U7.1}; {C12.1, C15.1, C38.1, C45.1, C48.1}; {C2.2, C2A.2}; {C20.1}; {C24.2}; {C27.2}; {C30.2}; {C31.1}; {C32.2}; {C39.2}; {C4.1, R2.1}; {C41.2}; {C42.1, U3.4}; {D4.2}; {D5.2}; {D6.2, J1.GND}; {GND_RF.1}; {Q11.L}; {Q3.L}; {Q4.L}; {Q5.L}; {Q6.L}; {Q9.R}; {R10.2}; {R32.1}; {R43.1}; {U4.19}; {U4.8}; {U5.6}; {U5.7} |
| H_BAT_SENSE | {C28.1}; {R3.2}; {R4.1} |
| H_LDO_IN | {C1.1, C1A.1, U1.L1}; {L2.2}; {U1.L3} |
| H_LED_CTL_A | {R30.1}; {TP1.1, U4.23} |
| H_LED_CTL_B | {R31.1}; {TP2.1, U4.22} |
| H_RX_ENABLE | {Q7.L, R19.1}; {R18.2} |
| H_RX_VDD | {C17.1}; {C24.1, U3.8}; {R20.2}; {R21.1}; {TP5.1} |
| OSC1 | {C30.1}; {U4.9}; {Y1.1} |
| OSC2 | {C31.2}; {U4.10}; {Y1.2} |
| PIC_RB3_RETURN | {R4.2}; {U4.24} |
| PIC_TP4_C41 | {C40.1, C41.1, R23.2, R42.1, TP4.1, U4.25}; {R44.1} |
| RX_A_PLUS | {C19.1}; {C20.2, D2.R}; {R28.2}; {U3.3} |
| TUNE_1_MID | {C10.2, C11.2}; {C12.2} |
| TUNE_2_MID | {C13.2, C14.2}; {C15.2} |
| TUNE_3_MID | {C16.2, C29.2}; {C38.2} |
| TUNE_4_MID | {C43.2, C44.2}; {C45.2} |
| TUNE_5_MID | {C46.2, C47.2}; {C48.2} |
| VDD | {C2.1, C2A.1, C3.1, C32.1, D3.R, Q7.R, R1.1, R19.2, R37.1, R39.2, U1.R1, U4.20, VDD.1}; {C34.1, U5.1}; {J1.VDD} |
| VSYS | {C27.1}; {C33.1, L1.1, L2.1, Q1.L, U5.4}; {R3.1} |

## Supersessions respected

- R39.1-to-Q2.R inherited inference replaced only by R39.1-to-TP16/Q2.S in v0.9.45.
- PIC21/V026-to-VREF withdrawn by owner; TP16-VREF 800 kohm and PIC21-TP16 remain current.
- Front C11/C14/C29/C44/C47 outer band is ANT2, not ground. N-B 414 kohm was explicitly corrected to B-G; actual N-B 1.4 ohm applies.
- TP14 is U5.8/OUTA, not BATTERY+. B61 516ohm to presumed Q1 gate is retained historically but latest B84/B85 are 21.4/21.7kohm.
- U2 supply is RF rail through R5, not printed 4.5 V VDD. The old 4.5V-driver argument for Q8 is obsolete; measured resting P VGS=0V.
- Q7 earlier 0/4.5 V R19 readings are not simultaneous; later direct QR-QL=0V is current state evidence, not a copper short.
- U6A physical labels retained; obsolete annotation native numbers are not imported. Current U106 pins 3/2/1=input/output/ground.
- C49 present on rear; TP9/R33 unsupported inventory withdrawn; rejected via artifacts do not become physical endpoints.
- S1 inferred common rows replaced by measured B38/B39; pressed B41 remains a switch state, not permanent copper.
