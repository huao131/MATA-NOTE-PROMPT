param(
  [string]$BaseRoot = "C:\Users\huao3\OneDrive\A自媒體"
)
$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$SeriesRoot = Join-Path $BaseRoot "歷史上的今天"
$RuntimeRoot = Join-Path $SeriesRoot "_SYSTEM\GOLDEN_PATH_RUNTIME_V1"

New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null
Copy-Item -Force -Recurse (Join-Path $PackageRoot "runtime\*") $RuntimeRoot

# Preserve the 7/28 production pattern: Windows Python + edge-tts + ffmpeg
& py -3.14 -m pip install edge-tts
if ($LASTEXITCODE -ne 0) { throw "edge-tts installation failed under Python 3.14." }

& powershell -ExecutionPolicy Bypass -File (Join-Path $RuntimeRoot "scripts\PREFLIGHT_GOLDEN_PATH.ps1") -BaseRoot $BaseRoot
if ($LASTEXITCODE -ne 0) { throw "Golden Path preflight failed." }

Write-Host "INSTALL_STATUS=READY"
Write-Host "DAILY_COMMAND:"
Write-Host "powershell -ExecutionPolicy Bypass -File `"$RuntimeRoot\scripts\RUN_DAILY_GOLDEN_PATH.ps1`" -DateMMDD 0731 -ProjectSlug 0731_JK_ROWLING"
