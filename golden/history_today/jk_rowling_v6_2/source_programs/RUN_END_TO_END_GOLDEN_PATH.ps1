param(
  [string]$BaseRoot = "C:\Users\huao3\OneDrive\A自媒體",
  [string]$Year = "2026",
  [string]$DateMMDD = "0731",
  [string]$ProjectSlug = "0731_JK_ROWLING"
)

$ErrorActionPreference = "Stop"
$FfmpegPath = & py -3.14 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>$null
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $FfmpegPath)) { throw "FFmpeg binary unavailable." }
Set-Alias -Name ffmpeg -Value $FfmpegPath -Scope Script
function Get-MediaDuration([string]$Path) {
  $priorErrorAction = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { $lines = & ffmpeg -hide_banner -i $Path 2>&1 } finally { $ErrorActionPreference = $priorErrorAction }
  $match = ($lines | Select-String -Pattern 'Duration:\s*(\d{2}):(\d{2}):(\d{2}\.\d+)').Matches | Select-Object -First 1
  if (-not $match) { return $null }
  $h=[double]$match.Groups[1].Value; $m=[double]$match.Groups[2].Value; $s=[double]$match.Groups[3].Value
  return ($h*3600 + $m*60 + $s)
}

function Fail([string]$Stage, [string]$Message, [int]$Code=50) {
  Write-Host "END_TO_END=FAIL"
  Write-Host "FAILED_STAGE=$Stage"
  Write-Host "MESSAGE=$Message"
  exit $Code
}

$SeriesRoot  = Join-Path $BaseRoot "歷史上的今天"
$RuntimeRoot = Join-Path $SeriesRoot "_SYSTEM\GOLDEN_PATH_RUNTIME_V1"
$ProjectRoot = Join-Path (Join-Path (Join-Path $SeriesRoot $Year) $DateMMDD) $ProjectSlug

$Narration = Join-Path $ProjectRoot "02_腳本\narration.txt"
$ScenePlan = Join-Path $ProjectRoot "02_腳本\scene_plan.json"
$Editorial = Join-Path $ProjectRoot "02_腳本\editorial_layout.json"
$AudioPlan = Join-Path $ProjectRoot "02_腳本\audio_plan.json"
$SubRead   = Join-Path $ProjectRoot "02_腳本\subtitle_reading_version.txt"

$VoiceMp3  = Join-Path $ProjectRoot "04_配音\voice_full.mp3"
$VoiceSrt  = Join-Path $ProjectRoot "04_配音\voice_full.srt"
$VisualDir = Join-Path $ProjectRoot "03_視覺素材"
$PackDir   = Join-Path $ProjectRoot "05_剪映素材包"
$OutDir    = Join-Path $ProjectRoot "06_成品"
$LogDir    = Join-Path $ProjectRoot "logs"

