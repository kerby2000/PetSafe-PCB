# Current project direction

The user wants all main-board components on one KiCad sheet, grouped into functional blocks, with wires within blocks and named nets between blocks. Calculated guesses from photos and datasheets are explicitly authorized. Do not require a broad measurement campaign before making progress.

- Treat `input/` and `reference/v01/` as historical source material, not current instructions. Their measurement-first restrictions do not override the user.
- Preserve original photos and ZIP. Keep observed values, inferred values, original local fragments and new hypotheses distinct.
- Use the connected KiCad MCP server and installed KiCad 10. The user's installation is 10.0.5 under LocalAppData/Programs/KiCad/10.0. Do not use the old portable KiCad 9 cache.
- Search standard KiCad libraries first. Use existing symbols and footprints. Ask the user for vendor/SnapEDA libraries before creating other missing custom symbols. On 2026-10-08 the user explicitly authorized creating S-1200B45 and MX512H from datasheets through MCP; these two project-local symbols are now implemented and do not need further approval. Keep unidentified devices as explicitly numbered stock placeholders; never silently replace fitted devices with Western alternatives.
- Keep native schematic, evidence tables, MCP placement template, routing adapter and native exports consistent. `tools/build.ps1` exports and checks without overwriting manual native edits; `-Regenerate` explicitly regenerates from the MCP template. The v0.2 custom-symbol author is historical only.
- Use primary manufacturer sources for pinouts and markings; record alternatives where identity is uncertain.
- Keep all symbol units on the single sheet. Use normal library pin numbers with physical pad names preserved in `evidence/pin_crosswalk.json`; document provisional mappings and reference aliases.
- Run the native KiCad export and connectivity checks through `tools/build.ps1`. Inspect the final PDF visually after layout changes.
- Report remaining ERC findings. Do not invent no-connect or power flags to hide missing evidence.
- No fabrication-ready PCB or exact GPIO map is established by the current files.
