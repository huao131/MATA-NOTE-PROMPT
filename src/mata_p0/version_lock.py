"""Version uniqueness and protected-artifact proposal checks."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping

from .constants import PROTECTED_DESIGNATIONS, PROTECTED_OPERATIONS
from .errors import ContractViolation, StopAndReport
from .schema_validation import require_fields, require_mapping, require_nonempty_string

_TOKEN_SPLIT = re.compile(r"[^A-Z0-9]+")


def protected_designations(path: str) -> frozenset[str]:
    tokens = frozenset(
        token
        for token in _TOKEN_SPLIT.split(PurePosixPath(path.replace("\\", "/")).name)
        if token
    )
    return frozenset(tokens & PROTECTED_DESIGNATIONS)


def assert_file_operation_allowed(
    operation: str, source_path: str, destination_path: str | None = None
) -> None:
    normalized_operation = operation.upper()
    if normalized_operation not in PROTECTED_OPERATIONS:
        raise StopAndReport(
            ContractViolation(
                "UNKNOWN_FILE_OPERATION",
                "$.operation",
                f"{operation!r} is not a governed protected-file operation",
            )
        )
    source_marks = protected_designations(source_path)
    if source_marks:
        raise StopAndReport(
            ContractViolation(
                "PROTECTED_ARTIFACT_MUTATION",
                source_path,
                f"{normalized_operation} forbidden for {sorted(source_marks)} artifact",
            )
        )
    if destination_path and protected_designations(destination_path):
        raise StopAndReport(
            ContractViolation(
                "PROTECTED_DESTINATION",
                destination_path,
                "operation cannot replace or impersonate a protected artifact",
            )
        )


def version_identity(record: Mapping[str, Any]) -> tuple[str, str, str]:
    item = require_mapping(record)
    require_fields(item, ("scope_id", "artifact_id", "version"))
    return tuple(
        require_nonempty_string(item[field], f"$.{field}")
        for field in ("scope_id", "artifact_id", "version")
    )


def assert_unique_versions(records: Iterable[Mapping[str, Any]]) -> None:
    seen: dict[tuple[str, str, str], int] = {}
    violations: list[ContractViolation] = []
    for index, record in enumerate(records):
        identity = version_identity(record)
        if identity in seen:
            violations.append(
                ContractViolation(
                    "DUPLICATE_VERSION",
                    f"$[{index}]",
                    f"{identity!r} duplicates record {seen[identity]}",
                )
            )
        else:
            seen[identity] = index
    if violations:
        raise StopAndReport(*violations)


def validate_supersession(
    old_record: Mapping[str, Any],
    superseding_record: Mapping[str, Any],
    *,
    old_artifact_mutated: bool = False,
) -> None:
    old_identity = version_identity(old_record)
    new_identity = version_identity(superseding_record)
    if old_identity[:2] != new_identity[:2]:
        raise StopAndReport(
            ContractViolation(
                "SUPERSESSION_IDENTITY_MISMATCH",
                "$.superseding_record",
                "scope and artifact identity must remain stable",
            )
        )
    if old_identity[2] == new_identity[2]:
        raise StopAndReport(
            ContractViolation(
                "DUPLICATE_VERSION",
                "$.superseding_record.version",
                "a superseding record must use a unique new version",
            )
        )
    if old_artifact_mutated:
        raise StopAndReport(
            ContractViolation(
                "PROTECTED_ARTIFACT_MUTATION",
                "$.old_record",
                "supersession is external; the prior artifact must remain unchanged",
            )
        )
