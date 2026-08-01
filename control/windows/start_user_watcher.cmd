@echo off
set "ROOT=C:\Users\huao3\OneDrive\文件\AI影音生成\MATA-AI-VIDEO-STUDIO-local-watcher"
set "PYTHON=C:\Python314\pythonw.exe"
if not exist "%PYTHON%" set "PYTHON=C:\Python314\python.exe"
set "PIDFILE=%ROOT%\control\runtime\local_watcher.pid"
if exist "%PIDFILE%" for /f %%P in (%PIDFILE%) do tasklist /fi "PID eq %%P" | find "%%P" >nul && exit /b 0
set TRANSPORT_MODE=github_rest_api
start "" /b "%PYTHON%" "%ROOT%\control\local_watcher.py" --poll-seconds 10
