from __future__ import annotations
import ctypes, json, os, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RUNTIME=ROOT/'control/runtime'; LOG=RUNTIME/'USER_CONTEXT_LAUNCHER.log'
LOCK = RUNTIME/'USER_CONTEXT_LAUNCHER.lock'
def note(text):
 RUNTIME.mkdir(parents=True,exist_ok=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(text+'\n')
def main():
 lock_fd = None
 try:
  RUNTIME.mkdir(parents=True, exist_ok=True)
  try:
   lock_fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
   os.write(lock_fd, str(os.getpid()).encode())
  except FileExistsError:
   # A user double-click must not launch duplicate Watchers or dialogs.
   if time.time() - LOCK.stat().st_mtime < 300: return 0
   LOCK.unlink(missing_ok=True)
   lock_fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
   os.write(lock_fd, str(os.getpid()).encode())
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
  if code == 0:
   message = 'MATA automated production connection succeeded. ChatGPT can send tasks.'
  else:
   detail = 'UNKNOWN'
   report = RUNTIME/'USER_CONTEXT_CONNECTION_TEST_REPORT.json'
   try: detail = json.loads(report.read_text(encoding='utf-8')).get('error', detail)
   except Exception: pass
   if detail == 'GITHUB_API_401':
    message = 'GitHub rejected the saved Token (401). Open the secure setup button and save a valid Token again. No Token is shown or logged.'
   else:
    message = 'Connection failed at: ' + str(detail) + '. See: ' + str(LOG)
  ctypes.windll.user32.MessageBoxW(0,message,'MATA',0x40 if code==0 else 0x10);return code
 except Exception as e:
  note('LAUNCHER_ERROR '+str(e));ctypes.windll.user32.MessageBoxW(0,'Connection failed. See: '+str(LOG),'MATA',0x10);return 1
 finally:
  if lock_fd is not None: os.close(lock_fd)
  LOCK.unlink(missing_ok=True)
if __name__=='__main__':raise SystemExit(main())
