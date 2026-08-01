from __future__ import annotations
import ctypes, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(r"C:\Users\huao3\OneDrive\文件\AI影音生成\MATA-AI-VIDEO-STUDIO-local-watcher")
RUNTIME=ROOT/'control/runtime'; LOG=RUNTIME/'USER_CONTEXT_LAUNCHER.log'
def note(text):
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(text+'\n')
def main():
 try:
  env=os.environ.copy();env['TRANSPORT_MODE']='github_rest_api'
  pid=RUNTIME/'local_watcher.pid'
  if pid.exists():
   try: subprocess.run(['taskkill','/PID',pid.read_text().strip(),'/F'],capture_output=True,timeout=10)
   except Exception: pass
   pid.unlink(missing_ok=True)
  note('REST_WATCHER_START')
  subprocess.Popen([r'C:\Python314\pythonw.exe',str(ROOT/'control/local_watcher.py'),'--poll-seconds','10'],cwd=ROOT,env=env)
  time.sleep(3)
  code=subprocess.call([r'C:\Python314\python.exe',str(ROOT/'control/windows/user_context_connection_test.py')],cwd=ROOT,env=env)
  message='MATA automated production connection succeeded. ChatGPT can send tasks.' if code==0 else 'Connection failed. See: '+str(LOG)
  ctypes.windll.user32.MessageBoxW(0,message,'MATA',0x40 if code==0 else 0x10);return code
 except Exception as e:
  note('LAUNCHER_ERROR '+str(e));ctypes.windll.user32.MessageBoxW(0,'Connection failed. See: '+str(LOG),'MATA',0x10);return 1
if __name__=='__main__':raise SystemExit(main())
