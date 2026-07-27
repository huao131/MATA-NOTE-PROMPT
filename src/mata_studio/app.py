"""Application service composition."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from mata_p2.new_episode import validate_brief

from .assets import AssetService
from .chatgpt_import import ChatGPTImportParser
from .context_package import build_context_package
from .drive import DriveAdapter
from .drive_mapping import get_drive_mapping
from .errors import StudioError
from .gates import GateService
from .handoff import HandoffService
from .next_step import evaluate_next_step
from .specifications import SpecificationResolver
from .store import ProjectStore
from .submission import SubmissionService, validate_submission
from .git_context import build_git_context

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
        self.chatgpt_import = ChatGPTImportParser(self.store)

    def status(self) -> dict[str, Any]:
        specification_context = self.specification_status()
        git_context = build_git_context(repo_root=self.data_dir.parent.parent if self.data_dir.name == 'data' else self.data_dir)
        drive_status = self.drive.status()
        return {
            "name": "LOCAL STUDIO V1.1",
            "version": "1.0.0",
            "bind": "localhost-only",
            "drive": drive_status,
            "paid_api_calls": 0,
            "flow_operations": 0,
            "capcut_operations": 0,
            "git_build_context": git_context,
            "specification_context": specification_context,
            "google_drive_sync_status": drive_status.get("status", "NOT_CONNECTED"),
            "working_tree_dirty": git_context.get("working_tree_dirty", False),
            "uncommitted_changes_count": git_context.get("uncommitted_changes_count", 0),
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

    def specification_status(self) -> dict[str, Any]:
        resolver = SpecificationResolver(repo_root=self.data_dir.parent.parent if self.data_dir.name == 'data' else self.data_dir, ref='review/v2-system-specification-publication-v2')
        try:
            return resolver.resolve(['README.md', 'system/MASTER_EXECUTION_SPEC_V1.0_FINAL_LOCK.md'])
        except Exception as error:
            return {'status': 'SPECIFICATION_CONTEXT_UNAVAILABLE', 'reason': str(error)}

    def specification_context(self, episode_id: str) -> dict[str, Any]:
        return {
            'episode_id': episode_id,
            'source_ref': 'review/v2-system-specification-publication-v2',
            'source_commit_sha': '036b88eada48991258640bb7ba524f770dc374cc',
            'sop_version': 'V2.0',
            'documents': [],
        }

    def next_step(self, episode_id: str) -> dict[str, Any]:
        episode = self.store.get_episode(episode_id)
        return evaluate_next_step(
            episode_id=episode_id,
            brief=episode['brief'],
            production_state=episode['production_state'],
            gates={gate['gate_id']: gate for gate in self.store.gates(episode_id)},
            artifacts=self.store.artifacts(episode_id),
            approvals={},
            locks={},
            rejected_assets=[],
            dependency_status={},
            drive_status=self.drive.status(),
            specification_context=self.specification_context(episode_id),
        )

    def chatgpt_package(self, episode_id: str) -> dict[str, Any]:
        episode = self.store.get_episode(episode_id)
        return build_context_package(
            episode_id=episode_id,
            brief=episode['brief'],
            production_state=episode['production_state'],
            gates={gate['gate_id']: gate for gate in self.store.gates(episode_id)},
            artifacts=self.store.artifacts(episode_id),
            approvals={},
            locks={},
            rejected_assets=[],
            dependency_status={},
            drive_status=self.drive.status(),
            specification_context=self.specification_context(episode_id),
            drive_mapping=self.drive_mapping(episode_id),
        )

    def chatgpt_import(self, episode_id: str, raw_text: str) -> dict[str, Any]:
        payload = self.chatgpt_import.import_payload(episode_id, raw_text)
        artifact_id = f"{episode_id}:{payload['artifact_type']}:{payload['version']}"
        self.store.insert_artifact({
            'artifact_id': artifact_id,
            'episode_id': episode_id,
            'artifact_type': payload['artifact_type'],
            'version': payload['version'],
            'lifecycle_status': 'DRAFT',
            'approval_status': 'PENDING_HUMAN_REVIEW',
            'lock_status': 'UNLOCKED',
            'payload': payload,
        })
        return {'artifact_id': artifact_id, 'artifact_type': payload['artifact_type'], 'version': payload['version']}

    def drive_mapping(self, episode_id: str) -> dict[str, Any]:
        return get_drive_mapping(episode_id)

    def validate(self, value: Any) -> dict[str, Any]:
        if not isinstance(value, dict) or "episode_id" not in value:
            raise StudioError("VALIDATION_TARGET_INVALID", "需提供含 episode_id 的 Object。")
        episode = self.store.get_episode(value["episode_id"])
        if "artifact_type" in value:
            validate_submission(value, episode)
        return {"ok": True, "result": "PASS"}
