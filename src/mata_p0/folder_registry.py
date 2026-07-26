"""Folder Registry reader and S01 contract validation."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .errors import ContractViolation, StopAndReport
from .schema_validation import (
    load_json,
    require_fields,
    require_list,
    require_mapping,
    require_nonempty_string,
)

REQUIRED_FOLDER_FIELDS = (
    "stable_folder_code",
    "display_name_zh_TW",
    "google_drive_folder_id",
    "parent_folder_id",
    "folder_purpose",
    "allowed_content",
    "prohibited_content",
    "verification_status",
    "verified_at",
)

CURRENT_EFFECTIVE_FOLDERS = {
    "MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2": {
        "display_name_zh_TW": "MATA AI 原創影片製片系統 V2",
        "google_drive_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
        "parent_folder_id": "ROOT_PARENT_NOT_IN_V2_SCOPE",
    },
    "GLOBAL_OS": {
        "display_name_zh_TW": "01_全域系統規範",
        "google_drive_folder_id": "1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5",
        "parent_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
    },
    "ORIGINAL_VIDEO_LIBRARY": {
        "display_name_zh_TW": "02_原創影片資料庫",
        "google_drive_folder_id": "14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC",
        "parent_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
    },
    "SHARED_ASSET_LIBRARY": {
        "display_name_zh_TW": "03_共用素材資料庫",
        "google_drive_folder_id": "1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV",
        "parent_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
    },
    "PRODUCTION_DATABASE": {
        "display_name_zh_TW": "04_製片控制與索引",
        "google_drive_folder_id": "1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG",
        "parent_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
    },
    "ARCHIVE": {
        "display_name_zh_TW": "05_封存資料庫",
        "google_drive_folder_id": "1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz",
        "parent_folder_id": "18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT",
    },
    "LEGACY_SYSTEM_AUDIT": {
        "display_name_zh_TW": "01_舊系統稽核",
        "google_drive_folder_id": "1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6",
        "parent_folder_id": "1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz",
    },
}


def _records_from_document(document: Any) -> list[Mapping[str, Any]]:
    if isinstance(document, list):
        records = document
    else:
        root = require_mapping(document)
        require_fields(root, ("folders",))
        records = require_list(root["folders"], "$.folders")
    return [require_mapping(item, f"$.folders[{index}]") for index, item in enumerate(records)]


def read_folder_registry(path: str) -> list[Mapping[str, Any]]:
    records = _records_from_document(load_json(path))
    validate_folder_registry(records)
    return records


def validate_folder_registry(
    records: Iterable[Mapping[str, Any]],
    *,
    enforce_current_effective: bool = True,
) -> dict[str, Mapping[str, Any]]:
    items = list(records)
    by_code: dict[str, Mapping[str, Any]] = {}
    by_drive_id: dict[str, str] = {}
    violations: list[ContractViolation] = []

    for index, raw in enumerate(items):
        path = f"$.folders[{index}]"
        item = require_mapping(raw, path)
        require_fields(item, REQUIRED_FOLDER_FIELDS, path)
        for field in REQUIRED_FOLDER_FIELDS:
            require_nonempty_string(item[field], f"{path}.{field}")
        code = item["stable_folder_code"]
        drive_id = item["google_drive_folder_id"]
        if code in by_code:
            violations.append(
                ContractViolation(
                    "DUPLICATE_STABLE_CODE",
                    f"{path}.stable_folder_code",
                    f"{code!r} is already registered",
                )
            )
        if drive_id in by_drive_id:
            violations.append(
                ContractViolation(
                    "DUPLICATE_DRIVE_ID",
                    f"{path}.google_drive_folder_id",
                    f"Drive ID is already used by {by_drive_id[drive_id]}",
                )
            )
        if item["verification_status"] != "VERIFIED":
            violations.append(
                ContractViolation(
                    "FOLDER_NOT_VERIFIED",
                    f"{path}.verification_status",
                    "Current Effective Folder Registry entries must be VERIFIED",
                )
            )
        by_code[code] = item
        by_drive_id[drive_id] = code

    if enforce_current_effective:
        expected_codes = set(CURRENT_EFFECTIVE_FOLDERS)
        actual_codes = set(by_code)
        for code in sorted(expected_codes - actual_codes):
            violations.append(
                ContractViolation(
                    "MISSING_FOLDER", "$.folders", f"missing stable code {code}"
                )
            )
        for code in sorted(actual_codes - expected_codes):
            violations.append(
                ContractViolation(
                    "UNREGISTERED_FOLDER",
                    "$.folders",
                    f"unexpected stable code {code}",
                )
            )
        for code in sorted(expected_codes & actual_codes):
            for field, expected in CURRENT_EFFECTIVE_FOLDERS[code].items():
                if by_code[code][field] != expected:
                    violations.append(
                        ContractViolation(
                            "FOLDER_CONTRACT_MISMATCH",
                            f"$.folders[{code}].{field}",
                            f"expected {expected!r}, got {by_code[code][field]!r}",
                        )
                    )

    if violations:
        raise StopAndReport(*violations)
    return by_code


def resolve_folder(
    registry: Mapping[str, Mapping[str, Any]],
    *,
    stable_folder_code: str | None = None,
    google_drive_folder_id: str | None = None,
) -> Mapping[str, Any]:
    if not stable_folder_code and not google_drive_folder_id:
        raise StopAndReport(
            ContractViolation(
                "MISSING_FOLDER_IDENTITY",
                "$",
                "stable_folder_code or google_drive_folder_id is required",
            )
        )
    matches = [
        record
        for code, record in registry.items()
        if (stable_folder_code is None or code == stable_folder_code)
        and (
            google_drive_folder_id is None
            or record["google_drive_folder_id"] == google_drive_folder_id
        )
    ]
    if len(matches) != 1:
        raise StopAndReport(
            ContractViolation(
                "FOLDER_RESOLUTION_FAILED",
                "$",
                "folder identity did not resolve to exactly one Registry record",
            )
        )
    return matches[0]
