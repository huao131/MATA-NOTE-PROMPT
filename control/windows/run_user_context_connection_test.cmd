@echo off
setlocal
set "ROOT=C:\Users\huao3\OneDrive\文件\AI影音生成\MATA-AI-VIDEO-STUDIO-local-watcher"
set "LOG=%ROOT%\control\runtime\USER_CONTEXT_LAUNCHER.log"
if not exist "%ROOT%\control\runtime" mkdir "%ROOT%\control\runtime"
echo [%DATE% %TIME%] launcher started>>"%LOG%"
call "%ROOT%\control\windows\start_user_watcher.cmd" >>"%LOG%" 2>&1
"C:\Python314\python.exe" "%ROOT%\control\windows\user_context_connection_test.py" >>"%LOG%" 2>&1
set "RESULT=%ERRORLEVEL%"
if "%RESULT%"=="0" (
  powershell -NoProfile -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms;[System.Windows.Forms.MessageBox]::Show('MATA connection succeeded. ChatGPT can send tasks.','MATA')" >>"%LOG%" 2>&1
) else (
  powershell -NoProfile -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms;[System.Windows.Forms.MessageBox]::Show('Connection failed. See launcher log: %LOG%','MATA')" >>"%LOG%" 2>&1
)
echo [%DATE% %TIME%] launcher finished exit=%RESULT%>>"%LOG%"
endlocal
