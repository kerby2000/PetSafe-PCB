# First continuity pass — no modifications

Use `evidence/measurements_round1.csv` to record results. No measurements have been prefilled.

Remove all four AA cells and disconnect any external supply. Check that the board has discharged before using resistance/continuity mode. Do not use the meter's resistance mode on a powered circuit. No component removal is required for this batch.

Touch the probes together and record their resistance first. A direct copper connection should be stable and close to that value. A beep alone is not proof: resistors and semiconductor paths can also beep. Record a resistance, or OL; reverse probes when a reading is ambiguous or polarity-dependent. An in-circuit result of several ohms or more is NOT automatically a same-net connection.

## Small first batch

M01–M08 establish ground and supply domains. M09–M13 verify the programming header. M14–M17 map the motor outputs and the two control inputs. Stop there initially if time is limited. M18–M23 extend the map into the analogue supply and sensor interface.

Use `photos/U4_probe_orientation.png` and `photos/U5_probe_orientation.png`. Pin names in a semiconductor datasheet describe the IC, not a confirmed connection elsewhere on this board.

For M16/M17, hold one fine probe on U5's indicated input and sweep the listed PIC pins carefully without bridging neighbours. Record the matching PIC pin and resistance. If there is no near-zero match, report that rather than assuming a connection; a series resistor or intermediate circuit may be present.

## What is deliberately deferred

Do not cut traces, lift IC pins, reprogram the PIC, connect ESP32 outputs, switch battery chemistry or remove the RFID capacitors for this continuity pass. These actions do not help identify the first hidden connections.

The next analogue pass will trace one complete switched-capacitor branch (Q3 with C10/C12/C11), then the two op-amp feedback/input networks. It will use the already established ground/supply nodes to avoid a large blind all-pairs search.

## Values versus connectivity

A connectivity-complete schematic can still contain UNKNOWN capacitor values. A multimeter can establish which pads are joined; it generally cannot uniquely identify an unmarked capacitor value inside a connected filter or resonant network. Later LCR measurements, and sometimes lifting one end, may be needed. Do not infer capacitance, dielectric or voltage rating from physical size.
