param([string]$KiCadCli = '', [string]$Python = 'python', [switch]$Regenerate)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
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
    if ($Regenerate) {
        # Opt-in: replaces manual native edits from the saved MCP placement template.
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
    & $KiCadCli sch erc --format json -o output/erc.json schematic/PetSafe_1001339.kicad_sch
    if ($LASTEXITCODE) { throw 'Native ERC process failed.' }
    & $Python tools/validate_native.py
    if ($LASTEXITCODE) { throw 'Native connectivity validation failed.' }
    & $Python tools/verify_footprints.py
    if ($LASTEXITCODE) { throw 'Stock footprint validation failed.' }
    & $Python tools/build_review.py
    if ($LASTEXITCODE) { throw 'Review generation failed.' }
    & $Python tools/build_completion_audit.py
    if ($LASTEXITCODE) { throw 'Completion audit generation failed.' }
} finally { Pop-Location }
