$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$python = 'C:\Python314\python.exe'
$watcher = Join-Path $root 'control\local_watcher.py'
$startup = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
$startupCmd = Join-Path $startup 'MATA_LOCAL_WATCHER.cmd'

if (-not (Test-Path -LiteralPath $python)) { throw "Required Python was not found: $python" }
if (-not (Test-Path -LiteralPath $watcher)) { throw "Watcher was not found: $watcher" }

$taskInstalled = $false
try {
    $action = New-ScheduledTaskAction -Execute $python -Argument ('"' + $watcher + '" --poll-seconds 10') -WorkingDirectory $root
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    Register-ScheduledTask -TaskName 'MATA-AI-VIDEO-STUDIO Local Watcher' -Action $action -Trigger $trigger -Description 'Consumes ChatGPT Run Requests and writes Runner results.' -Force | Out-Null
    Start-ScheduledTask -TaskName 'MATA-AI-VIDEO-STUDIO Local Watcher'
    $taskInstalled = $true
} catch {
    Write-Host "Task Scheduler unavailable; installing current-user Startup fallback."
}

if (-not $taskInstalled) {
    New-Item -ItemType Directory -Force -Path $startup | Out-Null
    $pidPath = Join-Path $root 'control\runtime\local_watcher.pid'
    $cmd = "@echo off`r`nset `"PIDFILE=$pidPath`"`r`nif exist `"%PIDFILE%`" (`r`n  for /f %%P in (%PIDFILE%) do tasklist /FI `"PID eq %%P`" ^| find `"%%P`" ^>nul ^&^& exit /b 0`r`n)`r`nstart `"MATA Local Watcher`" /b `"$python`" `"$watcher`" --poll-seconds 10`r`n"
    [System.IO.File]::WriteAllText($startupCmd, $cmd, [System.Text.UTF8Encoding]::new($false))
    Start-Process -WindowStyle Hidden -FilePath $python -ArgumentList ('"' + $watcher + '" --poll-seconds 10') -WorkingDirectory $root
}

& (Join-Path $PSScriptRoot 'watcher_status.ps1')
