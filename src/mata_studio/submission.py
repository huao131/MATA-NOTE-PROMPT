"""Governed ChatGPT artifact submission boundary."""

from __future__ import annotations

import json
import re
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from mata_p0.version_lock import protected_designations

from .constants import APPROVAL, ARTIFACT_TYPES, LIFECYCLE, LOCK, PRODUCTION
from .errors import StudioError
from .store import ProjectStore

SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "local_studio"


def _load_schema(name: str) -> dict[str, Any]:
    schema_path = SCHEMA_ROOT / name
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _validate_schema(value: Any, schema: Mapping[str, Any]) -> None:
    if not isinstance(value, Mapping):
        raise StudioError("SCHEMA_VALIDATION_FAILED", "Payload 必須是 Object。")
    if schema.get("type") == "object":
        required = schema.get("required", [])
        missing = [field for field in required if field not in value]
        if missing:
            raise StudioError("SCHEMA_VALIDATION_FAILED", f"缺少欄位：{missing}")
        for field_name, field_schema in schema.get("properties", {}).items():
            if field_name in value:
                if field_schema.get("type") == "object":
                    if not isinstance(value[field_name], Mapping):
                        raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 必須是 Object。")
                elif field_schema.get("type") == "array":
                    if not isinstance(value[field_name], list):
                        raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 必須是 Array。")
                elif field_schema.get("type") == "string":
                    if not isinstance(value[field_name], str):
                        raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 必須是字串。")
                enum = field_schema.get("enum")
                if enum and value[field_name] not in enum:
                    raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 值不合法。")
                const = field_schema.get("const")
                if const and value[field_name] != const:
                    raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 值不合法。")
                pattern = field_schema.get("pattern")
                if pattern and isinstance(value[field_name], str):
                    if not re.fullmatch(pattern, value[field_name]):
                        raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 格式不合法。")
                if field_name == "artifact_type" and value[field_name] not in ARTIFACT_TYPES:
                    raise StudioError("SCHEMA_VALIDATION_FAILED", "artifact_type 不在核准清單。")
    return None

VERSION = re.compile(r"^V[0-9]+\.[0-9]+$")
FORBIDDEN_APPROVERS = {"CODEX", "CHATGPT", "SYSTEM", "AI"}


def validate_submission(value: Any, episode: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise StudioError("INVALID_SUBMISSION", "Submission 必須是 JSON Object。")
    item = dict(value)
    required = (
        "episode_id", "series_id", "artifact_type", "version", "lifecycle_status",
        "approval_status", "lock_status", "production_state", "payload",
    )
    missing = [field for field in required if field not in item]
    if missing:
        raise StudioError("MISSING_SUBMISSION_FIELDS", f"缺少欄位：{missing}")
    if item["episode_id"] != episode["episode_id"] or item["series_id"] != episode["series_id"]:
        raise StudioError("IDENTITY_MISMATCH", "Episode 或 Series 身分不一致。", status=409)
    _validate_schema(item, _load_schema("artifact_submission.schema.json"))
    if item["artifact_type"] not in ARTIFACT_TYPES:
        raise StudioError("INVALID_ARTIFACT_TYPE", "artifact_type 不在核准清單。")
    if not isinstance(item["version"], str) or not VERSION.fullmatch(item["version"]):
        raise StudioError("INVALID_VERSION", "version 必須使用 Vn.n 格式。")
    if item["lifecycle_status"] not in LIFECYCLE:
        raise StudioError("INVALID_LIFECYCLE", "lifecycle_status 不合法。")
    if item["approval_status"] not in APPROVAL:
        raise StudioError("INVALID_APPROVAL", "approval_status 不合法。")
    if item["lock_status"] not in LOCK:
        raise StudioError("INVALID_LOCK", "lock_status 不合法。")
    if item["production_state"] not in PRODUCTION:
        raise StudioError("INVALID_PRODUCTION_STATE", "production_state 不合法。")
    if item["lifecycle_status"] in {"LOCKED", "APPROVED"} or item["lock_status"] == "LOCKED":
        raise StudioError("HUMAN_APPROVAL_REQUIRED", "Payload 不得建立 Approved／Locked。", status=409)
    if item["approval_status"] == "APPROVED":
        raise StudioError("APPROVAL_PAYLOAD_FORBIDDEN", "批准必須透過獨立 Gate Event。", status=409)
    if "approved_by" in item or "approver" in item:
        raise StudioError("APPROVER_IN_PAYLOAD", "Artifact Payload 不得指定批准人。", status=409)
    if not isinstance(item["payload"], Mapping):
        raise StudioError("INVALID_ARTIFACT_PAYLOAD", "payload 必須是 JSON Object。")
    sources = item.get("source_asset_ids", [])
    if not isinstance(sources, list) or not all(isinstance(source, str) and source for source in sources):
        raise StudioError("INVALID_SOURCE_ASSETS", "source_asset_ids 必須是 ID 清單。")
    if protected_designations(str(item.get("filename", ""))):
        raise StudioError("PROTECTED_NAME_FORBIDDEN", "Candidate 不得冒充 Protected Artifact。", status=409)
    if item.get("change_class") == "MAJOR" and item.get("dependency_recheck_status") != "DEPENDENCY_RECHECK_REQUIRED":
        raise StudioError(
            "DEPENDENCY_RECHECK_REQUIRED",
            "MAJOR 變更必須先標記 Dependency Recheck，受影響下游不得 PASS。",
            status=409,
        )
    return item


class SubmissionService:
    def __init__(self, store: ProjectStore):
        self.store = store

    def submit(self, episode_id: str, value: Any) -> dict[str, Any]:
        episode = self.store.get_episode(episode_id)
        item = validate_submission(value, episode)
        rejected = {asset["asset_id"] for asset in self.store.assets(episode_id) if asset["rejected"]}
        if rejected.intersection(item.get("source_asset_ids", [])):
            raise StudioError("REJECTED_ASSET_DEPENDENCY", "Rejected Asset 不得作下游輸入。", status=409)
        item["artifact_id"] = item.get("artifact_id") or f"ART-{uuid.uuid4().hex[:16].upper()}"
        return self.store.insert_artifact(item)
