param([string]$KiCadCli = '', [string]$Python = 'python', [switch]$Regenerate,
      [string]$SymbolsDir = '', [string]$FootprintsDir = '')
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousSymbols = $env:KICAD10_SYMBOL_DIR
$previousFootprints = $env:KICAD10_FOOTPRINT_DIR
Push-Location $projectRoot
try {
    if (-not $KiCadCli) {
        $candidates = @(
            (Join-Path $env:LOCALAPPDATA 'Programs/KiCad/10.0/bin/kicad-cli.exe'),
            (Join-Path $env:ProgramFiles 'KiCad/10.0/bin/kicad-cli.exe')
        )
        $KiCadCli = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
        if (-not $KiCadCli) {
            $command = Get-Command kicad-cli -ErrorAction SilentlyContinue
            if ($command) { $KiCadCli = $command.Source }
        }
    }
    if (-not $KiCadCli) { throw 'KiCad 10 CLI required. Supply -KiCadCli with its full path.' }
    $version = & $KiCadCli --version
    if ($LASTEXITCODE -or $version -notmatch '^10\.') { throw "KiCad 10 required; found $version. No fallback to the old portable KiCad 9." }
    # Use one explicit library environment for the native CLI and Python audits.
    # These are process-local overrides; do not edit global KiCad configuration.
    $share = Join-Path (Split-Path -Parent (Split-Path -Parent $KiCadCli)) 'share/kicad'
    if (-not $SymbolsDir) { $SymbolsDir = $previousSymbols }
    if (-not $FootprintsDir) { $FootprintsDir = $previousFootprints }
    if (-not $SymbolsDir) { $SymbolsDir = Join-Path $share 'symbols' }
    if (-not $FootprintsDir) { $FootprintsDir = Join-Path $share 'footprints' }
    if (-not (Test-Path -LiteralPath (Join-Path $SymbolsDir 'power.kicad_sym'))) {
        throw 'Packed KiCad 10 symbols required. Supply -SymbolsDir; see docs/REBUILD.md.'
    }
    if (-not (Test-Path -LiteralPath (Join-Path $FootprintsDir 'Device.pretty')) -and
        -not (Test-Path -LiteralPath (Join-Path $FootprintsDir 'Resistor_SMD.pretty'))) {
        throw 'KiCad 10 footprint libraries required. Supply -FootprintsDir; see docs/REBUILD.md.'
    }
    $env:KICAD10_SYMBOL_DIR = (Resolve-Path -LiteralPath $SymbolsDir).Path
    $env:KICAD10_FOOTPRINT_DIR = (Resolve-Path -LiteralPath $FootprintsDir).Path
    if ($Regenerate) {
        # Opt-in: restores the complete reviewed owner layout from its saved template.
        & $Python tools/finish_library_rebuild.py
        if ($LASTEXITCODE) { throw 'Stock-symbol routing failed. Python requires sexpdata.' }
    }
    New-Item -ItemType Directory -Force -Path output/pdf, output/svg | Out-Null
    & $KiCadCli sch export netlist --format kicadxml -o output/PetSafe_netlist.xml schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native netlist export failed.' }
    & $KiCadCli sch export pdf -o output/pdf/PetSafe_single_sheet.pdf schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native PDF export failed.' }
    & $KiCadCli sch export svg -o output/svg schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native SVG export failed.' }
    # KiCad appends trailing blanks to SVG primitives; normalize whitespace only.
    & $Python -c "from pathlib import Path; p=Path('output/svg/PetSafe_1001339.svg'); p.write_text('\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')"
    if ($LASTEXITCODE) { throw 'SVG whitespace normalization failed.' }
    & $KiCadCli sch erc --format json -o output/erc.json schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native ERC process failed.' }
    & $Python tools/validate_native.py
    if ($LASTEXITCODE) { throw 'Native connectivity validation failed.' }
    & $Python tools/verify_r39.py
    if ($LASTEXITCODE) { throw 'Bounded R39 correction failed.' }
    & $Python tools/verify_pr1_cleanup.py
    if ($LASTEXITCODE) { throw 'Documentation-only preservation check failed.' }
    & $Python tools/verify_receiver_input.py
    if ($LASTEXITCODE) { throw 'Bounded receiver-input correction failed.' }
    & $Python tools/verify_capacitor_application.py
    if ($LASTEXITCODE) { throw 'Capacitor value application validation failed.' }
    & $Python tools/verify_stock_symbols.py
    if ($LASTEXITCODE) { throw 'Library symbol verification failed.' }
    & $Python tools/audit_finalization.py
    if ($LASTEXITCODE) { throw 'Finalization audit failed.' }
    & $Python tools/verify_footprints.py
    if ($LASTEXITCODE) { throw 'Stock footprint validation failed.' }
    & $Python tools/build_review.py
    if ($LASTEXITCODE) { throw 'Review generation failed.' }
    & $Python tools/build_completion_audit.py
    if ($LASTEXITCODE) { throw 'Completion audit generation failed.' }
} finally {
    $env:KICAD10_SYMBOL_DIR = $previousSymbols
    $env:KICAD10_FOOTPRINT_DIR = $previousFootprints
    Pop-Location
}
