"""Small, dependency-free validation helpers for P0 contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .errors import ContractViolation, StopAndReport


def load_json(path: str | Path) -> Any:
    source = Path(path)
    try:
        with source.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise StopAndReport(
            ContractViolation("INVALID_JSON", str(source), str(exc))
        ) from exc


def require_mapping(value: Any, path: str = "$") -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise StopAndReport(
            ContractViolation("TYPE_ERROR", path, "expected an object")
        )
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise StopAndReport(
            ContractViolation("TYPE_ERROR", path, "expected an array")
        )
    return value


def require_fields(
    record: Mapping[str, Any], fields: Iterable[str], path: str = "$"
) -> None:
    violations = [
        ContractViolation("MISSING_FIELD", f"{path}.{field}", "field is required")
        for field in fields
        if field not in record
    ]
    if violations:
        raise StopAndReport(*violations)


def require_nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StopAndReport(
            ContractViolation(
                "INVALID_STRING", path, "expected a non-empty string"
            )
        )
    return value


def require_enum(value: Any, allowed: Iterable[str], path: str) -> str:
    allowed_values = frozenset(allowed)
    if value not in allowed_values:
        raise StopAndReport(
            ContractViolation(
                "INVALID_ENUM",
                path,
                f"{value!r} is not one of {sorted(allowed_values)}",
            )
        )
    return value


def require_boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise StopAndReport(
            ContractViolation("TYPE_ERROR", path, "expected a boolean")
        )
    return value


def require_nonnegative_integer(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StopAndReport(
            ContractViolation(
                "INVALID_INTEGER", path, "expected a non-negative integer"
            )
        )
    return value