foreach($d in @($VisualDir,$PackDir,$OutDir,$LogDir)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

Write-Host "=================================================="
Write-Host "HISTORY TODAY END-TO-END GOLDEN PATH"
Write-Host "PROJECT=$ProjectRoot"
Write-Host "=================================================="

# STAGE 0: PRECHECK INPUTS
foreach($f in @($Narration,$ScenePlan,$Editorial,$AudioPlan,$SubRead)) {
  if(-not (Test-Path $f)) { Fail "INPUTS" "Missing input: $f" 51 }
}
Write-Host "STAGE_INPUTS=PASS"

# STAGE 1 + 2: CHECKPOINT-AWARE PREFLIGHT / VOICE
$Preflight = Join-Path $RuntimeRoot "scripts\PREFLIGHT_GOLDEN_PATH.ps1"
if(-not (Test-Path $Preflight)) { Fail "PREFLIGHT" "Missing preflight: $Preflight" 52 }

$VoiceState = Join-Path $LogDir "voice_first_state.json"
$VoiceCheckpoint = Join-Path $LogDir "CHECKPOINT_VOICE_READY.json"
$voiceReady = $false

if ((Test-Path $VoiceMp3) -and (Test-Path $VoiceSrt)) {
  $probeDuration = Get-MediaDuration $VoiceMp3
  if ($probeDuration) { $voiceReady = $true }
}

if($voiceReady) {
  Write-Host "CHECKPOINT_DETECTED=VOICE_READY"
  & powershell -ExecutionPolicy Bypass -File $Preflight -BaseRoot $BaseRoot -SkipVoiceNetworkCheck
} else {
  & powershell -ExecutionPolicy Bypass -File $Preflight -BaseRoot $BaseRoot
}
if($LASTEXITCODE -ne 0) { Fail "PREFLIGHT" "Golden Path preflight failed." 53 }
Write-Host "STAGE_PREFLIGHT=PASS"

if($voiceReady) {
  Write-Host "STAGE_VOICE=RESUME_FROM_CHECKPOINT"
  Write-Host "VOICE_GENERATION=SKIPPED"
} else {
  $VoiceGen = Join-Path $RuntimeRoot "scripts\generate_voice_and_srt.py"
  if(-not (Test-Path $VoiceGen)) { Fail "VOICE" "Missing voice generator." 54 }
  & py -3.14 $VoiceGen $Narration $VoiceMp3 $VoiceSrt
  if($LASTEXITCODE -ne 0) { Fail "VOICE" "Edge TTS generation failed." 55 }
}

if(-not (Test-Path $VoiceMp3)) { Fail "VOICE" "voice_full.mp3 missing after generation." 56 }
$VoiceDurationRaw = Get-MediaDuration $VoiceMp3
if(-not $VoiceDurationRaw) { Fail "VOICE" "Unable to read voice duration." 57 }
$VoiceDuration = [double]$VoiceDurationRaw

# Refresh canonical Voice checkpoint even when resumed.
$voiceStateObj = @{
  narration_duration_seconds = $VoiceDuration
  scene_count = 5
  voice_first = $true
  ending_breath_seconds = 0.9
  status = "VOICE_READY_FOR_SCENE_RETIMING"
  updated_at = (Get-Date).ToString("o")
}
$voiceStateObj | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $VoiceState

$checkpointObj = @{
  checkpoint = "VOICE_READY"
  checkpoint_version = "1.0"
  status = "PASS"
  project = $ProjectSlug
  voice_engine = "Microsoft Edge TTS"
  voice_id = "zh-TW-HsiaoChenNeural"
  rate = "-4%"
  pitch = "-2Hz"
  voice_mp3 = $VoiceMp3
  voice_srt = $VoiceSrt
  narration_duration_seconds = $VoiceDuration
  resume_from = "VISUAL_RENDER"
  resume_rule = "Existing valid Voice artifacts skip redundant online TTS preflight and regeneration."
  refreshed_at = (Get-Date).ToString("o")
}
$checkpointObj | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $VoiceCheckpoint
New-Item -ItemType Directory -Force -Path (Join-Path $RuntimeRoot "checkpoints") | Out-Null
$checkpointObj | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $RuntimeRoot "checkpoints\LATEST_VOICE_READY.json")

Write-Host "STAGE_VOICE=PASS"
Write-Host "CHECKPOINT=VOICE_READY"
Write-Host "VOICE_DURATION_SECONDS=$VoiceDuration"

# STAGE 3: VISUAL INPUT CHECK
# The production rule is 5 clean 9:16 scene images, no storyboard crops.
$sceneFiles = 1..5 | ForEach-Object { Join-Path $VisualDir ("Scene_{0:D2}.png" -f $_) }
$missingScenes = @($sceneFiles | Where-Object { -not (Test-Path $_) })

if($missingScenes.Count -gt 0) {
  $manifest = @{
    status = "BLOCKED"
    failed_stage = "VISUAL_RENDER"
    requirement = "Five clean 9:16 cinematic scene images"
    missing = $missingScenes
    rule = "Storyboard/composite crops are prohibited as final visual assets."
  } | ConvertTo-Json -Depth 5
  $manifest | Set-Content -Encoding UTF8 (Join-Path $LogDir "END_TO_END_BLOCKER.json")
  Fail "VISUAL_RENDER" ("Missing clean Scene images: " + ($missingScenes -join ", ")) 60
}
Write-Host "STAGE_VISUAL_RENDER=PASS"

# STAGE 4: VOICE-FIRST TIMING
# Existing legacy scene_plan files may have damaged source encoding. The 5-scene
# production invariant is still authoritative; use equal scene weights if JSON
# parsing is unavailable, without modifying frozen narration or voice assets.
$weights = @(1,1,1,1,1)
$totalWeight = 5
$scenePlanRaw = Get-Content $ScenePlan -Raw
try {
  $plan = $scenePlanRaw | ConvertFrom-Json
  if(@($plan).Count -ne 5) { throw "Scene plan must contain exactly five scenes." }
  $weights = @($plan | ForEach-Object { [Math]::Max(1, ($_.narration | Out-String).Trim().Length) })
  $totalWeight = ($weights | Measure-Object -Sum).Sum
  Write-Host "SCENE_PLAN_TIMING=CONTENT_WEIGHTED"
} catch {
  Write-Host "SCENE_PLAN_TIMING=EQUAL_FIVE_SCENE_FALLBACK"
  Write-Host "SCENE_PLAN_PARSE=SKIPPED_LEGACY_ENCODING"
}
$sceneDurations = @()
for($i=0;$i -lt 5;$i++){
  $raw = ($VoiceDuration * $weights[$i] / $totalWeight)
  $sceneDurations += [Math]::Max(5.0, $raw)
}
$sumDur = ($sceneDurations | Measure-Object -Sum).Sum
if($sumDur -lt $VoiceDuration) {
  $sceneDurations[4] += ($VoiceDuration - $sumDur)
}

