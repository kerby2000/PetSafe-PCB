# Codex task: complete the PetSafe as-built schematic reconstruction

## Goal

Continue the attached `PetSafe_RE_v01` project into a complete, evidence-backed KiCad schematic of the existing **100-1339 R03 A** main PCB, then the **100-1398 R001** PIR daughterboard. Preserve original reference designators. This is NOT an ESP32 add-on design task.

## Starting point

Read README.md and AGENTS.md. Inspect the original photographs, not just stitched seams. Open `schematic/PetSafe_1001339.kicad_pro`. The current generated files have only structural validation; first establish that they open in native KiCad and fix any format issues without inventing electrical content. Then export a native netlist and SVG/PDF preview and record exactly which checks ran.

There are 150 catalog entries and 29 visual local net fragments, not a finished netlist. Pin identifiers for unknown packages are physical placeholders. The independent SVG preview is not evidence that KiCad accepted the project.

## Work autonomously where the evidence permits

1. Audit the photo-derived component inventory against all original images. Correct duplicated/missing aliases, reference-designator readings, marking transcription, population status and package pin orientation. Do not invent components merely because a reference number is skipped.
2. Use manufacturer datasheets to resolve IC identities. U3 is SGM8542XS, U4 PIC16F18855 (28-pin SOIC), U5 MX512H. U1 marking PPEK; U2 approximately C14R with six leads; U6 marking uncertain. Short marking matches with a different pin count/package are not acceptable identifications.
3. Expand only genuinely visible copper connections. Each electrical net must retain photo and/or measurement evidence. Update evidence/reconstruction.json, the generator/model and KiCad together. Do not populate a schematic by copying a datasheet application circuit.
4. Incorporate Sergey's measurements from measurements_round1.csv. Use actual resistance readings, not beeper-only guesses. Direct copper, semiconductor paths and resistance through another component are different findings.
5. Trace the full ground/supply domains, ICSP header, motor inputs/outputs, crystal, user switch/LED, PIR interface, receiver and antenna drive/tuning networks. Many apparently isolated vias may connect through hidden layers; the physical route need not be known if endpoint continuity is proven.
6. After the first measurement batch, request only the next small high-information batch with precise pin/pad names and annotated crop references. Complete one tuning branch (Q3, C10/C12/C11) before assuming the topology of the other four. Do not assume those three capacitors are simply parallel.
7. Move from the provisional component-grid capture to readable functional circuitry as nets become established. Keep an unresolved-pins register until every fitted component pin and intentional empty footprint is accounted for.
8. Add the daughterboard as its own hierarchical sheet, preserving its local designators without collisions. Request a clear opposite-side photograph only if needed; do not infer its three-wire protocol or logic level from wire colors.

## Deliverables

A native KiCad project that has actually been opened/exported; readable circuit sheets; an as-built BOM with unknown fields explicit; an evidence-linked netlist; the measurement history; an unresolved-items list; and an updated photo atlas. Capacitor values may require later LCR/isolated measurements. Connectivity completion and value completion must be reported separately.

## Acceptance conditions

No fabricated wires/values, no ambiguous part identified solely by a short code, no unverified ground merges, no NC flags used to hide unknowns. Native exports and ERC results must be reported honestly. Preserve factory firmware and physical hardware. Do not claim completion until every connection has evidence or is explicitly unresolved.
