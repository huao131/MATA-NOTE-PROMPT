"""Repository boundary checks that do not mutate the repository."""

from __future__ import annotations

import ntpath
from pathlib import PurePosixPath
from typing import Iterable

from .constants import MEDIA_EXTENSIONS
from .errors import ContractViolation, StopAndReport
from .version_lock import protected_designations

ALLOWED_P0_PREFIXES = (
    "src/mata_p0/",
    "schemas/p0/",
    "tests/p0/",
    "docs/work/v2_reports/",
)


def normalize_repo_path(path: str) -> str:
    if not path:
        raise StopAndReport(
            ContractViolation(
                "PATH_OUTSIDE_REPOSITORY",
                path,
                "expected a non-empty repository-relative path",
            )
        )

    slash_path = path.replace("\\", "/")
    drive, _ = ntpath.splitdrive(path)
    raw_parts = slash_path.split("/")
    if (
        drive
        or slash_path.startswith("/")
        or any(part == ".." for part in raw_parts)
    ):
        raise StopAndReport(
            ContractViolation(
                "PATH_OUTSIDE_REPOSITORY",
                path,
                "expected a repository-relative path",
            )
        )

    normalized = str(PurePosixPath(slash_path))
    if normalized == ".":
        raise StopAndReport(
            ContractViolation(
                "PATH_OUTSIDE_REPOSITORY",
                path,
                "expected a non-empty repository-relative path",
            )
        )
    return normalized


def assert_p0_write_path(path: str) -> str:
    normalized = normalize_repo_path(path)
    lowered_parts = {part.lower() for part in PurePosixPath(normalized).parts}
    is_test_fixture = normalized.startswith("tests/p0/fixtures/TEST_")
    if "legacy" in lowered_parts:
        raise StopAndReport(
            ContractViolation(
                "LEGACY_WRITE_FORBIDDEN", normalized, "Legacy is read-only"
            )
        )
    if PurePosixPath(normalized).suffix.lower() in MEDIA_EXTENSIONS:
        raise StopAndReport(
            ContractViolation(
                "MEDIA_WRITE_FORBIDDEN",
                normalized,
                "P0 cannot modify image, video, or audio assets",
            )
        )
    if protected_designations(normalized) and not is_test_fixture:
        raise StopAndReport(
            ContractViolation(
                "PROTECTED_ARTIFACT_MUTATION",
                normalized,
                "LOCK/FINAL/MASTER/APPROVED artifacts are immutable",
            )
        )
    if not normalized.startswith(ALLOWED_P0_PREFIXES):
        raise StopAndReport(
            ContractViolation(
                "P0_SCOPE_VIOLATION",
                normalized,
                "path is outside the approved P0 implementation surface",
            )
        )
    return normalized


def assert_changed_paths_are_p0_only(paths: Iterable[str]) -> None:
    violations: list[ContractViolation] = []
    for path in paths:
        try:
            assert_p0_write_path(path)
        except StopAndReport as exc:
            violations.extend(exc.violations)
    if violations:
        raise StopAndReport(*violations)
