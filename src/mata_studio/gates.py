"""Human-only Gate operations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .constants import GATES
from .errors import StudioError
from .store import ProjectStore
from .submission import FORBIDDEN_APPROVERS


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
