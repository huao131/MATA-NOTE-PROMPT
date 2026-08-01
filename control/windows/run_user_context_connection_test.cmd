@echo off
call "%~dp0start_user_watcher.cmd"
"C:\Python314\python.exe" "%~dp0user_context_connection_test.py"
if errorlevel 1 (msg * "MATA接線失敗。請查看 control\runtime\USER_CONTEXT_CONNECTION_TEST_REPORT.json" ) else (msg * "MATA自動製片接線成功。之後可由ChatGPT發送任務。")
