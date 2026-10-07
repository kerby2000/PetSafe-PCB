param([string]$KiCadCli = 'kicad-cli', [string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    if ($KiCadCli -eq 'kicad-cli' -and -not (Get-Command kicad-cli -ErrorAction SilentlyContinue)) {
        $portable = Join-Path $projectRoot '.cache/kicad/bin/kicad-cli.exe'
        if (Test-Path -LiteralPath $portable) { $KiCadCli = $portable }
        else { throw 'KiCad CLI is required. Pass -KiCadCli with the full path to kicad-cli.exe.' }
    }
    & $Python tools/single_sheet.py
    if ($LASTEXITCODE) { throw 'Schematic generation failed.' }
    New-Item -ItemType Directory -Force -Path output/pdf, output/svg | Out-Null
    & $KiCadCli sch export netlist --format kicadxml -o output/PetSafe_netlist.xml schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native netlist export failed.' }
    & $KiCadCli sch export pdf -o output/pdf/PetSafe_single_sheet.pdf schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native PDF export failed.' }
    & $KiCadCli sch export svg -o output/svg schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native SVG export failed.' }
    & $KiCadCli sch erc --format json -o output/erc.json schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native ERC process failed.' }
    & $Python tools/validate_native.py
    if ($LASTEXITCODE) { throw 'Native connectivity validation failed.' }
    & $Python tools/build_review.py
    if ($LASTEXITCODE) { throw 'Review generation failed.' }
} finally { Pop-Location }
