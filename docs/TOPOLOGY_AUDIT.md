# Physical-evidence closure audit

Generated for **v0.9.48** by `verify_evidence_contracts.py`. Source: [selected independent evidence](../evidence/physical_evidence_review_20261015.json); [machine-readable comparison](../evidence/topology_closure_audit.json).

**0 supported joins split; 0 measured separations merged; 0 photographed pads missing mappings in the reviewed regions.**

269 sourced join observations and 36 separation observations were checked. 6 modeled nets still contain separate evidence groups in this corpus. This is an evidence-coverage result, not a count of proven wrong wires. Existing native checks separately establish file consistency.

## Decisions and specific remaining joins

| Area | Assessment / missing evidence | Action |
|---|---|---|
| E11 / receiver-input bridge - completed | C20 lower/model2 joins D2.R and R28 right/model2; R28 left remains TP7. C20-to-U3.3=1.023 Mohm and C20-to-TP7=998 kohm exclude direct copper; C20-to-R28 right=1.5 ohm supports the bounded split. | Resolved using already supplied results; no repeated C20-lower-to-U3 test. The full resistive path is not claimed. |
| E11 / U3.3 destination | Resolved by new owner report and annotated photo: U3 pin3 (third lower contact from the pin1 dot) joins printed VREF. The earlier C19.1/C20.2-to-U3.3 high-resistance readings remain exclusions, not copper links. | Join U3.3 to VREF. RX-3 stays deferred and unmeasured; no owner action. |
| E11 / C19.1 destination | Resolved by explicit owner clarification: C19 lower/model1 joins R28 right/model2 and C20 lower/model2, hence the established D2.R group. Upper/model2 joins R29 right/model2 on GND. This explains the matching 1.023-Mohm readings from C19/C20 lower to U3.3 without inventing a new resistor. | Join C19.1 to D2_C20; preserve RX-1 and the 100pF* estimate. |
| E11 / C20.1 destination | Resolved by owner annotation: C20 upper/model1 follows the drawn route to R42 lower/model2 and the existing D3.S junction. R42 is the cropped 122 resistor at the upper-right, distinct from R25 below C23. RX-2 = 271 kohm to GND remains valid. C19 and C20 share only their lower-terminal group, not both terminals. | Join C20.1 to H_D3_SIGNAL; preserve RX-2 and the 100pF* estimate. |
| E11 / U1 enable | L2 LEFT/model2-C1 UPPER/model1-U1 upper-left/native1 VIN now has visible support in IMG_2430/2435. Only U1 lower-left/native3 ON/OFF-to-VIN remains hidden under the package. | Undetermined from existing evidence. Preserve the qualified modeled join; owner action: none. |
| E11 / R18 and receiver supply | R18 upper/model2-to-Q7.L remains partly under the Q7 body in IMG_2434. B65 proves Q7.L-R19.1, not R18. R21 right/C17 lower/C24 upper/U3.8 form a visible group; R20.2 and TP5 remain separate evidence groups on H_RX_VDD. | Undetermined from existing evidence. Preserve the qualified modeled join; owner action: none. |
| E11 / battery-divider junction | R3 lower/model2, R4 upper/model1 and C28 lower/model1 still lack visible common copper in IMG_2436/2437. R4 lower-to-PIC24 and R3 upper-to-VSYS are separately supported. | Undetermined from existing evidence. Preserve the qualified modeled join; owner action: none. |
| E11 / VDD fan-out | C34.1-U5.1 is locally visible in IMG_2438; its join to printed VDD, and J1.VDD-to-printed VDD, still lack independently selected direct evidence. Do not use the motor pin4 rail or IC pin names as proof. | Undetermined from existing evidence. Preserve the qualified modeled join; owner action: none. |
| E04 / five rear midpoints - evidence reconciled | Existing owner reports for V107/103/100/095/090 identify C10/13/16/43/46 front midpoint pairs; original IMG_2442 independently identifies their C12/15/38/45/48 right lands. Each bridge is recorded individually. No shared midpoint or coil bridge is introduced. | Copper-evidence gap closed for these five joins. Tuning transistor identity, pin roles and switching behavior remain under E04/I01. No new bench work. |
| E11 / ground fan-out | Supported in this round: R10.2-to-GND through owner-ground V116 and its original-photo neck; R2.1/C4.1-to-U1.2 through continuous exposed copper in IMG_2430. Remaining separate candidate ground groups: BATN.1; C30.2/C31.1; C39.2; C42.1/U3.4; D4.2; D5.2; D6.2/J1.GND; GND_RF.1; Q3.L; R43.1; U5.6; U5.7. C20.1 is excluded from GND by RX-2, not another candidate ground bridge. | Twelve candidate ground groups retain missing evidence to the established ground group. Existing schematic membership is preserved. No pending readings. |
| E11 / ground BATN.1 | Undetermined from existing evidence. IMG_2438: Battery-negative solder terminal/wire is visible. Its onward copper is covered by the solder/terminal area; no continuous exposed route to the central GND anchor or an independently grounded via is established. The printed minus sign is not continuity evidence. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground C30.2/C31.1 | Undetermined from existing evidence. IMG_2436: The inward capacitor terminals share the already supported T-shaped neck below the crystal. The common land then becomes obscured at the crystal/package area; no independently identified ground-via bridge is visible. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground C39.2 | Undetermined from existing evidence. IMG_2436: The right/model2 capacitor land reaches a local via. Its earlier matched inventory ID is V038, not owner-ground V032. V038 has no independent owner GND report; rear-copper appearance and PIC-reference function do not complete the ground bridge. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground C42.1/U3.4 | Undetermined from existing evidence. IMG_2434 and IMG_2429: C42 upper/model1 and U3 bottom-right pin4 form the supported local group. The nearby local land/via does not have an independently established route to a known ground anchor in these images; amplifier supply pin naming is not a measured bridge. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground D4.2 | Undetermined from existing evidence. IMG_2437: The upper diode terminal reaches its local via, previously matched as V030. V030 was not in the owner ground list. Its ground classification came from rear-plane appearance; a specific continuous bridge to a measured ground anchor is not recovered. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground D5.2 | Undetermined from existing evidence. IMG_2437: The upper diode terminal reaches its local via, previously matched as V027. V027 was not in the owner ground list. Its ground classification came from rear-plane appearance; a specific continuous bridge to a measured ground anchor is not recovered. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground D6.2/J1.GND | Undetermined from existing evidence. IMG_2437: B24 establishes D6 upper/model2 to J1 middle/native3 at 1 ohm. The original guide identifies Z as J1.GND, not the separate printed GND test hole. Thus this proves the local group only; no new root-ground bridge follows from the label. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground GND_RF.1 | Undetermined from existing evidence. IMG_2432: The second pad printed GND is partly hidden by C5. The capacitor body covers the intervening area, so a complete exposed neck to the measured negative/ground group cannot be followed. The repeated GND label alone is insufficient. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground Q3.L | Undetermined from existing evidence. IMG_2433, IMG_2442 and IMG_2443: The fifth transistor upper-left pad visibly reaches a short dedicated via. The four other ordered ground sites V089/094/099/104 do not identify this fifth site. V109 lies near the antenna terminal below C11, not this Q3 pad; no owner-ground report can be assigned to the fifth via from the existing inventory. Approximate rear projection does not reveal a uniquely matched exposed connection. Do not extrapolate device symmetry or a PNP emitter role. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground R43.1 | Undetermined from existing evidence. IMG_2438: The upper/model1 resistor termination is visible, but its onward buried/via destination is not independently grounded. The lower/model2 is the established V015/TP14/U5.8 motor-output group; neither that result nor the nearby VSYS island identifies the upper-side return. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground U5.6 | Undetermined from existing evidence. IMG_2438: With the pin1 dot at upper-right, pin6 is the second lower contact from the left. Solder/package coverage prevents a continuous exposed route to C33/C34 return vias from being established; MX512H GND pin naming alone does not prove the PCB join. | Retain qualified GND membership; no new edge or owner action. |
| E11 / ground U5.7 | Undetermined from existing evidence. IMG_2438: With the pin1 dot at upper-right, pin7 is the third lower contact from the left. No independently traceable exposed bridge to pin6 or a confirmed ground via is recovered; do not merge evidence groups by adjacent GND pin roles. | Retain qualified GND membership; no new edge or owner action. |
| E06 / accepted reconstruction boundary | PIC14-TP11 and PIC18-TP17 are valid local routes. Photographs cannot exclude buried continuation or prove test-only purpose. | Explicitly accepted limitation; no TP16 rechecks, no new test or NC claim. |

