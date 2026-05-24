#Requires -Version 5.1
# Windows entrypoint for the verification script.
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
& python "$PSScriptRoot/verify.py"
exit $LASTEXITCODE
