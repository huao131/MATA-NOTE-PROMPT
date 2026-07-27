"""Asset registration and protected-state controls."""

from __future__ import annotations

from typing import Any

from mata_p0.asset_index import assert_exact_asset_operation, assert_asset_usage

from .errors import StudioError
from .store import ProjectStore


class AssetService:
    def __init__(self, store: ProjectStore):
        self.store = store

    def register(self, episode_id: str, item: Any) -> dict[str, Any]:
        if not isinstance(item, dict):
            raise StudioError("INVALID_ASSET", "Asset 必須是 Object。")
        required = ("asset_id", "version")
        missing = [key for key in required if not item.get(key)]
        if missing:
            raise StudioError("MISSING_ASSET_FIELDS", f"缺少欄位：{missing}")
        if item.get("drive_folder_id") in {"root", "ROOT"}:
            raise StudioError("DRIVE_ROOT_FORBIDDEN", "正式 Asset 不得位於 Drive 首頁。", status=409)
        item = dict(item)
        item["episode_id"] = episode_id
        return self.store.insert_asset(item)

    def transition(self, asset_id: str, action: str, payload: Any) -> dict[str, Any]:
        asset = self.store.asset(asset_id)
        if action == "approve" and asset["rejected"]:
            raise StudioError("REJECTED_ASSET_APPROVAL", "Rejected Asset 不得批准。", status=409)
        if action == "lock" and not asset["drive_file_id"]:
            raise StudioError("UNVERIFIED_DRIVE_LOCK", "未驗證 Drive File ID 不得 Lock。", status=409)
        if action not in {"approve", "reject", "lock"}:
            raise StudioError("INVALID_ASSET_ACTION", "未知 Asset 操作。")
        # MVP records transitions as new versions; it never mutates a protected file.
        return {"asset_id": asset_id, "requested_action": action, "status": "EVENT_RECORDED", "payload": payload or {}}

    def assert_usable(self, asset_id: str, role: str) -> None:
        asset = self.store.asset(asset_id)
        assert_asset_usage(
            {"lifecycle_status": "REJECTED" if asset["rejected"] else asset["lifecycle_status"]},
            role,
        )

    def exact_asset_check(self, asset_id: str, proposed_file_id: str, generated: bool) -> None:
        asset = self.store.asset(asset_id)
        metadata = {
            "exact_asset": bool(asset["exact_asset"]),
            "approved_original_drive_file_id": asset["drive_file_id"],
        }
        assert_exact_asset_operation(
            metadata,
            proposed_drive_file_id=proposed_file_id,
            generated_or_redrawn=generated,
        )
