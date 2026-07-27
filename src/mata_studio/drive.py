"""Google Drive adapter contracts; credentials never enter the repository."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .constants import ROOT_FOLDER_CODE
from .errors import StudioError


class DriveTransport(Protocol):
    def folder(self, folder_id: str) -> dict[str, Any]: ...
    def files(self, folder_id: str) -> list[dict[str, Any]]: ...
    def create_folder(self, name: str, parent_id: str) -> dict[str, Any]: ...
    def upload(self, name: str, parent_id: str, content: bytes, mime_type: str) -> dict[str, Any]: ...


@dataclass(slots=True)
class DriveAdapter:
    registry: dict[str, dict[str, Any]]
    transport: DriveTransport | None = None

    @property
    def connected(self) -> bool:
        return self.transport is not None

    def status(self) -> dict[str, Any]:
        return {"status": "CONNECTED" if self.connected else "NOT_CONNECTED", "real_e2e": "AVAILABLE" if self.connected else "NOT_EXECUTED_DUE_TO_AUTHORIZATION"}

    def _require(self) -> DriveTransport:
        if self.transport is None:
            raise StudioError("DRIVE_NOT_CONNECTED", "Google Drive 尚未授權。", status=503)
        return self.transport

    def folder(self, folder_id: str, expected_parent_id: str | None = None) -> dict[str, Any]:
        if folder_id in {"", "root", "ROOT"}:
            raise StudioError("DRIVE_ROOT_FORBIDDEN", "不得以 Drive 首頁作正式位置。", status=409)
        metadata = self._require().folder(folder_id)
        if expected_parent_id and expected_parent_id not in metadata.get("parents", []):
            raise StudioError("PARENT_FOLDER_MISMATCH", "Parent Folder ID 不符。", status=409)
        return metadata

    def files(self, folder_id: str) -> list[dict[str, Any]]:
        self.folder(folder_id)
        return self._require().files(folder_id)

    def ensure_child(self, name: str, parent_id: str, authorized: bool) -> dict[str, Any]:
        self.folder(parent_id)
        matches = [item for item in self._require().files(parent_id) if item.get("name") == name and item.get("mimeType") == "application/vnd.google-apps.folder"]
        if len(matches) > 1:
            raise StudioError("DUPLICATE_DRIVE_FOLDER", "同名資料夾不唯一。", status=409)
        if matches:
            return matches[0]
        if not authorized:
            raise StudioError("DRIVE_CREATE_NOT_AUTHORIZED", "未授權建立 Drive 資料夾。", status=403)
        return self._require().create_folder(name, parent_id)

    def upload(self, name: str, folder_id: str, content: bytes, mime_type: str) -> dict[str, Any]:
        self.folder(folder_id)
        result = self._require().upload(name, folder_id, content, mime_type)
        if folder_id not in result.get("parents", []):
            raise StudioError("UPLOAD_PARENT_MISMATCH", "上傳後 Parent ID 回讀不符。", status=409)
        if not result.get("id"):
            raise StudioError("UPLOAD_FILE_ID_MISSING", "上傳後未取得 File ID。", status=409)
        return result

    def validate_canonical_root(self) -> dict[str, Any]:
        root = self.registry.get(ROOT_FOLDER_CODE)
        if not root or root.get("verification_status") != "VERIFIED":
            raise StudioError("CANONICAL_ROOT_UNVERIFIED", "正式 Drive 根目錄尚未 VERIFIED。", status=409)
        return self.folder(root["google_drive_folder_id"])


class MockDriveTransport:
    """Deterministic contract transport used only by tests."""

    def __init__(self, folders: dict[str, dict[str, Any]] | None = None):
        self.folders = folders or {}
        self.children: dict[str, list[dict[str, Any]]] = {}
        self.counter = 0

    def folder(self, folder_id: str) -> dict[str, Any]:
        if folder_id not in self.folders:
            raise StudioError("DRIVE_FOLDER_NOT_FOUND", "Folder ID 不存在。", status=404)
        return self.folders[folder_id]

    def files(self, folder_id: str) -> list[dict[str, Any]]:
        self.folder(folder_id)
        return list(self.children.get(folder_id, []))

    def create_folder(self, name: str, parent_id: str) -> dict[str, Any]:
        self.counter += 1
        item = {"id": f"mock-folder-{self.counter}", "name": name, "parents": [parent_id], "mimeType": "application/vnd.google-apps.folder"}
        self.folders[item["id"]] = item
        self.children.setdefault(parent_id, []).append(item)
        return item

    def upload(self, name: str, parent_id: str, content: bytes, mime_type: str) -> dict[str, Any]:
        self.counter += 1
        item = {"id": f"mock-file-{self.counter}", "name": name, "parents": [parent_id], "mimeType": mime_type, "size": len(content), "thumbnailLink": f"mock://thumbnail/{self.counter}", "webViewLink": f"mock://file/{self.counter}"}
        self.children.setdefault(parent_id, []).append(item)
        return item
