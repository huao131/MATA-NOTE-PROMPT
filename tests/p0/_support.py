from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mata_p0.folder_registry import CURRENT_EFFECTIVE_FOLDERS  # noqa: E402


def folder_records() -> list[dict]:
    return [
        {
            "stable_folder_code": code,
            **copy.deepcopy(identity),
            "folder_purpose": f"TEST purpose for {code}",
            "allowed_content": "TEST controlled content",
            "prohibited_content": "TEST prohibited content",
            "verification_status": "VERIFIED",
            "verified_at": "2026-07-26T12:36:35+08:00",
        }
        for code, identity in CURRENT_EFFECTIVE_FOLDERS.items()
    ]


def registry_by_code() -> dict[str, dict]:
    return {item["stable_folder_code"]: item for item in folder_records()}


def valid_asset(*, exact: bool = False) -> dict:
    folder = registry_by_code()["GLOBAL_OS"]
    asset = {
        "asset_id": "TEST_ASSET_001",
        "asset_type": "TEST_DOCUMENT",
        "scope_type": "ASSET",
        "scope_id": "TEST_SCOPE",
        "version": "V1.0",
        "folder_ref": {
            key: folder[key]
            for key in (
                "stable_folder_code",
                "display_name_zh_TW",
                "google_drive_folder_id",
                "parent_folder_id",
            )
        },
        "google_drive_file_id": "TEST_DRIVE_FILE_001",
        "checksum": "sha256:TEST_CHECKSUM",
        "mime_type": "application/json",
        "file_size_bytes": 128,
        "evidence_status": "VERIFIED",
        "lifecycle_status": "APPROVED",
        "qc_status": "QC_APPROVED",
        "approval_ref": "TEST_APPROVAL",
        "lock_ref": None,
        "source_asset_ids": [],
        "dependency_check_status": "PASS",
        "exact_asset": exact,
    }
    if exact:
        asset.update(
            {
                "exact_asset_id": "TEST_EXACT_001",
                "approved_original_drive_file_id": "TEST_DRIVE_FILE_001",
                "approved_version": "V1.0",
                "usage_locations": ["TEST_LOCATION"],
                "crop_or_scale_allowed": False,
            }
        )
    return asset