$timing = @()
$cursor = 0.0
for($i=0;$i -lt 5;$i++){
  $d = [Math]::Round($sceneDurations[$i],3)
  $timing += [pscustomobject]@{
    scene = $i+1
    start = [Math]::Round($cursor,3)
    duration = $d
    end = [Math]::Round($cursor+$d,3)
  }
  $cursor += $d
}
$timing | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $LogDir "scene_timing.json")
Write-Host "STAGE_TIMING=PASS"

# STAGE 5: BUILD EACH SCENE VIDEO WITH SLOW CINEMATIC MOTION
$sceneVideos = @()
for($i=0;$i -lt 5;$i++){
  $img = $sceneFiles[$i]
  $dur = [double]$timing[$i].duration
  $sceneOut = Join-Path $PackDir ("scene_{0:D2}.mp4" -f ($i+1))
  if ((Test-Path $sceneOut) -and ((Get-Item $sceneOut).Length -gt 1024)) {
    Write-Host ("SCENE_{0:D2}=SKIPPED_EXISTING" -f ($i+1))
    $sceneVideos += $sceneOut
    continue
  }

  # alternating subtle motion to avoid PPT feel
  if(($i % 2) -eq 0) {
    $vf = "scale=1200:2134,crop=1080:1920:x='(iw-ow)/2 + 10*sin(t/4)':y='(ih-oh)/2',zoompan=z='min(zoom+0.00018,1.06)':d=1:s=1080x1920:fps=30,format=yuv420p"
  } else {
    $vf = "scale=1200:2134,crop=1080:1920:x='(iw-ow)/2 - 10*sin(t/4)':y='(ih-oh)/2',zoompan=z='min(zoom+0.00012,1.045)':d=1:s=1080x1920:fps=30,format=yuv420p"
  }

  & ffmpeg -y -loop 1 -i "$img" -t $dur -vf $vf -r 30 -c:v libx264 -pix_fmt yuv420p -an "$sceneOut"
  if($LASTEXITCODE -ne 0) { Fail "SCENE_MOTION" "Failed rendering $sceneOut" 62 }
  $sceneVideos += $sceneOut
}
Write-Host "STAGE_SCENE_MOTION=PASS"

