"""Non-interactive GitHub Contents API transport for the local watcher."""
from __future__ import annotations
import base64, ctypes, json, os, time
from pathlib import Path
from urllib import error, request

REPO='huao131/MATA-AI-VIDEO-STUDIO'; BRANCH='agent/issue-14-runner-bridge'; TARGET='MATA-AI-VIDEO-STUDIO/GitHubTransport'
class TransportError(Exception): pass
class AuthRequired(TransportError): pass

def credential_token() -> str:
    if os.name != 'nt': raise AuthRequired('AUTH_REQUIRED')
    class CRED(ctypes.Structure): _fields_=[('Flags',ctypes.c_uint),('Type',ctypes.c_uint),('TargetName',ctypes.c_wchar_p),('Comment',ctypes.c_wchar_p),('LastWritten',ctypes.c_longlong),('CredentialBlobSize',ctypes.c_uint),('CredentialBlob',ctypes.POINTER(ctypes.c_byte)),('Persist',ctypes.c_uint),('AttributeCount',ctypes.c_uint),('Attributes',ctypes.c_void_p),('TargetAlias',ctypes.c_wchar_p),('UserName',ctypes.c_wchar_p)]
    ptr=ctypes.POINTER(CRED)()
    if not ctypes.windll.advapi32.CredReadW(TARGET,1,0,ctypes.byref(ptr)): raise AuthRequired('AUTH_REQUIRED')
    try: return ctypes.string_at(ptr.contents.CredentialBlob,ptr.contents.CredentialBlobSize).decode('utf-16-le')
    finally: ctypes.windll.advapi32.CredFree(ptr)

class GitHubApiTransport:
 def __init__(self, token=None, timeout=30): self.token=token or credential_token(); self.timeout=timeout
 def call(self, method, path, payload=None):
  data=None if payload is None else json.dumps(payload).encode(); req=request.Request('https://api.github.com'+path,data=data,method=method,headers={'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'MATA-Local-Watcher'})
  for attempt in range(3):
   try:
    with request.urlopen(req,timeout=self.timeout) as r: return json.loads(r.read() or b'{}')
   except error.HTTPError as e:
    if e.code in (401,403): raise AuthRequired('AUTH_REQUIRED')
    if e.code==404: raise TransportError('TRANSPORT_NOT_FOUND')
    if attempt==2: raise TransportError('TRANSPORT_RETRY:'+str(e.code))
   except (error.URLError,TimeoutError) as e:
    if attempt==2: raise TransportError('TRANSPORT_RETRY')
   time.sleep(2**attempt)
 def inbox(self): return self.call('GET',f'/repos/{REPO}/contents/control/transport/inbox?ref={BRANCH}')
 def read(self,path): return json.loads(base64.b64decode(self.call('GET',f'/repos/{REPO}/contents/{path}?ref={BRANCH}')['content']).decode())
 def result(self,request_id,value):
  path=f'control/transport/results/{request_id}.json'; body={'message':f'chore(transport): publish {request_id}','branch':BRANCH,'content':base64.b64encode(json.dumps(value,ensure_ascii=False,indent=2).encode()).decode()}
  try: body['sha']=self.call('GET',f'/repos/{REPO}/contents/{path}?ref={BRANCH}')['sha']
  except TransportError: pass
  return self.call('PUT',f'/repos/{REPO}/contents/{path}',body)
