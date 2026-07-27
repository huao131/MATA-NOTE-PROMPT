"""Localhost-only JSON API and static web server."""

from __future__ import annotations

import json
import mimetypes
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .app import StudioApp
from .constants import MAX_JSON_BYTES
from .errors import StudioError, normalize_error


def handler_factory(app: StudioApp, web_root: Path):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MATAStudio/1.0"

        def log_message(self, format: str, *args: object) -> None:
            return

        def _json(self, status: int, value: object) -> None:
            data = json.dumps(value, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _body(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            if length > MAX_JSON_BYTES:
                raise StudioError("PAYLOAD_TOO_LARGE", "JSON 超過 2MB 限制。", status=413)
            try:
                value = json.loads(self.rfile.read(length) or b"{}")
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                raise StudioError("INVALID_JSON", "JSON 格式錯誤。") from error
            if not isinstance(value, dict):
                raise StudioError("JSON_OBJECT_REQUIRED", "Request Body 必須是 Object。")
            return value

        def _serve_static(self, path: str) -> None:
            relative = "index.html" if path == "/" else path.lstrip("/")
            target = (web_root / relative).resolve()
            if web_root.resolve() not in target.parents and target != web_root.resolve():
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            if not target.is_file():
                target = web_root / "index.html"
            content = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def do_GET(self) -> None:
            try:
                path = urlparse(self.path).path
                if not path.startswith("/api/"):
                    self._serve_static(path)
                    return
                if path == "/api/openapi.json":
                    result = json.loads((web_root / "openapi.json").read_text(encoding="utf-8"))
                elif path == "/api/system/status": result = app.status()
                elif path == "/api/system/config": result = app.config()
                elif path == "/api/system/drive-status": result = app.drive.status()
                elif path == "/api/specifications/status": result = app.specification_status()
                elif path == "/api/specifications/context": result = app.specification_context('')
                elif path == "/api/series": result = app.store.list_series()
                elif path == "/api/episodes": result = app.store.list_episodes()
                elif match := re.fullmatch(r"/api/series/([^/]+)", path): result = app.store.get_series(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)", path): result = app.store.get_episode(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/state", path): result = {"production_state": app.store.get_episode(match[1])["production_state"]}
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/gates", path): result = app.store.gates(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/artifacts", path): result = app.store.artifacts(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/next-step", path): result = app.next_step(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/chatgpt-package", path): result = app.chatgpt_package(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/chatgpt-package/latest", path): result = app.chatgpt_package(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/drive-mapping", path): result = app.drive_mapping(match[1])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/artifacts/([^/]+)", path): result = app.store.artifact(match[2])
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/assets", path): result = app.store.assets(match[1])
                elif match := re.fullmatch(r"/api/assets/([^/]+)", path): result = app.store.asset(match[1])
                elif match := re.fullmatch(r"/api/assets/([^/]+)/versions", path): result = [app.store.asset(match[1])]
                elif match := re.fullmatch(r"/api/drive/folders/([^/]+)/files", path): result = app.drive.files(match[1])
                elif match := re.fullmatch(r"/api/drive/folders/([^/]+)", path): result = app.drive.folder(match[1])
                elif match := re.fullmatch(r"/api/drive/assets/([^/]+)/preview", path): result = app.store.asset(match[1])
                else: raise StudioError("ROUTE_NOT_FOUND", "找不到 API Route。", status=404)
                self._json(200, {"ok": True, "data": result})
            except Exception as error:
                normalized = normalize_error(error)
                self._json(normalized.status, normalized.payload())

        def do_POST(self) -> None:
            try:
                path, body = urlparse(self.path).path, self._body()
                status = 200
                if path == "/api/system/drive-connect":
                    result = {"status": "AUTHORIZATION_REQUIRED", "message": "請依本機 OAuth 文件設定；API 不接收或保存 Token。"}
                elif path == "/api/system/validate": result = app.validate(body)
                elif path == "/api/series": result, status = app.store.create_series(body["series_id"], body["name"]), 201
                elif path == "/api/episodes": result, status = app.create_episode(body), 201
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/artifacts", path): result, status = app.submissions.submit(match[1], body), 201
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/artifacts/([^/]+)/validate", path): result = app.validate({**body, "episode_id": match[1]})
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/gates/([^/]+)/submit", path): result = app.gates.submit(match[1], match[2], body.get("artifact_version", ""))
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/gates/([^/]+)/(approve|reject)", path): result = app.gates.decide(match[1], match[2], "PASS" if match[3] == "approve" else "REJECTED", body)
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/chatgpt-import", path): result, status = app.chatgpt_import(match[1], body.get("raw_text", "")), 201
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/chatgpt-import/validate", path): result = app.chatgpt_import(match[1], body.get("raw_text", ""))
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/drive-mapping", path): result, status = app.drive_mapping(match[1]), 200
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/assets/register", path): result, status = app.assets.register(match[1], body), 201
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/assets/upload", path): raise StudioError("DRIVE_UPLOAD_REQUIRES_OAUTH", "請先完成 Drive OAuth，且只能上傳至已驗證 Folder ID。", status=503)
                elif match := re.fullmatch(r"/api/assets/([^/]+)/(approve|reject|lock)", path): result = app.assets.transition(match[1], match[2], body)
                elif match := re.fullmatch(r"/api/drive/episodes/([^/]+)/initialize-folders", path): raise StudioError("DRIVE_AUTHORIZATION_REQUIRED", "需 OAuth 與明確資料夾建立授權。", status=503)
                elif match := re.fullmatch(r"/api/drive/assets/([^/]+)/sync", path): raise StudioError("DRIVE_AUTHORIZATION_REQUIRED", "需 OAuth 才能同步。", status=503)
                elif match := re.fullmatch(r"/api/episodes/([^/]+)/export/(flow-package|editing-package|episode-summary)", path): result = app.handoff.export(match[1], match[2])
                else: raise StudioError("ROUTE_NOT_FOUND", "找不到 API Route。", status=404)
                self._json(status, {"ok": True, "data": result})
            except Exception as error:
                normalized = normalize_error(error)
                self._json(normalized.status, normalized.payload())

        def do_PATCH(self) -> None:
            try:
                path, body = urlparse(self.path).path, self._body()
                match = re.fullmatch(r"/api/episodes/([^/]+)", path)
                if not match:
                    raise StudioError("ROUTE_NOT_FOUND", "找不到 API Route。", status=404)
                self._json(200, {"ok": True, "data": app.store.update_episode(match[1], body)})
            except Exception as error:
                normalized = normalize_error(error)
                self._json(normalized.status, normalized.payload())

    return Handler


def serve(app: StudioApp, host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise StudioError("PUBLIC_BIND_FORBIDDEN", "MVP 只允許 localhost。")
    root = Path(__file__).with_name("web")
    server = ThreadingHTTPServer((host, port), handler_factory(app, root))
    print(f"MATA AI VIDEO STUDIO: http://{host}:{port}")
    server.serve_forever()
