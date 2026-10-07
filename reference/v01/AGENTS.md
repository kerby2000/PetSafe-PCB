# Project-specific instructions

Reconstruct the AS-BUILT PetSafe 100-1339 R03 A. Do not design a similar generic RFID circuit.

Preserve original photos and their names. Image stitching may warp/register/crop source pixels, but must never inpaint or generate electrical detail. Inspect original sources when a seam affects a trace.

Distinguish visible copper, electrical measurements, datasheet pin definitions and circuit hypotheses. A datasheet proves a pin's function, not its PCB net. No fabricated component values, hidden power connections, net assignments, tests or measurements.

Treat open captured pins as unresolved, not NC. Do not populate empty footprints as zero-ohm links. Do not merge identically named supply pads without evidence. Layer count remains unconfirmed.

Keep the native KiCad project, evidence model and readable documentation in agreement. First validate that the generated project opens in an installed KiCad. Do not claim an ERC pass when checks were not run or suppress unresolved-input errors just to achieve a green report.

Hardware changes, firmware replacement and rechargeable-power redesign are outside this reconstruction task. Ask Sergey for small grouped continuity measurements at named physical pads rather than broad exploratory work.
