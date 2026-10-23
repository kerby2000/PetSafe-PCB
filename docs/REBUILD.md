# Use the project or rebuild the investigation outputs

## Ordinary use

Open `schematic/PetSafe_1001339.kicad_pro` in **KiCad 10** with its standard symbol and footprint libraries installed. Keep the whole `schematic/` directory: its project-local library tables resolve the custom and imported symbols without installing a private MCP server. The PDF is a qualified reconstruction, not a fabrication-ready PCB. The optional STEP model has separate noncommercial terms; see [publication/licensing preparation](PUBLICATION.md#licensing-proposal).

To build the **ESP32 add-on**, follow [firmware setup and flashing](../firmware/button_bridge/README.md#build-and-configure). That uses ESP-IDF v6.0.2 and does not require KiCad, the Python audit dependencies or reconstruction regeneration. Firmware remains **0.1.0**; the schematic remains **0.9.52**.

## Optional native export and reconstruction audits

Tested environment: **Windows, PowerShell, KiCad 10.0.5 and Python 3.11**. Other operating systems have not been tested for these scripts. Node.js is needed for the existing JavaScript syntax/form tests. Clone the full repository history: historical evidence checks use earlier commits and cannot run from a source-only ZIP or shallow clone.

From the repository root:

```powershell
python -m venv .venv
& .venv/Scripts/python.exe -m pip install -r tools/requirements.txt
$env:PYTHONUTF8 = '1'
./tools/build.ps1 -Python .venv/Scripts/python.exe
./tools/refresh_review.ps1 -Python .venv/Scripts/python.exe
node tools/test_measurement_form.cjs
```

The native build locates KiCad 10 in the normal Windows installation directories or on PATH. It derives the packed symbol and footprint directories from that installation. For a different installation, pass actual paths:

```powershell
./tools/build.ps1 -Python .venv/Scripts/python.exe `
  -KiCadCli 'D:/KiCad/10.0/bin/kicad-cli.exe' `
  -SymbolsDir 'D:/KiCad/10.0/share/kicad/symbols' `
  -FootprintsDir 'D:/KiCad/10.0/share/kicad/footprints'
```

`KICAD10_SYMBOL_DIR` and `KICAD10_FOOTPRINT_DIR` are also accepted. The build applies the same directories to the native CLI and Python checks, then restores the process environment. It does not edit global KiCad configuration. The standalone audits accept `--symbols` and `--footprints` respectively. They now use `sexpdata` from the listed requirements directly; **no owner's `Documents/VS.Code.Projects/KiCAD-MCP-Server` folder or external DynamicSymbolLoader is required**. Missing symbols/parents and cyclic inheritance fail explicitly. The graphical/pin comparison and imported-asset hash checks remain enforced.

Use **packed `.kicad_sym` libraries** from a matching KiCad 10 installation. Upstream's unpacked `.kicad_symdir` source checkout is not an interchangeable path for these project tables. See [official library downloads](https://www.kicad.org/libraries/download/) and [KiCad symbols packaging](https://gitlab.com/kicad/libraries/kicad-symbols/-/tree/10.0.5).

The ordinary build exports/checks the current native drawing. `-Regenerate` is optional and restores the complete reviewed owner layout from `tools/templates/mcp_standard_placements.kicad_sch`; it can overwrite manual layout edits. It is not needed to use the project or reproduce the exports. The refresh command rebuilds the existing HTML/Markdown reports from the existing register, without adding readings or reviving the retired completion PDF.

## Library failure and validation boundary

The 2026-10-18 commissioning attempt failed to load a locally modified `power.kicad_sym`. Its SHA-256 was `782ee8920a2bec30ecaf31f824d74ad814c74a81e4c98046a98f8712116fe0e9`; the previous validated exports were retained. This was an environment failure, not an accepted ERC baseline.

On 2026-10-23 the installed file already matched the earlier validated library hash, `9f49ee941555a5194f330db1363f24f339b88272a2a60c6e15da8ba11ec6d114`. Direct GND export and a fresh native ERC completed with only the **intentional U6/U6A power-output conflict**. No global library edit or schematic change was needed for this recovery. Full publication-branch check results and their exact source commit are recorded in [publication preparation](PUBLICATION.md#validation).

If a library cannot load, fix the installed library or select a known matching directory and rerun. Do not delete warnings, weaken ERC expectations, or refresh expected hashes to accept a broken environment. Successful file checks establish modeled connectivity and asset consistency, not complete physical reconstruction or power safety.
