param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    & $Python tools/reconcile_via_review.py
    if ($LASTEXITCODE) { throw 'Via evidence reconciliation failed' }
    & $Python tools/build_via_review.py
    if ($LASTEXITCODE) { throw 'Via review generation failed' }
    & $Python tools/build_via_pair_plan.py
    if ($LASTEXITCODE) { throw 'Via-pair metadata refresh failed' }
    & $Python tools/build_via_pair_guide.py --html-only
    if ($LASTEXITCODE) { throw 'Via-pair HTML refresh failed' }
    foreach ($script in @(
        'tools/build_complete_status.py',
        'tools/build_finishing_measurements.py',
        'tools/build_review.py',
        'tools/build_completion_audit.py',
        'tools/verify_evidence_contracts.py',
        'tools/verify_via_pair_plan.py',
        'tools/verify_current_review.py',
        'tools/test_review_progress.py'
    )) {
        & $Python $script
        if ($LASTEXITCODE) { throw "Review step failed: $script" }
    }
} finally { Pop-Location }
