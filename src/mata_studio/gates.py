"""Human-only Gate operations."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import GATES
from .errors import StudioError
from .store import ProjectStore
from .submission import FORBIDDEN_APPROVERS

SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schemas" / "local_studio"


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _validate_gate_event_schema(value: Any) -> None:
    if not isinstance(value, dict):
        raise StudioError("SCHEMA_VALIDATION_FAILED", "Approval Event 必須是 Object。")
    schema = _load_schema("approval_event.schema.json")
    required = schema.get("required", [])
    missing = [field for field in required if field not in value]
    if missing:
        raise StudioError("SCHEMA_VALIDATION_FAILED", f"缺少欄位：{missing}")
    for field_name, field_schema in schema.get("properties", {}).items():
        if field_name in value:
            if field_schema.get("type") == "string" and not isinstance(value[field_name], str):
                raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 必須是字串。")
            not_schema = field_schema.get("not")
            if not_schema:
                forbidden = not_schema.get("enum")
                if forbidden and value[field_name] in forbidden:
                    raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 不合法。")
            pattern = field_schema.get("pattern")
            if pattern and not __import__("re").fullmatch(pattern, value[field_name]):
                raise StudioError("SCHEMA_VALIDATION_FAILED", f"欄位 {field_name} 格式不合法。")


class GateService:
    def __init__(self, store: ProjectStore):
        self.store = store

    def submit(self, episode_id: str, gate_id: str, artifact_version: str) -> dict[str, Any]:
        self._gate(gate_id)
        if not any(item["version"] == artifact_version for item in self.store.artifacts(episode_id)):
            raise StudioError("ARTIFACT_VERSION_NOT_FOUND", "找不到 Artifact 版本。", status=404)
        self.store.submit_gate(episode_id, gate_id, artifact_version)
        return {"gate_id": gate_id, "gate_status": "SUBMITTED"}

    def decide(self, episode_id: str, gate_id: str, decision: str, event: Any) -> dict[str, Any]:
        self._gate(gate_id)
        if decision not in {"PASS", "REJECTED"}:
            raise StudioError("INVALID_GATE_DECISION", "Gate 只能 PASS 或 REJECTED。")
        if not isinstance(event, dict):
            raise StudioError("INVALID_APPROVAL_EVENT", "Approval Event 必須是 Object。")
        _validate_gate_event_schema(event)
        required = ("approver", "artifact_version", "evidence", "comment")
        missing = [field for field in required if not isinstance(event.get(field), str) or not event[field].strip()]
        if missing:
            raise StudioError("MISSING_APPROVAL_EVENT_FIELDS", f"缺少欄位：{missing}")
        if event["approver"].strip().upper() in FORBIDDEN_APPROVERS:
            raise StudioError("NON_HUMAN_APPROVER", "Codex／ChatGPT／System 不得批准 Gate。", status=403)
        gates = self.store.gates(episode_id)
        index = GATES.index(gate_id)
        current = next(item for item in gates if item["gate_id"] == gate_id)
        if current["gate_status"] != "SUBMITTED":
            raise StudioError("GATE_NOT_SUBMITTED", "Gate 尚未提交人工審閱。", status=409)
        if decision == "PASS" and index and gates[index - 1]["gate_status"] != "PASS":
            raise StudioError("PREDECESSOR_GATE_NOT_PASS", "前一 Gate 尚未通過。", status=409)
        event = dict(event)
        event["approved_at"] = datetime.now(timezone.utc).isoformat()
        self.store.decide_gate(episode_id, gate_id, decision, event)
        return {"gate_id": gate_id, "gate_status": decision, "event": event}

    @staticmethod
    def _gate(gate_id: str) -> None:
        if gate_id not in GATES:
            raise StudioError("INVALID_GATE", "未知 Gate ID。")
