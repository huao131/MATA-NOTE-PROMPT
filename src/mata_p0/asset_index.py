"""Asset Index read/write contract validation from S02."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .constants import (
    ASSET_USAGE_ROLES,
    DEPENDENCY_STATUSES,
    EVIDENCE_STATUSES,
    LIFECYCLE_STATUSES,
)
from .errors import ContractViolation, StopAndReport
from .schema_validation import (
    load_json,
    require_boolean,
    require_enum,
    require_fields,
    require_list,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_integer,
)

REQUIRED_ASSET_FIELDS = (
    "asset_id",
    "asset_type",
    "scope_type",
    "scope_id",
    "version",
    "folder_ref",
    "google_drive_file_id",
    "checksum",
    "mime_type",
    "file_size_bytes",
    "evidence_status",
    "lifecycle_status",
    "qc_status",
    "approval_ref",
    "lock_ref",
    "source_asset_ids",
    "dependency_check_status",
    "exact_asset",
)
REQUIRED_FOLDER_REF_FIELDS = (
    "stable_folder_code",
    "display_name_zh_TW",
    "google_drive_folder_id",
    "parent_folder_id",
)
REQUIRED_EXACT_ASSET_FIELDS = (
    "exact_asset_id",
    "approved_original_drive_file_id",
    "approved_version",
    "usage_locations",
    "crop_or_scale_allowed",
)


def _asset_records(document: Any) -> list[Mapping[str, Any]]:
    if isinstance(document, list):
        records = document
    else:
        root = require_mapping(document)
        require_fields(root, ("assets",))
        records = require_list(root["assets"], "$.assets")
    return [require_mapping(item, f"$.assets[{index}]") for index, item in enumerate(records)]


def read_asset_index(
    path: str, folder_registry: Mapping[str, Mapping[str, Any]]
) -> list[Mapping[str, Any]]:
    records = _asset_records(load_json(path))
    validate_asset_index(records, folder_registry)
    return records


def validate_asset_record(
    record: Mapping[str, Any],
    folder_registry: Mapping[str, Mapping[str, Any]],
    *,
    canonical_candidate: bool = False,
    path: str = "$",
) -> None:
    item = require_mapping(record, path)
    require_fields(item, REQUIRED_ASSET_FIELDS, path)
    for field in (
        "asset_id",
        "asset_type",
        "scope_type",
        "scope_id",
        "version",
        "google_drive_file_id",
        "checksum",
        "mime_type",
        "qc_status",
    ):
        require_nonempty_string(item[field], f"{path}.{field}")
    require_nonnegative_integer(item["file_size_bytes"], f"{path}.file_size_bytes")
    require_enum(item["evidence_status"], EVIDENCE_STATUSES, f"{path}.evidence_status")
    require_enum(
        item["lifecycle_status"], LIFECYCLE_STATUSES, f"{path}.lifecycle_status"
    )
    require_enum(
        item["dependency_check_status"],
        DEPENDENCY_STATUSES,
        f"{path}.dependency_check_status",
    )
    if item["qc_status"] in LIFECYCLE_STATUSES:
        raise StopAndReport(
            ContractViolation(
                "QC_LIFECYCLE_MIXED",
                f"{path}.qc_status",
                "qc_status and lifecycle_status are separate domains",
            )
        )
    for optional_ref in ("approval_ref", "lock_ref"):
        value = item[optional_ref]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise StopAndReport(
                ContractViolation(
                    "INVALID_GOVERNANCE_REF",
                    f"{path}.{optional_ref}",
                    "expected null or a non-empty reference",
                )
            )
    source_ids = require_list(item["source_asset_ids"], f"{path}.source_asset_ids")
    if not all(isinstance(value, str) and value.strip() for value in source_ids):
        raise StopAndReport(
            ContractViolation(
                "INVALID_SOURCE_ASSET_IDS",
                f"{path}.source_asset_ids",
                "source asset IDs must be non-empty immutable IDs",
            )
        )

    folder_ref = require_mapping(item["folder_ref"], f"{path}.folder_ref")
    require_fields(folder_ref, REQUIRED_FOLDER_REF_FIELDS, f"{path}.folder_ref")
    code = folder_ref["stable_folder_code"]
    expected_folder = folder_registry.get(code)
    if expected_folder is None:
        raise StopAndReport(
            ContractViolation(
                "UNKNOWN_FOLDER_REF",
                f"{path}.folder_ref.stable_folder_code",
                f"{code!r} is not registered",
            )
        )
    for field in REQUIRED_FOLDER_REF_FIELDS:
        if folder_ref[field] != expected_folder[field]:
            raise StopAndReport(
                ContractViolation(
                    "FOLDER_REF_MISMATCH",
                    f"{path}.folder_ref.{field}",
                    "folder reference must exactly match the Registry record",
                )
            )

    exact_asset = require_boolean(item["exact_asset"], f"{path}.exact_asset")
    if exact_asset:
        require_fields(item, REQUIRED_EXACT_ASSET_FIELDS, path)
        for field in (
            "exact_asset_id",
            "approved_original_drive_file_id",
            "approved_version",
        ):
            require_nonempty_string(item[field], f"{path}.{field}")
        usage_locations = require_list(
            item["usage_locations"], f"{path}.usage_locations"
        )
        if not all(
            isinstance(location, str) and location.strip()
            for location in usage_locations
        ):
            raise StopAndReport(
                ContractViolation(
                    "INVALID_USAGE_LOCATIONS",
                    f"{path}.usage_locations",
                    "usage locations must be non-empty strings",
                )
            )
        require_boolean(
            item["crop_or_scale_allowed"], f"{path}.crop_or_scale_allowed"
        )
        if item["google_drive_file_id"] != item["approved_original_drive_file_id"]:
            raise StopAndReport(
                ContractViolation(
                    "EXACT_ASSET_FILE_MISMATCH",
                    f"{path}.approved_original_drive_file_id",
                    "Exact Asset must use the approved original Drive File ID",
                )
            )

    if canonical_candidate:
        if item["evidence_status"] != "VERIFIED":
            raise StopAndReport(
                ContractViolation(
                    "NON_VERIFIED_CANONICAL_WRITE",
                    f"{path}.evidence_status",
                    "only VERIFIED evidence can support Canonical State",
                )
            )
        if item["dependency_check_status"] != "PASS":
            raise StopAndReport(
                ContractViolation(
                    "DEPENDENCY_NOT_PASS",
                    f"{path}.dependency_check_status",
                    "Canonical candidate requires dependency PASS",
                )
            )
        if item["lifecycle_status"] == "REJECTED":
            raise StopAndReport(
                ContractViolation(
                    "REJECTED_CANONICAL_WRITE",
                    f"{path}.lifecycle_status",
                    "REJECTED assets cannot enter Canonical State",
                )
            )


def validate_asset_index(
    records: Iterable[Mapping[str, Any]],
    folder_registry: Mapping[str, Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    by_id: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(records):
        path = f"$.assets[{index}]"
        validate_asset_record(item, folder_registry, path=path)
        asset_id = item["asset_id"]
        if asset_id in by_id:
            raise StopAndReport(
                ContractViolation(
                    "DUPLICATE_ASSET_ID",
                    f"{path}.asset_id",
                    f"{asset_id!r} is already registered",
                )
            )
        by_id[asset_id] = item
    return by_id


def assert_asset_usage(record: Mapping[str, Any], role: str) -> None:
    require_enum(role, ASSET_USAGE_ROLES, "$.role")
    if record.get("lifecycle_status") == "REJECTED":
        raise StopAndReport(
            ContractViolation(
                "REJECTED_ASSET_USAGE",
                "$.lifecycle_status",
                f"REJECTED asset cannot be used as {role}",
            )
        )


def assert_exact_asset_operation(
    record: Mapping[str, Any],
    *,
    proposed_drive_file_id: str,
    generated_or_redrawn: bool,
) -> None:
    if not record.get("exact_asset"):
        return
    if generated_or_redrawn:
        raise StopAndReport(
            ContractViolation(
                "EXACT_ASSET_GENERATION_FORBIDDEN",
                "$.exact_asset",
                "Exact Asset cannot be generated, redrawn, imitated, or replaced",
            )
        )
    if proposed_drive_file_id != record.get("approved_original_drive_file_id"):
        raise StopAndReport(
            ContractViolation(
                "EXACT_ASSET_REPLACEMENT_FORBIDDEN",
                "$.approved_original_drive_file_id",
                "Exact Asset must retain the approved original Drive File ID",
            )
        )
