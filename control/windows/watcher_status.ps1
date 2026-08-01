$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$runtime = Join-Path $root 'control\runtime'
$pidPath = Join-Path $runtime 'local_watcher.pid'
$heartbeat = Join-Path $runtime 'local_watcher.heartbeat.json'
$startupCmd = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup\MATA_LOCAL_WATCHER.cmd'
$watcherPid = if (Test-Path $pidPath) { [int](Get-Content $pidPath) } else { $null }
$process = if ($watcherPid) { Get-Process -Id $watcherPid -ErrorAction SilentlyContinue } else { $null }
[pscustomobject]@{ StartupFallback = Test-Path $startupCmd; Pid = $watcherPid; ProcessRunning = $null -ne $process; Heartbeat = if (Test-Path $heartbeat) { Get-Content $heartbeat -Raw } else { $null } }
