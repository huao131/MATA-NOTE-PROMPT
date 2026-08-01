"""Non-interactive GitHub Contents API transport for the local watcher."""
from __future__ import annotations

import base64
import ctypes
import json
import os
import time
from urllib import error, request

REPO = "huao131/MATA-AI-VIDEO-STUDIO"
BRANCH = "agent/issue-14-runner-bridge"
CREDENTIAL_TARGET = "MATA-AI-VIDEO-STUDIO/GitHubTransport"


class TransportError(Exception):
    pass


class AuthRequired(TransportError):
    pass


def credential_token() -> str:
    """Read the current user's generic credential without exposing its value."""
    if os.name != "nt":
        raise AuthRequired("CREDENTIAL_READ_FAILED:NON_WINDOWS")

    class Credential(ctypes.Structure):
        _fields_ = [
            ("Flags", ctypes.c_uint32), ("Type", ctypes.c_uint32),
            ("TargetName", ctypes.c_wchar_p), ("Comment", ctypes.c_wchar_p),
            ("LastWritten", ctypes.c_int64), ("CredentialBlobSize", ctypes.c_uint32),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
            ("Persist", ctypes.c_uint32), ("AttributeCount", ctypes.c_uint32),
            ("Attributes", ctypes.c_void_p), ("TargetAlias", ctypes.c_wchar_p),
            ("UserName", ctypes.c_wchar_p),
        ]

    advapi = ctypes.WinDLL("Advapi32.dll", use_last_error=True)
    cred_read = advapi.CredReadW
    cred_read.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.POINTER(Credential))]
    cred_read.restype = ctypes.c_bool
    cred_free = advapi.CredFree
    cred_free.argtypes = [ctypes.c_void_p]
    cred_free.restype = None

    value = ctypes.POINTER(Credential)()
    if not cred_read(CREDENTIAL_TARGET, 1, 0, ctypes.byref(value)):
        raise AuthRequired(f"CREDENTIAL_READ_FAILED:{ctypes.get_last_error()}")
    try:
        raw = ctypes.string_at(value.contents.CredentialBlob, value.contents.CredentialBlobSize)
        token = raw.decode("utf-16-le").rstrip("\x00")
    finally:
        cred_free(value)
    if not token:
        raise AuthRequired("CREDENTIAL_READ_FAILED:EMPTY")
    return token


class GitHubApiTransport:
    def __init__(self, token: str | None = None, timeout: int = 30):
        self.token = token or credential_token()
        self.timeout = timeout

    def call(self, method: str, path: str, payload: dict | None = None):
        data = None if payload is None else json.dumps(payload).encode()
        req = request.Request(
            "https://api.github.com" + path,
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + self.token,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "MATA-Local-Watcher",
            },
        )
        for attempt in range(3):
            try:
                with request.urlopen(req, timeout=self.timeout) as response:
                    return json.loads(response.read() or b"{}")
            except error.HTTPError as exc:
                if exc.code == 401:
                    raise AuthRequired("GITHUB_API_401") from None
                if exc.code == 403:
                    raise TransportError("GITHUB_API_403") from None
                if exc.code == 404:
                    raise TransportError("TRANSPORT_NOT_FOUND") from None
                if attempt == 2:
                    raise TransportError(f"TRANSPORT_RETRY:{exc.code}") from None
            except (error.URLError, TimeoutError):
                if attempt == 2:
                    raise TransportError("TRANSPORT_RETRY") from None
            time.sleep(2**attempt)

    def inbox(self):
        return self.call("GET", f"/repos/{REPO}/contents/control/transport/inbox?ref={BRANCH}")

    def read(self, path: str):
        encoded = self.call("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")["content"]
        return json.loads(base64.b64decode(encoded).decode())

    def result(self, request_id: str, value: dict):
        path = f"control/transport/results/{request_id}.json"
        body = {
            "message": f"chore(transport): publish {request_id}",
            "branch": BRANCH,
            "content": base64.b64encode(json.dumps(value, ensure_ascii=False, indent=2).encode()).decode(),
        }
        try:
            body["sha"] = self.call("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")["sha"]
        except TransportError:
            pass
        return self.call("PUT", f"/repos/{REPO}/contents/{path}", body)
