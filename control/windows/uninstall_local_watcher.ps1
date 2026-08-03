$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$pidPath = Join-Path $root 'control\runtime\local_watcher.pid'
$startupCmd = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\MATA_LOCAL_WATCHER.cmd'
if (Test-Path $pidPath) { $watcherPid = [int](Get-Content $pidPath); Stop-Process -Id $watcherPid -Force -ErrorAction SilentlyContinue; Remove-Item $pidPath -Force -ErrorAction SilentlyContinue }
Unregister-ScheduledTask -TaskName 'MATA-AI-VIDEO-STUDIO Local Watcher' -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item $startupCmd -Force -ErrorAction SilentlyContinue
