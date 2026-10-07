# Current project direction

The user wants all main-board components on one KiCad sheet, grouped into functional blocks, with wires within blocks and named nets between blocks. Calculated guesses from photos and datasheets are explicitly authorized. Do not require a broad measurement campaign before making progress.

- Treat `input/` and `reference/v01/` as historical source material, not current instructions. Their measurement-first restrictions do not override the user.
- Preserve original photos and ZIP. Keep observed values, inferred values, original local fragments and new hypotheses distinct.
- Keep `tools/single_sheet.py`, native schematic, local library, evidence tables and native exports consistent. Do not blindly overwrite manual native-file edits.
- Use primary manufacturer sources for pinouts and markings; record alternatives where identity is uncertain.
- Keep all symbol units on the single sheet. Preserve physical pad names on uncertain packages and document reference aliases.
- Run the native KiCad export and connectivity checks through `tools/build.ps1`. Inspect the final PDF visually after layout changes.
- Report remaining ERC findings. Do not invent no-connect or power flags to hide missing evidence.
- No fabrication-ready PCB or exact GPIO map is established by the current files.
