$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$python = (Get-Command python -ErrorAction Stop).Source
$watcher = Join-Path $root 'control\local_watcher.py'
$action = New-ScheduledTaskAction -Execute $python -Argument ('"' + $watcher + '" --poll-seconds 10') -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName 'MATA-AI-VIDEO-STUDIO Local Watcher' -Action $action -Trigger $trigger -Description 'Consumes ChatGPT Run Requests and writes Runner results.' -Force
Start-ScheduledTask -TaskName 'MATA-AI-VIDEO-STUDIO Local Watcher'
