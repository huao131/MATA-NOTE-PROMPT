"""Structured application errors."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from mata_p0.errors import StopAndReport


@dataclass(slots=True)
class StudioError(Exception):
    code: str
    message: str
    path: str = "$"
    status: int = 400

    def payload(self) -> dict[str, object]:
        return {"ok": False, "error": asdict(self)}


def normalize_error(error: Exception) -> StudioError:
    if isinstance(error, StudioError):
        return error
    if isinstance(error, StopAndReport):
        detail = "; ".join(
            f"{item.code}@{item.path}: {item.message}" for item in error.violations
        )
        return StudioError("STOP_AND_REPORT", detail, status=409)
    return StudioError("INTERNAL_ERROR", "未處理的系統錯誤。", status=500)
