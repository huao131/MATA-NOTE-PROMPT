param(
  [string]$BaseRoot = "C:\Users\huao3\OneDrive\A自媒體",
  [switch]$SkipVoiceNetworkCheck
)
$ErrorActionPreference = "Stop"
function ffmpeg {
  $binary = & py -3.14 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>$null
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path $binary)) { throw "FFmpeg binary unavailable." }
  $priorErrorAction = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $binary @args } finally { $ErrorActionPreference = $priorErrorAction }
}
$SeriesRoot  = Join-Path $BaseRoot "歷史上的今天"
$RuntimeRoot = Join-Path $SeriesRoot "_SYSTEM\GOLDEN_PATH_RUNTIME_V1"
$Ending      = Join-Path $RuntimeRoot "assets\ending\SHIGUANG_ENDING_MASTER_V1.0_GOLDEN_PATH.mp4"

function Fail($Code, $Message) {
  Write-Host "GOLDEN_PATH_PREFLIGHT=FAIL"
  Write-Host "BLOCKER=$Code"
  Write-Host $Message
  exit 20
}

# Python 3.14
try { $pyver = & py -3.14 -c "import sys; print(sys.version)" 2>&1 }
catch { Fail "PYTHON_3_14_MISSING" "Python 3.14 launcher not available." }

# edge-tts package
& py -3.14 -c "import edge_tts" 2>$null
if ($LASTEXITCODE -ne 0) { Fail "EDGE_TTS_MISSING" "Install with: py -3.14 -m pip install edge-tts" }

# Required voice. A validated voice checkpoint must not repeat network TTS.
if ($SkipVoiceNetworkCheck) {
  Write-Host "VOICE_NETWORK_CHECK=SKIPPED"
} else {
$VoiceTest = Join-Path $env:TEMP "golden_path_voice_test.mp3"

& py -3.14 -m edge_tts `
  --voice "zh-TW-HsiaoChenNeural" `
  --rate=-4% `
  --pitch=-2Hz `
  --text "歷史上的今天語音檢查" `
  --write-media "$VoiceTest"

if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VoiceTest)) {
  Fail "REQUIRED_VOICE_UNAVAILABLE" "zh-TW-HsiaoChenNeural synthesis failed. Fallback prohibited."
}

Remove-Item $VoiceTest -Force -ErrorAction SilentlyContinue
}

# FFmpeg / FFprobe
& ffmpeg -version *> $null
if ($LASTEXITCODE -ne 0) { Fail "FFMPEG_MISSING" "ffmpeg is not callable from PATH." }
# This runtime ships FFmpeg through imageio-ffmpeg. Validate media directly
# rather than assuming a separate ffprobe executable is on PATH.

# Runtime + Ending
if (-not (Test-Path $RuntimeRoot)) { Fail "RUNTIME_MISSING" $RuntimeRoot }
if (-not (Test-Path $Ending)) { Fail "ENDING_MASTER_MISSING" $Ending }

# Verify ending technical characteristics
$probe = & ffmpeg -v error -i "$Ending" -f null - 2>&1
if ($LASTEXITCODE -ne 0) { Fail "ENDING_MASTER_INVALID" "ffprobe failed on Ending Master." }

Write-Host "GOLDEN_PATH_PREFLIGHT=PASS"
Write-Host "PYTHON=$pyver"
Write-Host "VOICE=zh-TW-HsiaoChenNeural"
Write-Host "RATE=-4%"
Write-Host "PITCH=-2Hz"
Write-Host "FFMPEG=PASS"
Write-Host "ENDING_MASTER=$Ending"
Write-Host "RUNTIME_ROOT=$RuntimeRoot"

