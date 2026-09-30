# One-command setup: creates .venv (if missing), installs requirements,
# and runs the tools/examples as a smoke test.
#
# Usage:  .\setup.ps1
# If PowerShell blocks the script, run it once with:
#   powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

$venvPython = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment in .venv ..."
    python -m venv .venv
} else {
    Write-Host ".venv already exists, skipping creation."
}

Write-Host "Installing requirements ..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host ""
Write-Host "Running tools/examples as a smoke test ..."
$failed = $false
Get-ChildItem tools\examples\*.json | Sort-Object Name | ForEach-Object {
    Write-Host "=== $($_.Name) ==="
    & $venvPython tools\verify_lp.py $_.FullName
    $exitCode = $LASTEXITCODE
    # 05_wrong_claim.json is a deliberately wrong claim and is expected to FAIL (exit 1).
    if ($exitCode -ne 0 -and $_.Name -ne "05_wrong_claim.json") {
        $failed = $true
    }
    Write-Host ""
}

if ($failed) {
    Write-Host "Setup finished, but one or more examples failed unexpectedly. Check the output above." -ForegroundColor Red
    exit 1
}

Write-Host "Setup complete. Run Python for this project with: .\.venv\Scripts\python"