The issue register owns owner actions and closure criteria: [OPEN_ITEMS.md](OPEN_ITEMS.md#e11). The [completed original-photo probe guide](measurement-images/receiver_input_bridge.svg) is retained for orientation; C20-to-U3.3, TP7 and R28 results are recorded and must not be repeated. Generic graph gaps below are not an all-to-all bench queue.

## Original-photo review

| Region | Source | Finding |
|---|---|---|
| R39/Q2/PIR | [IMG_2425.jpg](../photos/originals/IMG_2425.jpg); [IMG_2435.jpg](../photos/originals/IMG_2435.jpg) | R39 correction independently supported. R38/base and R39/output remain distinct. Q2 function is still a candidate. |
| Receiver/D2/D3 | [IMG_2429.jpg](../photos/originals/IMG_2429.jpg); [IMG_2434.jpg](../photos/originals/IMG_2434.jpg) | Original-photo-only assessment before the new owner annotation (see current decisions above): Feedback/DNP local copper remains corroborated. Owner E11 follow-up now separates D2.R/C20.2/R28.2 from U3.3. At that review C19.1-U3.3 and C20.1-GND remained unverified; subsequent RX-1/RX-2 reject both and supersede those inherited joins. |
| RF supply/driver | [IMG_2428.jpg](../photos/originals/IMG_2428.jpg); [IMG_2431.jpg](../photos/originals/IMG_2431.jpg) | Separate input branches, output gate resistors, R5 feed and Q8 outer-drain band corroborated. R5 is a boundary; 24/27ohm are not copper. Device ratings do not justify rewiring. |
| Tuning front/rear | [IMG_2433.jpg](../photos/originals/IMG_2433.jpg); [IMG_2442.jpg](../photos/originals/IMG_2442.jpg) | Five front pairs and ANT2 band visible. The earlier registration-only qualification is superseded for the five rear midpoint bridges by separately cited owner via-ID reports plus original rear-land identification below. Device identity and switched behavior remain open. |
| Power and motor | [IMG_2430.jpg](../photos/originals/IMG_2430.jpg); [IMG_2438.jpg](../photos/originals/IMG_2438.jpg) | Local output/filter/option pads reviewed. No additional unambiguous correction found. U1 enable-to-input branch and some rail/pad associations still lack independently encoded direct support. |
| U1 input neck | [IMG_2430.jpg](../photos/originals/IMG_2430.jpg); [IMG_2435.jpg](../photos/originals/IMG_2435.jpg) | L2 left/model2 to C1 upper/model1 closes the input-feed gap. U1 lower-left/native3 enable disappears beneath the package and is not closed. |
| LED and oscillator | [IMG_2432.jpg](../photos/originals/IMG_2432.jpg); [IMG_2436.jpg](../photos/originals/IMG_2436.jpg); [IMG_2425.jpg](../photos/originals/IMG_2425.jpg) | Two LED resistor-to-test-point tracks, both PIC/crystal/load-capacitor branches, and R4 lower-to-PIC24 are visible. No ground or battery-divider junction inferred from proximity. |
| Receiver fan-out and hidden routes | [IMG_2434.jpg](../photos/originals/IMG_2434.jpg); [IMG_2429.jpg](../photos/originals/IMG_2429.jpg) | Original-photo-only assessment before the new owner annotation (see current decisions above): C17 lower and R21 right join C24 upper/U3.8 visibly. R20.2/TP5 supply continuation remains hidden. R18 upper trace disappears under Q7; do not upgrade it to direct copper proof. C19 lower-to-U3.3 and C20 upper-to-GND remain unproved. |
| Five numbered rear midpoint lands | [IMG_2442.jpg](../photos/originals/IMG_2442.jpg); [IMG_2433.jpg](../photos/originals/IMG_2433.jpg) | Each rear via/land was individually identified in the original: V107=C12.2, V103=C15.2, V100=C38.2, V095=C45.2, V090=C48.2. The corresponding front destination is the explicit owner report for that ID, not the projected front marker. All five owner-supported bridges are encoded separately; seven OL inter-midpoint exclusions remain. Rear left common band reaches owner-ground V093. |
| Selected ground branches | [IMG_2438.jpg](../photos/originals/IMG_2438.jpg); [IMG_2436.jpg](../photos/originals/IMG_2436.jpg); [IMG_2437.jpg](../photos/originals/IMG_2437.jpg); [IMG_2433.jpg](../photos/originals/IMG_2433.jpg); [IMG_2442.jpg](../photos/originals/IMG_2442.jpg) | Existing ground reports now paired with original local pad-to-via necks: C27 right, PIC8/PIC19/C32 right, Q9 lower-right, R32 upper, C41 left, and Q11/Q6/Q5/Q4 left. Q3 and unlocated ground branches remain qualified; no assumed device-role edge. |
| Round2 receiver path and remaining local grounds | [IMG_2429.jpg](../photos/originals/IMG_2429.jpg); [IMG_2434.jpg](../photos/originals/IMG_2434.jpg); [IMG_2436.jpg](../photos/originals/IMG_2436.jpg); [IMG_2441.jpg](../photos/originals/IMG_2441.jpg); [D2_user_pad_labels_20261009.png](../photos/user_updates/D2_user_pad_labels_20261009.png) | Original-photo-only assessment before the new owner annotation (see current decisions above): U3 pin1 dot confirms lower pins 1/2/3/4 from left. Pin3 has no exposed trace identifying an external feed; its continuation is obscured under/along the package. C19 lower and C20 upper destinations cannot be followed continuously from the front; the rear original supplies no uniquely traceable alternate route. TP7/R28/R29 visible local routes and the completed C20 measurements do not resolve U3.3. C24 lower-to-R22 ground end is continuous; C30/C31 inner ends share a visible local neck, but its ground bridge remains unproved. No new electrical correction is justified. |
| R10 and U1 empty-option ground bridges | [IMG_2431.jpg](../photos/originals/IMG_2431.jpg); [IMG_2443.jpg](../photos/originals/IMG_2443.jpg); [IMG_2430.jpg](../photos/originals/IMG_2430.jpg) | Supported: R10.2 reaches the unique adjacent V116 ground via. R2.1/C4.1 share continuous exposed copper with U1 native2, distinct from native3 enable. Both close evidence gaps on existing GND membership; no topology, device role, value or population changes. |
| Receiver destinations / owner annotation and explicit clarification | [owner_receiver_connections_20261015.png](../evidence/owner_receiver_connections_20261015.png) | New evidence establishes U3.3-VREF, C20 upper-R42 lower/D3.S and C19 lower-C20 lower/R28 right/D2.R. Existing R29 right-C19 upper/GND and TP7-R28 left remain. Original numerical results are unchanged. |

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

B65/B66 directly support Q7.L-R19.1 and Q7.R-R19.2. Diode results favor a PNP-like base at L, but do not isolate E/C or maker. Later direct QR-QL=0V is consistent with no forward base-emitter bias at rest; TP5=0.066V and VREF=0V were recorded in the red-blinking state. Earlier R19-to-ground readings must not be subtracted as one simultaneous state. Equal 10 kohm R21/R22 imply half-rail VREF only with negligible loading. Visible feedback around both op-amps is supported; detector/input and enabled behavior remain separate questions. E11 follow-up rejects the former detector/R28-to-U3.3 copper join; C20 and C19 are no longer modeled in parallel. No new transfer-function claim is supported. The subsequent RX-1/RX-2 results reject C19.1-U3.3 and C20.1-GND; those inherited joins are now withdrawn. Its actual external signal/DC-return path is unresolved under E11; a capacitor does not establish a DC return. U3.5/VREF remains settled. This is a reconstruction gap, not evidence of a defective board.

Sources: [q7_r19_join_results_20261014.json](../evidence/q7_r19_join_results_20261014.json), [q7_diode_results_20261014.json](../evidence/q7_diode_results_20261014.json), [q7_direct_bias_result_20261014.json](../evidence/q7_direct_bias_result_20261014.json), [receiver_supply_results_20261014.json](../evidence/receiver_supply_results_20261014.json), [receiver_input_results_20261015.json](../evidence/receiver_input_results_20261015.json).

### E09: Q1

Battery positive reaches Q1 single/native3; Q1.L/native2 reaches VSYS and U5.4. R44 reaches Q1.R/native1. The chosen PMOS G/S/D roles remain a candidate; two 6.3V nodes alone do not prove a direct join across Q1. R44=15kohm and rechecked TP14-to-Q1.R 21.4/21.7kohm no longer support the earlier 516 ohm bypass concern. Exact control path behavior remains open; no new wire is inferred.

Sources: [q1_gate_recheck_results_20261015.json](../evidence/q1_gate_recheck_results_20261015.json), [r44_resistance_result_20261015.json](../evidence/r44_resistance_result_20261015.json), [tp14_followup_results_20261014.json](../evidence/tp14_followup_results_20261014.json).

### E10: D6 and programming

Routing and measured polarity are established: anode GND, cathode VPP; forward approximately 0.7V, reverse OL. These do not determine reverse breakdown or compatibility with high-voltage programming. Preserve the qualified symbol and do not apply a breakdown test through the PIC or infer a voltage solely from G3.

Sources: [d6_u6_open_pad_results_20261009.json](../evidence/d6_u6_open_pad_results_20261009.json).

### Accepted E06 boundary; reproduction

PIC14-to-TP11 and PIC18-to-TP17 are valid supported local endpoints. Photos cannot exclude buried branches or establish firmware purpose. No routed PCB, recovered firmware, fully qualified footprints or proven stackup is provided. Battery, motor, antenna and PIR daughterboard remain external assembly context, not added main-board BOM parts.

Sources: [e06_disposition_v0941.json](../evidence/e06_disposition_v0941.json).

### E11 / receiver reference and coupling: current copper versus function

The latest owner report establishes an external VREF connection to U3 pin3, in addition to the already established pin5/VREF connection. It does not imply an internal connection between the two amplifier inputs. C19 lower joins C20 lower/D2.R/R28 right; C19 upper is GND. C20 upper joins R42 lower/D3.S. Thus C19 shunts the D2_C20 node to ground, while C20 couples that node to the R42/D3 junction; they are not parallel capacitors. At DC, C21/C22/C23 open and DNP R47/C42 remain absent. R26 (120 kohm) supplies negative feedback to U3.2; the R48 (5.6 kohm)-R25 (1.2 kohm) branch terminates through C23. Under powered linear operation the first amplifier can follow VREF at DC; this conditional circuit interpretation does not establish the dynamic transfer or PIC function. The existing R28 (1 Mohm)/R29 (15 kohm) path remains a conditional resistive return if RA1 is high impedance. No new resistor or capacitor value is inferred. RX-3 remains deferred, not measured. Prior alternatives for an unknown U3.3 feed are superseded by the owner VREF report.

Sources: [SGM8541_SGM8542_SGM8544.pdf](https://www.sg-micro.com/rect/assets/537cce2c-8022-4ea6-97f4-6524851a35e8/SGM8541_SGM8542_SGM8544.pdf), [SGM8542.pdf](../docs/datasheets/SGM8542.pdf), [receiver_input_results_20261015.json](../evidence/receiver_input_results_20261015.json), [IMG_2429.jpg](../photos/originals/IMG_2429.jpg), [IMG_2434.jpg](../photos/originals/IMG_2434.jpg), [receiver_connections_v0948.json](../evidence/receiver_connections_v0948.json).

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
| GND | {BATN.1}; {C1.2, C12.1, C15.1, C17.2, C19.2, C1A.2, C2.2, C24.2, C25.2, C26.2, C27.2, C28.2, C2A.2, C32.2, C33.2, C34.2, C35.2, C36.2, C37.2, C38.1, C4.1, C40.2, C41.2, C45.1, C48.1, C49.2, C5.2, C6.2, C7.2, C8.2, C9.2, D3.L, GND.1, J3.3, LED1.BL, LED1.BR, Q11.L, Q2.L, Q4.L, Q5.L, Q6.L, Q8.B2, Q9.R, R10.2, R2.1, R22.1, R29.2, R32.1, S1.TL, S1.TR, U1.L2, U2.T2, U4.19, U4.8, U6.R3, U6A.R2, U7.1}; {C30.2, C31.1}; {C39.2}; {C42.1, U3.4}; {D4.2}; {D5.2}; {D6.2, J1.GND}; {GND_RF.1}; {Q3.L}; {R43.1}; {U5.6}; {U5.7} |
| H_BAT_SENSE | {C28.1}; {R3.2}; {R4.1} |
| H_LDO_IN | {C1.1, C1A.1, L2.2, U1.L1}; {U1.L3} |
| H_RX_ENABLE | {Q7.L, R19.1}; {R18.2} |
| H_RX_VDD | {C17.1, C24.1, R21.1, U3.8}; {R20.2}; {TP5.1} |
| VDD | {C2.1, C2A.1, C3.1, C32.1, D3.R, Q7.R, R1.1, R19.2, R37.1, R39.2, U1.R1, U4.20, VDD.1}; {C34.1, U5.1}; {J1.VDD} |

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
- v0.9.46: the initial 1 Mohm C20-U3.3 report is refined to 1.023 Mohm. The inherited D2.R/C20.2/R28.2-to-U3.3 copper join is withdrawn. C19/C20 parallel-200pF rationale is no longer applicable; individual starred estimates remain unchanged.
- Topology closure round1: the five rear-midpoint evidence gaps are resolved by individually reconciling the existing V090/095/100/103/107 owner reports with IMG_2442. This upgrades evidence coverage only, not values, device types, or modeled copper. The former approximate front-marker interpretation is not used as proof.
- Topology round2 leaves the v0.9.46 electrical partitions unchanged. C24.2 joins grounded R22.1 by visible local copper; C30.2/C31.1 form one local group, whose ground bridge is still unproved. E11 now explicitly includes the missing external signal/DC-bias feed into U3.3; confirming C19 alone cannot close it. RX-1/RX-2 are the only staged new checks.
- RX-1 C19 lower/model1 to U3.3 = 1.023 Mohm (raw 1.023mohm, interpreted as megaohms); RX-2 C20 upper/model1 to printed GND = 271 kohm; shorted probes = 1 ohm. Settling/drift not reported. Both inherited direct joins withdrawn in v0.9.47; replacement destinations remain unknown.
- v0.9.48: owner VREF report, annotated R42/C20 route and explicit C19/C20 lower common-node clarification supersede only the three unknown destination placeholders from v0.9.47. All measured separations and raw results remain. No reading is pending.
