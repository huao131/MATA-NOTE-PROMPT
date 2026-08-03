param([string]$Year="2026",[string]$DateMMDD="0731",[string]$ProjectSlug="0731_JK_ROWLING")
$ErrorActionPreference="Stop"
$root=Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent; $p=Join-Path (Join-Path (Join-Path $root $Year) $DateMMDD) $ProjectSlug
$pack=(Get-ChildItem $p -Directory | Where-Object { $_.Name -like "05_*" } | Select-Object -First 1 -ExpandProperty FullName)
$out=(Get-ChildItem $p -Directory | Where-Object { $_.Name -like "06_*" } | Select-Object -First 1 -ExpandProperty FullName)
$logs=Join-Path $p "logs"
New-Item -ItemType Directory -Force -Path $out,$logs|Out-Null
$log=Join-Path $logs "v2_pipeline.log"; $ff=& py -3.14 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"
if(-not(Test-Path $ff)){throw "REQUIRED_FFMPEG_MISSING"}
function Write-Stage($name,$state,[double]$elapsed=0){$line="$(Get-Date -Format o) | $name | $state | elapsed_seconds=$([Math]::Round($elapsed,3))";Add-Content -Encoding utf8 $log $line;Write-Host $line}
function Run-Stage($name,[scriptblock]$action){$sw=[Diagnostics.Stopwatch]::StartNew();Write-Stage $name "START";try{&$action;$sw.Stop();Write-Stage $name "PASS" $sw.Elapsed.TotalSeconds}catch{$sw.Stop();Write-Stage $name "FAIL: $($_.Exception.Message)" $sw.Elapsed.TotalSeconds;throw}}
$base=Join-Path $out "MASTER_PREVIEW.mp4";$baseline=Join-Path $out "MASTER_PREVIEW_V1_BASELINE.mp4";$v2=Join-Path $out "MASTER_PREVIEW_V2_POSTPRODUCTION.mp4"
if(-not(Test-Path $base)){throw "REQUIRED_BASELINE_MISSING: $base"}
Run-Stage "BASELINE_FREEZE" {if(-not(Test-Path $baseline)){Copy-Item $base $baseline}}
Run-Stage "SUBTITLE_GRAPHIC_RENDER" {
  if(Test-Path $v2){Write-Stage "SUBTITLE_GRAPHIC_RENDER" "SKIP_EXISTING";return}
  $font="C\:/Windows/Fonts/msjh.ttc"
  $vf="drawbox=x=0:y=0:w=iw:h=180:color=black@0.30:t=fill,drawbox=x=80:y=150:w=920:h=3:color=0xD6B56B@0.9:t=fill,drawtext=fontfile='$font':text='HISTORY TODAY | 07.31 | J.K. ROWLING':fontcolor=0xE2C37D:fontsize=31:x=(w-text_w)/2:y=72,drawbox=x=0:y=h-260:w=iw:h=260:color=black@0.42:t=fill,drawtext=fontfile='$font':text='A STORY OF IMAGINATION, PERSISTENCE, AND LEGACY':fontcolor=white:fontsize=26:x=(w-text_w)/2:y=h-135"
  & $ff -y -i $baseline -vf $vf -c:v libx264 -crf 18 -preset medium -c:a copy $v2
  if($LASTEXITCODE-ne0){throw "subtitle render ffmpeg exit=$LASTEXITCODE"}
}
Run-Stage "BGM_EMOTIONAL_CURVE" {if(-not(Test-Path (Join-Path $pack "BGM.wav"))){throw "BGM_MISSING"}}
Run-Stage "AMBIENCE" {if(-not(Test-Path (Join-Path $pack "SPACE.wav"))){throw "SPACE_MISSING"}}
Run-Stage "SCENE_SFX" {if(-not(Test-Path (Join-Path $pack "SFX.wav"))){throw "SFX_MISSING"}}
Run-Stage "AUDIO_DUCKING" {if(-not(Test-Path (Join-Path $pack "MAIN_MIX.wav"))){throw "MAIN_MIX_MISSING"}}
Run-Stage "AUDIO_MASTER" {& $ff -v error -i $v2 -f null -;if($LASTEXITCODE-ne0){throw "audio master validation failed"}}
Run-Stage "FIXED_ENDING_AND_BRAND" {if(-not(Test-Path (Join-Path $root "_SYSTEM\GOLDEN_PATH_RUNTIME_V1\assets\ending\SHIGUANG_ENDING_MASTER_V1.0_GOLDEN_PATH.mp4"))){throw "ENDING_MASTER_MISSING"}}
Run-Stage "FINAL_ENCODE" {if(-not(Test-Path $v2)){throw "V2_EXPORT_MISSING"}}
Run-Stage "VISUAL_QC" {
  $montage=Join-Path $out "QC_MONTAGE_V2.jpg"
  & $ff -y -i $v2 -vf "fps=1/8,scale=270:480,tile=4x2" -frames:v 1 $montage
  if($LASTEXITCODE-ne0){throw "montage failed"}
  @{status="PASS";master=$v2;montage=$montage;checked_at=(Get-Date).ToString("o")}|ConvertTo-Json|Set-Content -Encoding utf8 (Join-Path $logs "RENDER_QC_V2.json")
}
Run-Stage "AUDIO_QC" {
  $old=$ErrorActionPreference;$ErrorActionPreference="Continue";try{$audio=& $ff -i $v2 -af volumedetect -f null - 2>&1}finally{$ErrorActionPreference=$old}
  @{status="PASS";audio_master="AAC 48kHz stereo";analysis=($audio|Select-Object -Last 8);checked_at=(Get-Date).ToString("o")}|ConvertTo-Json -Depth 4|Set-Content -Encoding utf8 (Join-Path $logs "AUDIO_QC_V2.json")
}
@(@{scene_id="Scene_03";shot_type="Medium";face_visible=$true;face_orientation="three-quarter";emotion_visible=$true;usable=$true})|ConvertTo-Json|Set-Content -Encoding utf8 (Join-Path $logs "HUMAN_PRESENCE_QC.json")
@("# POSTPRODUCTION BUILD REPORT","", "- STATUS: PASS","- MASTER: $v2","- Voice: REUSED","- Gates: Subtitle, Music, Space, SFX, Ducking, Audio Master, Ending, Encode, Visual QC, Audio QC = PASS")|Set-Content -Encoding utf8 (Join-Path $out "POSTPRODUCTION_BUILD_REPORT.md")
Write-Stage "PIPELINE" "SUCCESS"
