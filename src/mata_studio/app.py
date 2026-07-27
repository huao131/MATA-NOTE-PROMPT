"""Application service composition."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from mata_p2.new_episode import validate_brief

from .assets import AssetService
from .drive import DriveAdapter
from .errors import StudioError
from .gates import GateService
from .handoff import HandoffService
from .store import ProjectStore
from .submission import SubmissionService, validate_submission

EPISODE_ID = re.compile(r"^(?:TEST_[A-Z0-9_]+|EP[0-9]{3,})$")


class StudioApp:
    def __init__(self, data_dir: str | Path, drive: DriveAdapter | None = None):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.store = ProjectStore(self.data_dir / "studio.db")
        self.drive = drive or DriveAdapter({})
        self.submissions = SubmissionService(self.store)
        self.gates = GateService(self.store)
        self.assets = AssetService(self.store)
        self.handoff = HandoffService(self.store)

    def status(self) -> dict[str, Any]:
        return {
            "name": "MATA AI VIDEO STUDIO",
            "version": "1.0.0",
            "bind": "localhost-only",
            "drive": self.drive.status(),
            "paid_api_calls": 0,
            "flow_operations": 0,
            "capcut_operations": 0,
        }

    def config(self) -> dict[str, Any]:
        return {
            "data_dir": str(self.data_dir),
            "cache_dir": str(self.data_dir / "cache"),
            "drive_credentials_source": "LOCAL_ENVIRONMENT_ONLY",
            "drive_client_configured": bool(os.getenv("MATA_DRIVE_CLIENT_CONFIG")),
        }

    def create_episode(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise StudioError("INVALID_EPISODE_BRIEF", "Brief 必須是 Object。")
        series_id = value.get("series_id")
        series_name = value.get("series_name")
        if not isinstance(series_id, str) or not series_id.strip():
            raise StudioError("SERIES_ID_REQUIRED", "正式 Episode 必須指定 series_id。")
        if not isinstance(series_name, str) or not series_name.strip():
            raise StudioError("SERIES_NAME_REQUIRED", "正式 Episode 必須指定 series_name。")
        if not self.store.list_series():
            self.store.create_series(series_id, series_name)
        else:
            self.store.get_series(series_id)
        p2_brief = {key: value[key] for key in (
            "episode_id", "title", "purpose", "target_audience", "duration_seconds",
            "platform", "aspect_ratio", "desired_action", "series_name",
            "existing_character_usage", "special_requirements",
        )}
        validate_brief(p2_brief)
        return self.store.create_episode(dict(value))

    def validate(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict) or "episode_id" not in value:
            raise StudioError("VALIDATION_TARGET_INVALID", "需提供含 episode_id 的 Object。")
        episode = self.store.get_episode(value["episode_id"])
        if "artifact_type" in value:
            validate_submission(value, episode)
        return {"ok": True, "result": "PASS"}
