"""Structured P0 contract failures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ContractViolation:
    code: str
    path: str
    message: str


class StopAndReport(ValueError):
    """Raised when governance requires the caller to stop without mutation."""

    def __init__(self, *violations: ContractViolation):
        self.violations = tuple(violations)
        detail = "; ".join(
            f"{item.code}@{item.path}: {item.message}" for item in self.violations
        )
        super().__init__(detail or "STOP_AND_REPORT")
