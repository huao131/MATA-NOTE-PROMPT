"""Dependency Recheck queue and Gate blocking rules."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .constants import GATE_STATUSES, RECHECK_RESULTS
from .errors import ContractViolation, StopAndReport
from .schema_validation import (
    require_enum,
    require_fields,
    require_list,
    require_mapping,
    require_nonempty_string,
)

REQUIRED_RECHECK_FIELDS = (
    "affected_assets",
    "affected_segments",
    "affected_outputs",
    "recheck_owner",
    "recheck_result",
    "evidence_source",
)


def create_recheck_record(
    *,
    affected_assets: Iterable[str],
    affected_segments: Iterable[str],
    affected_outputs: Iterable[str],
    recheck_owner: str,
    evidence_source: Iterable[str],
) -> dict[str, Any]:
    record = {
        "dependency_status": "DEPENDENCY_RECHECK_REQUIRED",
        "affected_assets": list(affected_assets),
        "affected_segments": list(affected_segments),
        "affected_outputs": list(affected_outputs),
        "recheck_owner": recheck_owner,
        "recheck_result": "DEPENDENCY_RECHECK_REQUIRED",
        "evidence_source": list(evidence_source),
    }
    validate_recheck_record(record)
    return record


def validate_recheck_record(record: Mapping[str, Any]) -> None:
    item = require_mapping(record)
    require_fields(item, REQUIRED_RECHECK_FIELDS)
    for field in ("affected_assets", "affected_segments", "affected_outputs"):
        values = require_list(item[field], f"$.{field}")
        if not all(isinstance(value, str) and value.strip() for value in values):
            raise StopAndReport(
                ContractViolation(
                    "INVALID_AFFECTED_SCOPE",
                    f"$.{field}",
                    "affected IDs must be non-empty immutable identifiers",
                )
            )
    if not any(item[field] for field in ("affected_assets", "affected_segments", "affected_outputs")):
        raise StopAndReport(
            ContractViolation(
                "EMPTY_RECHECK_SCOPE",
                "$",
                "an upstream change must identify at least one affected downstream item",
            )
        )
    require_nonempty_string(item["recheck_owner"], "$.recheck_owner")
    require_enum(item["recheck_result"], RECHECK_RESULTS, "$.recheck_result")
    evidence = require_list(item["evidence_source"], "$.evidence_source")
    if not all(isinstance(value, str) and value.strip() for value in evidence):
        raise StopAndReport(
            ContractViolation(
                "INVALID_EVIDENCE_SOURCE",
                "$.evidence_source",
                "recheck evidence sources must be non-empty references",
            )
        )


def assert_gate_allowed(
    gate_status: str, recheck_record: Mapping[str, Any]
) -> None:
    require_enum(gate_status, GATE_STATUSES, "$.gate_status")
    validate_recheck_record(recheck_record)
    if gate_status == "PASS" and recheck_record["recheck_result"] != "PASS":
        raise StopAndReport(
            ContractViolation(
                "GATE_BLOCKED_BY_RECHECK",
                "$.gate_status",
                "affected Gate cannot PASS before Dependency Recheck PASS",
            )
        )


def assert_segment_ready_does_not_promote_episode(
    *,
    segment_status: str,
    current_episode_status: str,
    proposed_episode_status: str,
    promotion_basis: str,
) -> None:
    if (
        segment_status == "READY"
        and proposed_episode_status == "READY"
        and current_episode_status != "READY"
        and promotion_basis == "SEGMENT_READY"
    ):
        raise StopAndReport(
            ContractViolation(
                "SEGMENT_EPISODE_PROMOTION_FORBIDDEN",
                "$.episode_status",
                "Segment READY cannot promote Episode READY",
            )
        )
