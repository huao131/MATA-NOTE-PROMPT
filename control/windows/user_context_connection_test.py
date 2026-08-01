from __future__ import annotations
import json, os, subprocess, sys, time, uuid
from pathlib import Path
ROOT=Path(r"C:\Users\huao3\OneDrive\文件\AI影音生成\MATA-AI-VIDEO-STUDIO-local-watcher")
sys.path.insert(0,str(ROOT/'control'))
from github_api_transport import GitHubApiTransport
def main():
 report=ROOT/'control/runtime/USER_CONTEXT_CONNECTION_TEST_REPORT.json'; rid='connection-test-user-'+uuid.uuid4().hex[:12]
 try:
  t=GitHubApiTransport(); req={'request_id':rid,'request_type':'connection_test','episode_id':'CONNECTION_TEST','payload':{}}
  t.call('PUT',f'/repos/{t.REPO if hasattr(t,"REPO") else "huao131/MATA-AI-VIDEO-STUDIO"}/contents/control/transport/inbox/{rid}.json',{'message':'test: user context connection','branch':'agent/issue-14-runner-bridge','content':__import__('base64').b64encode(json.dumps(req).encode()).decode()})
  for _ in range(24):
   try:
    result=t.read(f'control/transport/results/{rid}.json')
    if result.get('outcome',{}).get('result')=='CONNECTION_TEST_SUCCESS': report.write_text(json.dumps({'status':'SUCCESS','request_id':rid},indent=2)); return 0
   except Exception: pass
   time.sleep(5)
  raise RuntimeError('RESULT_TIMEOUT')
 except Exception as e:
  report.write_text(json.dumps({'status':'BLOCKED','error':str(e)},indent=2)); return 1
if __name__=='__main__': raise SystemExit(main())
