# Remaining open items

Current schematic **v0.9.48**. Generated from [the authoritative register](../evidence/remaining_work.json); edit that source, not this view.

[Schematic and PCB photographs](../README.md) | [HTML checklist](FINISHING_CHECKLIST.html) | [History and closed findings](history/README.md)

Owner action: none. No pending readings. RX-3 is deferred and unmeasured; completed RX-1/RX-2 and earlier C20 checks are not repeated. [Independent connection audit](TOPOLOGY_AUDIT.md). Supported copper, device interpretation and operating validation are distinct claims.

| ID | Area | Category |
|---|---|---|
| [E03](#e03) | RF supply and Q8 drive | Device function/rating; operating behaviour |
| [E04](#e04) | Antenna and tuning-cell topology | Physical pin mapping; device function/rating |
| [E07](#e07) | PIR: Q2 behavior and operating supply | Device function/rating; operating behaviour |
| [E08](#e08) | Receiver and Q7 operating behavior | Device function/rating; operating behaviour |
| [E09](#e09) | Supply voltages and Q1 control | Device function/rating; operating behaviour |
| [E10](#e10) | D6 breakdown and ICSP compatibility | Device function/rating |
| [I01](#i01) | Candidate device identities and pin roles | Physical pin mapping; device function/rating |
| [V01](#v01) | Capacitor values and passive ratings | Reproduction/package (values and passive ratings) |
| [M01](#m01) | LED footprint and mechanical qualification | Reproduction/package |
| [E11](#e11) | Inherited copper joins without independent closure | Copper connection; evidence coverage |

<a id="e03"></a>
## E03 - RF supply and Q8 drive

| Field | Current position |
|---|---|
| Category | Device function/rating; operating behaviour |
| Known | C5/C6 and Q8 source/ground/outer-drain joins supported. U2/C7 supply now fed from H_RF_VDD through R5 (22 ohm): local and endpoint readings B78-B81 support this route. U2 supply = 6.3 V; direct difference to printed VDD = +1.8 V rejects old VDD tie. Q8 output-to-ANT1 accepted from visible copper and compatible B82 4.5-ohm reading with antenna fitted. Rest gate-source voltages: P=0 V, N=+6.3 V. TI lists C14R among the DBV candidate markings; absolute maximum VCC is 6.5 V, distinct from the 5.5-V recommended maximum. |
| Unresolved claim | Exact U2 identity and compatibility with measured 6.3 V remain unresolved; candidate SN74LVC2G14 recommended supply maximum is 5.5 V. Q8 switching margin, timing and RF waveform validation are deferred by owner. B82 alone is not a zero-ohm proof; output route is photo-supported. |
| Next Codex action | Photo and device-consistency review completed in TOPOLOGY_AUDIT.md. Keep the measured 6.3 V U2 feed and explicit 5.5 V recommended-limit conflict; no justified device replacement or further copper correction. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | U2 identity and voltage compatibility resolved; RF operating waveform validation recorded separately when the owner resumes scope work. Local RF supply/output drawing is corrected; unknown C6/C7 values remain V01. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [q3_deferred_q8_followup_20261009.json](../evidence/q3_deferred_q8_followup_20261009.json), [q8_supply_result_20261009.json](../evidence/q8_supply_result_20261009.json), [supply_baseline_results_20261014.json](../evidence/supply_baseline_results_20261014.json), [q8_gate_bias_results_20261014.json](../evidence/q8_gate_bias_results_20261014.json), [u2_supply_join_results_20261014.json](../evidence/u2_supply_join_results_20261014.json), [u2_supply_voltage_result_20261014.json](../evidence/u2_supply_voltage_result_20261014.json), [u2_vdd_separation_result_20261014.json](../evidence/u2_vdd_separation_result_20261014.json), [u2_c7_feed_results_20261015.json](../evidence/u2_c7_feed_results_20261015.json), [r5_supply_feed_results_20261015.json](../evidence/r5_supply_feed_results_20261015.json), [q8_output_antenna_result_20261015.json](../evidence/q8_output_antenna_result_20261015.json), [u2_r5_topology_correction_v0940.json](../evidence/u2_r5_topology_correction_v0940.json), [circuit_consistency_v0942.json](../evidence/circuit_consistency_v0942.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="e04"></a>
## E04 - Antenna and tuning-cell topology

| Field | Current position |
|---|---|
| Category | Physical pin mapping; device function/rating |
| Known | PIC-to-control resistors and local tuning midpoints are mapped. B44/B45 midpoint-to-antenna DC readings are OL. B52 C11 outer end to ANT2 = 1.4 ohm; photo-shared outer pads of C14/C29/C44/C47 now join ANT2. Rear capacitor returns remain GND. ANT1-ANT2 is about 5 ohm with antenna fitted. The mistaken 414 kohm N-B report was corrected to B-G. Q3 L-S latest 0.48 V, L-R 2.3 V; all other diode directions OL. Antenna inductance now reported as 500 uH; test conditions not specified. Existing V090/095/100/103/107 owner reports reconciled individually with original rear lands in IMG_2442 now support all five front/rear midpoint links. Seven OL midpoint exclusions remain. |
| Unresolved claim | Tuning transistor family, native pin-role interpretation and switching behavior remain unresolved. The five midpoint correspondences now have owner-report plus original-photo support; this does not validate the PNP device model or capacitor estimates. |
| Next Codex action | Keep copper and starred values unchanged. Preserve Q3 diode results and qualify the device model independently of the now-supported midpoint joins. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Tuning device pin roles and switched RF behavior are supported; outer ANT2 path is already resolved. |

Evidence: [architect_review_v0930.json](../evidence/architect_review_v0930.json), [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [q3_diode_results_20261009.json](../evidence/q3_diode_results_20261009.json), [q3_deferred_q8_followup_20261009.json](../evidence/q3_deferred_q8_followup_20261009.json), [finishing_measurements.json](../evidence/finishing_measurements.json), [antenna_midpoint_results_20261014.json](../evidence/antenna_midpoint_results_20261014.json), [antenna_outer_rail_results_20261014.json](../evidence/antenna_outer_rail_results_20261014.json), [antenna_outer_rail_correction_v0937.json](../evidence/antenna_outer_rail_correction_v0937.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="e07"></a>
## E07 - PIR: Q2 behavior and operating supply

| Field | Current position |
|---|---|
| Category | Device function/rating; operating behaviour |
| Known | J3/U7 ordering, U6 external pads and PIC21/TP16/Q2 output routing are established. U6 pin5 is tied to VIN; pin4 is unused. B58 measured 3.3 V at J3.1 with PIR connected; logic VDD was 4.5 V. R39.1 joins TP16/Q2.S/PIC21 by continuous copper in original IMG_2425; R39.2 remains VDD. Earlier base-side assignment is withdrawn. |
| Unresolved claim | Q2 terminal functions, PIR raw-signal behavior and PIC input response remain unverified. The loaded PIR supply is established at 3.3 V in the reported state; transients and other states are not characterized. |
| Next Codex action | Photo and device-consistency review completed in TOPOLOGY_AUDIT.md. R39 endpoint correction and native regression completed; Q2 identity and enabled behavior remain qualified. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Q2 signal behavior and U6 output are supported by device or operating evidence. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [r33_withdrawal_v0932.json](../evidence/r33_withdrawal_v0932.json), [supply_baseline_results_20261014.json](../evidence/supply_baseline_results_20261014.json), [r39_endpoint_correction_v0945.json](../evidence/r39_endpoint_correction_v0945.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="e08"></a>
## E08 - Receiver and Q7 operating behavior

| Field | Current position |
|---|---|
| Category | Device function/rating; operating behaviour |
| Known | U3.5/VREF and R23/R42/C40, C23/R25/R48 and DNP R47/C42 paths are reconciled. VREF supplies U3 pins3 and5, with pin3 newly identified by the owner; C25.1-TP6.1 measured 1.5 ohm joins the receiver filter to PIC2/RA0. Powered: VREF 0 V, TP5 0.066 V, R19 left/right 0/4.5 V. Both R19-to-Q7 joins measured 1.5 ohm. Q7 diode results: R->L 0.74 V, L->R 1.74 V, S->L 0.74 V, L->S OL. These support PNP polarity with L as base; reverse finite reading can include parallel-board paths. B71 direct QR-QL measured 0 V, consistent with no forward base-emitter bias in the latest state and the low receiver supply; stability not reported. |
| Unresolved claim | Why the receiver is inactive and its enabled-state behavior remain unverified. Earlier separate 0/4.5 V readings conflict with the later direct 0 V; do not diagnose failure or assume simultaneous identical states. Exact Q7 identity and E/C selection remain qualified. Receiver gain/filter response and MCU interface roles are unverified; DC readings do not exclude pulses. The new VREF connection establishes U3.3 bias routing. RX-1/RX-2 exclusions remain; the supported C19/C20 destinations are recorded under E11. This does not establish enabled-state gain or timing. |
| Next Codex action | Retain the established receiver feedback and U3.3/U3.5 VREF reference. Keep the owner-supported C19/C20 destinations and measured separations. Operating behavior remains deferred, separate from copper. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Receiver supply, bias and the existing RA0/RA1/RB4 interfaces have supported operating roles; no presumed extra output wire is required. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [ra0_tp6_connection_v0938.json](../evidence/ra0_tp6_connection_v0938.json), [supply_baseline_results_20261014.json](../evidence/supply_baseline_results_20261014.json), [receiver_supply_results_20261014.json](../evidence/receiver_supply_results_20261014.json), [q7_r19_voltage_results_20261014.json](../evidence/q7_r19_voltage_results_20261014.json), [q7_r19_join_results_20261014.json](../evidence/q7_r19_join_results_20261014.json), [q7_diode_results_20261014.json](../evidence/q7_diode_results_20261014.json), [q7_direct_bias_result_20261014.json](../evidence/q7_direct_bias_result_20261014.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="e09"></a>
## E09 - Supply voltages and Q1 control

| Field | Current position |
|---|---|
| Category | Device function/rating; operating behaviour |
| Known | VSYS/RF 6.3 V, printed VDD 4.5 V, PIR supply 3.3 V with PIR attached; VREF 0 V and red LED approximately 1 Hz. TP14 is on U5.8/OUTA at 1.5 ohm, with R43.2/V015; BATTERY+ stays separate. Receiver TP5 = 0.066 V (B62). R44 = 15 kohm (B83); TP14-to-Q1 presumed gate recheck = 21.4/21.7 kohm (B84/B85). The earlier 516-ohm conflict is not reproduced and no wiring change is warranted. |
| Unresolved claim | Q1 fitted identity, terminal roles and powered control behavior remain unverified. The resistance recheck is compatible with R44 in the path but does not prove an intact MOSFET or the exact remaining path. Q1/motor dynamics and R3/R4/C28 sensing role remain qualified. |
| Next Codex action | Photo and device-consistency review completed in TOPOLOGY_AUDIT.md. R44 local route corroborated; 516-ohm contradiction stays closed by B84/B85. Q1 roles/control remain qualified. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Actual supply levels and control behavior are recorded without merging battery, VSYS or filtered branches. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [supply_baseline_results_20261014.json](../evidence/supply_baseline_results_20261014.json), [product_manual_led_review_20261014.json](../evidence/product_manual_led_review_20261014.json), [tp14_motor_output_correction_v0939.json](../evidence/tp14_motor_output_correction_v0939.json), [receiver_supply_results_20261014.json](../evidence/receiver_supply_results_20261014.json), [circuit_consistency_v0942.json](../evidence/circuit_consistency_v0942.json), [r44_resistance_result_20261015.json](../evidence/r44_resistance_result_20261015.json), [q1_gate_recheck_results_20261015.json](../evidence/q1_gate_recheck_results_20261015.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="e10"></a>
## E10 - D6 breakdown and ICSP compatibility

| Field | Current position |
|---|---|
| Category | Device function/rating |
| Known | D6 anode is GND and cathode is VPP; forward drop is about 0.7V and reverse diode mode is OL. J1 pin order is resolved. Primary programming specification DS40001753B requires 8.0-9.0 V for high-voltage entry; low-voltage entry exists only when LVP is enabled. |
| Unresolved claim | G3 is nonunique: MMSZ5228BS is 3.9 V; PZU2.4B is 2.4 V. Neither rating has been measured on this board. A directly connected clamp of either rating would load the required high-voltage ICSP level. The current PIC LVP configuration and actual D6 breakdown are unknown. |
| Next Codex action | Photo and device-consistency review completed in TOPOLOGY_AUDIT.md. Measured polarity is distinct from unmeasured breakdown; no safe in-circuit identification step is justified here. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Clamp class/rating is established or explicitly bounded for reconstruction, and programming compatibility is checked. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [d6_programming_review_20261009.json](../evidence/d6_programming_review_20261009.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="i01"></a>
## I01 - Candidate device identities and pin roles

| Field | Current position |
|---|---|
| Category | Physical pin mapping; device function/rating |
| Known | Manufacturer candidate datasheets and pin tables exist. D2 local wiring is complete; measured R -> S -> L diode behavior supports a series pair. |
| Unresolved claim | Exact fitted identity/ratings remain candidates for D1-D6, Q1-Q8/Q11, U1/U2/U6. The 4P marking alone does not identify three-pin D2; a manufacturer 4P code for a two-pin diode is incompatible. |
| Next Codex action | Photo and device-consistency review completed in TOPOLOGY_AUDIT.md. D2 series-junction equivalent documented separately from its unchanged physical placeholder. Primary U2/Q3 sources checked; remaining identities stay candidates. |
| Owner input | None now. Scope and component-isolation work are deferred by owner. |
| Closure evidence | Each part has a supported pin/function model and adequate ratings or an explicit accepted-equivalent limitation; exact branding is not falsely claimed. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json).

<a id="v01"></a>
## V01 - Capacitor values and passive ratings

| Field | Current position |
|---|---|
| Category | Reproduction/package (values and passive ratings) |
| Known | C5 is 470uF/16V; L1/L2 reported 1.4/2.2uH. Marked resistors are recorded. All 44 unknown ceramics now have numerical design candidates: 12 supply, 17 signal/timing and 15 tuning-bank parts, with proposed ratings/dielectrics. PetSafe variant FAQ supports 134.2 kHz. C21/C22 raw auto-mode readings remain preserved. Native v0.9.44 now displays all 44 estimates with asterisks. The owner reports antenna inductance of 500 uH; test conditions are unspecified. |
| Unresolved claim | The 44 original fitted ceramic values remain unconfirmed. Numerical choices are explicit design proposals. The RF bank uses the reported 500 uH and assumes ideal switches. Inductance test conditions, weights/order, voltage stress and firmware tuning remain unverified. Receiver/timing choices and L1/L2 ratings also need qualification. |
| Next Codex action | Preserve all 44 starred estimates and their qualifications. Capacitor selection is outside this topology task. |
| Owner input | None for this task; value/package qualification remains later work. |
| Closure evidence | Candidate choices are validated for the intended reconstruction; original-value and original-rating claims remain separate unless independently established. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [receiver_capacitance_test_plan_20261015.json](../evidence/receiver_capacitance_test_plan_20261015.json), [receiver_capacitance_results_20261015.json](../evidence/receiver_capacitance_results_20261015.json), [capacitor_value_review_20261015.json](../evidence/capacitor_value_review_20261015.json), [antenna_inductance_results_20261015.json](../evidence/antenna_inductance_results_20261015.json), [capacitor_application_v0944.json](../evidence/capacitor_application_v0944.json).

<a id="m01"></a>
## M01 - LED footprint and mechanical qualification

| Field | Current position |
|---|---|
| Category | Reproduction/package |
| Known | LED1 is the only unassigned footprint; R30/PIC23 lights red and R31/PIC22 lights green. C5 diameter/height, S1 body/actuator size, R8 and C11 sizes are already measured. J5 rear placement and both board contacts are mapped to U5 outputs from front/rear photos. |
| Unresolved claim | LED1 land pattern/manufacturer numbering and internal pairing of its externally grounded cathode pads remain unverified. C5 pitch and S1 pad fit/3D heights are reproduction qualifications, not unknown schematic wires. J5 stock-footprint pad order/pitch and external motor harness colours remain unverified. |
| Next Codex action | Preserve measured body dimensions and candidate footprints. LED1 pad geometry and exact fit remain reproduction prerequisites, outside this task. |
| Owner input | None for this task; value/package qualification remains later work. |
| Closure evidence | LED footprint has a supported pad map; remaining package-fit assumptions are documented separately from schematic connectivity. |

Evidence: [remaining_work.json](../docs/history/v0.9.30-before-finalization/evidence/remaining_work.json), [led1_colour_results_20261009.json](../evidence/led1_colour_results_20261009.json), [j5_photo_review_20261009.json](../evidence/j5_photo_review_20261009.json).

<a id="e11"></a>
## E11 - Inherited copper joins without independent closure

| Field | Current position |
|---|---|
| Category | Copper connection; evidence coverage |
| Known | Owner now identifies U3.3 as VREF; C20 upper/model1 as R42 lower/model2/D3.S; C19 lower/model1 as C20 lower/model2/R28 right/model2/D2.R. C19 upper/model2 remains R29 right/model2/GND. Completed C20-to-U3.3=1.023 Mohm, C20-to-TP7=998 kohm, C20-to-R28 right=1.5 ohm, RX-1=1.023 Mohm and RX-2=271 kohm retain their original meaning. These joins resolve all three isolated receiver endpoints and their four ERC findings without suppressions. Earlier R39, R10/V116 and R2/C4 ground recoveries remain. |
| Unresolved claim | Remaining undetermined bridges: U1 native3-VIN; R18.2-Q7.L; R20.2 and TP5.1 to C24.1/U3.8; R3.2-R4.1-C28.1; U5.1/C34.1 and J1.VDD to printed VDD; twelve candidate ground groups individually listed in TOPOLOGY_AUDIT.md. Six modeled nets retain incomplete independent evidence groups. Receiver terminal destinations are now reported; circuit operating roles and device identities remain separately qualified. |
| Next Codex action | Keep the three supported receiver joins and earlier measured separations. Preserve the specifically qualified remaining copper groups and intentional U6A ERC conflict; no new measurement campaign. |
| Owner input | Owner action: none. No pending readings. RX-3 is deferred and unmeasured; completed RX-1/RX-2 and earlier C20 checks are not repeated. |
| Closure evidence | Remaining named copper gaps acquire independent support or a documented disposition; reported receiver terminal routes are now incorporated without claiming verified dynamic function. |

Evidence: [physical_evidence_review_20261015.json](../evidence/physical_evidence_review_20261015.json), [topology_closure_audit.json](../evidence/topology_closure_audit.json), [d2_diode_20261009.json](../evidence/d2_diode_20261009.json), [receiver_input_bridge.svg](../docs/measurement-images/receiver_input_bridge.svg), [receiver_input_results_20261015.json](../evidence/receiver_input_results_20261015.json), [receiver_input_correction_v0946.json](../evidence/receiver_input_correction_v0946.json), [finishing_measurements.json](../evidence/finishing_measurements.json), [receiver_input_correction_v0947.json](../evidence/receiver_input_correction_v0947.json), [receiver_connections_v0948.json](../evidence/receiver_connections_v0948.json).

## Accepted reconstruction boundaries

These are acknowledged limits, not closed physical findings.

### E06 - PIC14/TP11 and PIC18/TP17: hidden continuation not excluded

**Disposition:** Drawing resolved; physical completeness unproved

PIC14/RC3 reaches TP11; PIC18/RC7 reaches TP17. Front/rear photos show no onward surface route. Both local routes are represented and are valid endpoints.

**Not established:** Additional inner-layer branches and firmware purpose remain unverified; test-only use is not asserted.

**Reopen when:** A specific unassigned destination, contradictory continuity result, inner-layer image or firmware evidence identifies an onward connection that the current drawing omits.

DNP options retain all modeled local routes and candidate roles. J6.2/R36.1 terminates at an unpopulated external interface; no additional onboard rail is assumed. U6A stays a regulator symbol with its visible output conflict by explicit user choice.

## Reproduction requirements

No routed reproduction PCB exists.

- **Electrical design:** Resolve the active main-board issue groups, recover critical values, and qualify candidate pin functions/ratings. TP11/TP17 hidden-layer completeness remains a documented reconstruction limitation.

- **Mechanical fit:** Dimensioned board perimeter, mounting holes, connector positions and lead geometry; LED land pattern.

- **Copper and stackup:** No routed PCB exists; four layers remain a hypothesis. Continuity identifies nets, not hidden track geometry or dielectric thickness.

- **Firmware and configuration:** No PIC firmware/configuration backup is present. An identical populated board needs the program and configuration, or compatible replacement firmware.

- **Complete working assembly:** Powered validation, motor/antenna/PIR integration, and daughterboard internals if that board is also being copied.
