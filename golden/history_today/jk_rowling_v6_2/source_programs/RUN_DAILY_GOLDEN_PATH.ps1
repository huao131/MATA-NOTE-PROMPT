param(
  [Parameter(Mandatory=$true)][string]$DateMMDD,
  [Parameter(Mandatory=$true)][string]$ProjectSlug,
  [string]$Year = "2026",
  [string]$BaseRoot = "C:\Users\huao3\OneDrive\A自媒體"
)
$ErrorActionPreference = "Stop"
$SeriesRoot  = Join-Path $BaseRoot "歷史上的今天"
$RuntimeRoot = Join-Path $SeriesRoot "_SYSTEM\GOLDEN_PATH_RUNTIME_V1"
$ProjectRoot = Join-Path (Join-Path (Join-Path $SeriesRoot $Year) $DateMMDD) $ProjectSlug

# 0. Golden Path preflight
& powershell -ExecutionPolicy Bypass -File (Join-Path $RuntimeRoot "scripts\PREFLIGHT_GOLDEN_PATH.ps1") -BaseRoot $BaseRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 1. Daily canonical folders
$folders = @(
  "01_研究資料","02_腳本","03_視覺素材","04_配音",
  "05_剪映素材包","06_成品","logs"
)
foreach ($f in $folders) { New-Item -ItemType Directory -Force -Path (Join-Path $ProjectRoot $f) | Out-Null }

$narration = Join-Path $ProjectRoot "02_腳本\narration.txt"
$voiceMp3  = Join-Path $ProjectRoot "04_配音\voice_full.mp3"
$voiceSrt  = Join-Path $ProjectRoot "04_配音\voice_full.srt"

if (-not (Test-Path $narration)) {
  Write-Host "BLOCKED=SCRIPT_NOT_READY"
  Write-Host "Expected: $narration"
  exit 21
}

# 2. One continuous Microsoft Edge TTS narration + boundaries
& py -3.14 (Join-Path $RuntimeRoot "scripts\generate_voice_and_srt.py") $narration $voiceMp3 $voiceSrt
if ($LASTEXITCODE -ne 0) {
  Write-Host "BLOCKED=VOICE_MODULE"
  exit $LASTEXITCODE
}

# 3. Voice-first: get true narration duration; downstream scene timing reads this value.
$duration = & ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$voiceMp3"
$duration = [double]$duration
$timingJson = @{
  narration_duration_seconds = $duration
  scene_count = 5
  voice_first = $true
  ending_breath_seconds = 0.9
  ending_master = (Join-Path $RuntimeRoot "assets\ending\SHIGUANG_ENDING_MASTER_V1.0_GOLDEN_PATH.mp4")
  status = "VOICE_READY_FOR_SCENE_RETIMING"
} | ConvertTo-Json -Depth 5
$timingJson | Set-Content -Encoding UTF8 (Join-Path $ProjectRoot "logs\voice_first_state.json")

Write-Host "DAILY_GOLDEN_PATH_STAGE=VOICE_READY"
Write-Host "PROJECT_ROOT=$ProjectRoot"
Write-Host "VOICE_DURATION_SECONDS=$duration"
Write-Host "NEXT=Scene retiming -> editorial subtitles -> sound mix -> ending -> MASTER_PREVIEW"
