param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    foreach ($script in @(
        'tools/build_complete_status.py',
        'tools/build_review.py',
        'tools/build_completion_audit.py',
        'tools/verify_v099_review.py',
        'tools/verify_via_pair_plan.py',
        'tools/verify_current_review.py'
    )) {
        & $Python $script
        if ($LASTEXITCODE) { throw "Review step failed: $script" }
    }
} finally { Pop-Location }
