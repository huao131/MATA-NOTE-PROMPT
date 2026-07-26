"""Evidence and Canonical Production State eligibility checks."""

from __future__ import annotations

from typing import Any, Mapping

from .constants import DEPENDENCY_STATUSES, EVIDENCE_STATUSES
from .errors import ContractViolation, StopAndReport
from .schema_validation import require_enum, require_fields, require_mapping


def validate_evidence_record(record: Mapping[str, Any]) -> None:
    item = require_mapping(record)
    require_fields(item, ("evidence_status", "evidence_source"))
    require_enum(item["evidence_status"], EVIDENCE_STATUSES, "$.evidence_status")
    sources = item["evidence_source"]
    if not isinstance(sources, list) or not all(
        isinstance(source, str) and source.strip() for source in sources
    ):
        raise StopAndReport(
            ContractViolation(
                "INVALID_EVIDENCE_SOURCE",
                "$.evidence_source",
                "expected a non-empty array of resolvable source references",
            )
        )


def assert_canonical_eligible(record: Mapping[str, Any]) -> None:
    validate_evidence_record(record)
    if record["evidence_status"] != "VERIFIED":
        raise StopAndReport(
            ContractViolation(
                "NON_VERIFIED_CANONICAL_WRITE",
                "$.evidence_status",
                "only VERIFIED evidence can support Canonical Production State",
            )
        )
    dependency = record.get("dependency_status")
    if dependency is not None:
        require_enum(dependency, DEPENDENCY_STATUSES, "$.dependency_status")
        if dependency != "PASS":
            raise StopAndReport(
                ContractViolation(
                    "DEPENDENCY_NOT_PASS",
                    "$.dependency_status",
                    "Canonical eligibility requires dependency PASS",
                )
            )
