"""Validate the fixed six-Gate register."""
from collections.abc import Mapping, Sequence
from typing import Any

from mata_p0.schema_validation import require_fields, require_mapping

from .constants import GATE_ORDER
from .errors import stop

FIELDS = (
    "gate_id",
    "gate_status",
    "approved_version",
    "approved_by",
    "approved_at",
    "basis_documents",
    "evidence_status",
    "dependency_recheck_result",
    "blocked_reason",
)


def validate_gate_register(
    value: Sequence[Mapping[str, Any]],
) -> Sequence[Mapping[str, Any]]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray, Mapping))
    ):
        stop("GATE_REGISTER_SEQUENCE_REQUIRED", "$.gates", "expected a Gate list")

    records: list[Mapping[str, Any]] = []
    for index, item in enumerate(value):
        path = f"$.gates[{index}]"
        if isinstance(item, bool) or not isinstance(item, Mapping):
            stop("GATE_RECORD_REQUIRED", path, "expected a Gate mapping record")
        record = require_mapping(item, path)
        require_fields(record, FIELDS, path)
        records.append(record)

    if len(records) != 6 or tuple(r["gate_id"] for r in records) != GATE_ORDER:
        stop(
            "GATE_ORDER_INVALID",
            "$.gates",
            "exactly six ordered Gates are required",
        )

    for index, record in enumerate(records):
        if record["gate_status"] != "PASS":
            continue
        path = f"$.gates[{index}]"
        if record["approved_by"] == "CODEX":
            stop("HUMAN_APPROVAL_REQUIRED", path, "Codex cannot declare Gate PASS")
        if not all(
            (
                record["approved_version"],
                record["approved_by"],
                record["approved_at"],
                record["basis_documents"],
            )
        ):
            stop("GATE_PASS_AUDIT_INCOMPLETE", path, "PASS audit fields are required")
        if record["evidence_status"] != "VERIFIED":
            stop("GATE_PASS_EVIDENCE_INVALID", path, "PASS requires VERIFIED evidence")
        if record["dependency_recheck_result"] != "PASS":
            stop("GATE_PASS_DEPENDENCY_INVALID", path, "PASS requires dependency PASS")
        if index > 0 and records[index - 1]["gate_status"] != "PASS":
            stop("GATE_PREDECESSOR_NOT_PASS", path, "previous Gate must PASS first")
    return value
