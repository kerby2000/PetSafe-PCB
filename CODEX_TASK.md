# Continue the KiCad 10 single-sheet reconstruction

Read README.md and docs/LIBRARIES_AND_ALTERNATIVES.md. Use the existing connected KiCad MCP Server with installed KiCad 10.0.5. The active schematic is one A2 sheet containing all 150 catalog entries with 22 stock symbol definitions and no custom library.

Preserve the normal KiCad pin numbers and evidence/pin_crosswalk.json mappings to all 352 physical pads. The 81 modeled net partitions and 29 original visual fragments pass native export checks. ERC has 80 open findings; placeholders have passive pins and incomplete checking. The reconstruction remains inferred, not hardware verified.

Ask for vendor/SnapEDA symbols before creating missing custom symbols. U1 (S-1200B45) and U5 (MX512H) await exact symbols; U6 and Q8 await identification. SGM8542 uses the stock generic dual op-amp. MCP6002-I/SN and DRV8212PDSGR are documented Western alternatives, not substitutions applied to this board.

tools/build.ps1 exports/validates current files without regeneration. -Regenerate explicitly recreates routing around the saved MCP placement template; preserve manual edits before using it. The old custom-symbol author is retired under reference/v02 and refuses direct execution. Never reinstate the old six-sheet grid or silently return to KiCad 9.