# STAGE 6: CONCAT SCENES
$concat = Join-Path $PackDir "concat.txt"
($sceneVideos | ForEach-Object { "file '$([IO.Path]::GetFileName($_).Replace("'","''"))'" }) | Set-Content -Encoding ASCII $concat
$videoNoAudio = Join-Path $PackDir "VIDEO_NO_AUDIO.mp4"
& ffmpeg -y -f concat -safe 0 -i "$concat" -c copy "$videoNoAudio"
if($LASTEXITCODE -ne 0) { Fail "VIDEO_CONCAT" "Scene concat failed." 63 }
Write-Host "STAGE_VIDEO_CONCAT=PASS"

# STAGE 7: SOUND BED
# Generate deterministic warm harmonic bed + room tone using FFmpeg lavfi.
$mainDur = [Math]::Max($VoiceDuration + 0.9, [double]$cursor)
$bgm = Join-Path $PackDir "BGM.wav"
$space = Join-Path $PackDir "SPACE.wav"
$sfx = Join-Path $PackDir "SFX.wav"

$bgmFilter = "sine=f=196:r=48000:d=$mainDur,volume=0.035[a];sine=f=246.94:r=48000:d=$mainDur,volume=0.025[b];sine=f=293.66:r=48000:d=$mainDur,volume=0.02[c];[a][b][c]amix=inputs=3,afade=t=in:st=0:d=1,afade=t=out:st=$([Math]::Max(0,$mainDur-1.2)):d=1.2"
& ffmpeg -y -f lavfi -i "$bgmFilter" -ar 48000 -ac 2 "$bgm"
if($LASTEXITCODE -ne 0) { Fail "AUDIO_BGM" "BGM generation failed." 64 }

& ffmpeg -y -f lavfi -i "anoisesrc=color=brown:amplitude=0.006:duration=${mainDur}:sample_rate=48000" -af "lowpass=f=600,afade=t=in:st=0:d=1,afade=t=out:st=$([Math]::Max(0,$mainDur-1.2)):d=1.2" -ar 48000 -ac 2 "$space"
if($LASTEXITCODE -ne 0) { Fail "AUDIO_SPACE" "Space generation failed." 65 }

# Opening clock ticks + page turns approximate with short tonal/noise cues.
$tick = "sine=f=680:r=48000:d=0.10,volume=0.06"
$page = "anoisesrc=color=white:amplitude=0.03:duration=0.75:sample_rate=48000,lowpass=f=1800,highpass=f=180"
$inputs = @()
$filters = @()
$idx = 0
foreach($t in @(0.45,1.60,2.75,3.90)){
  $inputs += @("-f","lavfi","-i",$tick)
  $delay = [int]($t*1000)
  $filters += "[${idx}:a]adelay=$delay|$delay[t$idx]"
  $idx++
}
foreach($tm in @($timing[0].end,$timing[1].end,$timing[2].end,$timing[3].end)){
  $inputs += @("-f","lavfi","-i",$page)
  $delay = [int](([double]$tm)*1000)
  $filters += "[${idx}:a]adelay=$delay|$delay[p$idx]"
  $idx++
}
$labels = (0..($idx-1) | ForEach-Object { if($_ -lt 4){"[t$_]"}else{"[p$_]"} }) -join ""
$filters += "${labels}amix=inputs=${idx}:normalize=0[sfx]"
$filterComplex = $filters -join ";"
& ffmpeg -y @inputs -filter_complex $filterComplex -map "[sfx]" -t $mainDur -ar 48000 -ac 2 "$sfx"
if($LASTEXITCODE -ne 0) { Fail "AUDIO_SFX" "SFX generation failed." 66 }
Write-Host "STAGE_SOUND_DESIGN=PASS"

# STAGE 8: MIX WITH SIDECHAIN DUCKING + MASTER
$mix = Join-Path $PackDir "MAIN_MIX.wav"
$fc = "[1:a][0:a]sidechaincompress=threshold=0.035:ratio=7:attack=18:release=350[duck];[duck][2:a][3:a]amix=inputs=3:normalize=0[bed];[0:a][bed]amix=inputs=2:normalize=0,acompressor=threshold=-20dB:ratio=2:attack=10:release=160:makeup=1.8,loudnorm=I=-16:TP=-1.5:LRA=10,alimiter=limit=0.94[out]"
& ffmpeg -y -i "$VoiceMp3" -i "$bgm" -i "$space" -i "$sfx" -filter_complex $fc -map "[out]" -ar 48000 -ac 2 "$mix"
if($LASTEXITCODE -ne 0) { Fail "AUDIO_MIX" "Sidechain/master mix failed." 67 }
Write-Host "STAGE_AUDIO_MIX=PASS"

# STAGE 9: MUX MAIN VIDEO + AUDIO
$main = Join-Path $PackDir "MAIN_STORY.mp4"
& ffmpeg -y -i "$videoNoAudio" -i "$mix" -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest "$main"
if($LASTEXITCODE -ne 0) { Fail "MAIN_MUX" "Main mux failed." 68 }
Write-Host "STAGE_MAIN_MUX=PASS"

# STAGE 10: ENDING CONCAT
$ending = Join-Path $RuntimeRoot "assets\ending\SHIGUANG_ENDING_MASTER_V1.0_GOLDEN_PATH.mp4"
if(-not (Test-Path $ending)) { Fail "ENDING" "Ending Master missing: $ending" 69 }

# Normalize both streams to identical codec parameters before concat
$mainN = Join-Path $PackDir "MAIN_STORY_NORMALIZED.mp4"
$endN = Join-Path $PackDir "ENDING_NORMALIZED.mp4"
& ffmpeg -y -i "$main" -vf "scale=1080:1920,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 "$mainN"
if($LASTEXITCODE -ne 0) { Fail "ENDING_PREP" "Main normalization failed." 70 }
& ffmpeg -y -i "$ending" -vf "scale=1080:1920,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 "$endN"
if($LASTEXITCODE -ne 0) { Fail "ENDING_PREP" "Ending normalization failed." 71 }

$finalList = Join-Path $PackDir "final_concat.txt"
@("file '$([IO.Path]::GetFileName($mainN))'","file '$([IO.Path]::GetFileName($endN))'") | Set-Content -Encoding ASCII $finalList

$master = Join-Path $OutDir "MASTER_PREVIEW.mp4"
& ffmpeg -y -f concat -safe 0 -i "$finalList" -c copy "$master"
if($LASTEXITCODE -ne 0) { Fail "MASTER_EXPORT" "Final concat/export failed." 72 }

Write-Host "STAGE_ENDING=PASS"
Write-Host "STAGE_MASTER_EXPORT=PASS"
Write-Host "END_TO_END=PASS"
Write-Host "MASTER_PREVIEW=$master"
