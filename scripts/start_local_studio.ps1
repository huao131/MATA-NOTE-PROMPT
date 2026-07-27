$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $repoRoot 'src'
if (-not $env:MATA_STUDIO_DATA_DIR) {
    $env:MATA_STUDIO_DATA_DIR = Join-Path $repoRoot '.local\mata-studio'
}
$port = if ($env:MATA_STUDIO_PORT) { [int]$env:MATA_STUDIO_PORT } else { 8765 }
Write-Host "Starting MATA AI VIDEO STUDIO at http://127.0.0.1:$port"
python -m mata_studio --host 127.0.0.1 --port $port --data-dir $env:MATA_STUDIO_DATA_DIR
