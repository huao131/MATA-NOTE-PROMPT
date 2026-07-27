"""Flow, editing, and summary package exports without external execution."""

from __future__ import annotations

from typing import Any

from .errors import StudioError
from .store import ProjectStore


class HandoffService:
    def __init__(self, store: ProjectStore):
        self.store = store

    def export(self, episode_id: str, package_type: str) -> dict[str, Any]:
        episode = self.store.get_episode(episode_id)
        artifacts = self.store.artifacts(episode_id)
        assets = [asset for asset in self.store.assets(episode_id) if not asset["rejected"]]
        allowed = {"flow-package", "editing-package", "episode-summary"}
        if package_type not in allowed:
            raise StudioError("INVALID_HANDOFF", "未知 Handoff 類型。")
        if package_type == "flow-package":
            required = {"STORYBOARD", "KEYFRAME_DEFINITION"}
        elif package_type == "editing-package":
            required = {"TIMELINE", "VOICEOVER", "SRT_MANIFEST"}
        else:
            required = {"EPISODE_BRIEF"}
        present = {item["artifact_type"] for item in artifacts}
        missing = sorted(required - present)
        if missing:
            raise StudioError("HANDOFF_DEPENDENCY_MISSING", f"缺少上游 Artifact：{missing}", status=409)
        return {
            "episode_id": episode_id,
            "package_type": package_type,
            "status": "CANDIDATE",
            "external_execution": False,
            "artifacts": [item["artifact_id"] for item in artifacts],
            "asset_ids": [item["asset_id"] for item in assets],
        }
