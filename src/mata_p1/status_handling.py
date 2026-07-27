"""Validate Segment and Asset status controls."""
from typing import Any, Mapping
from mata_p0.asset_index import assert_asset_usage, assert_exact_asset_operation
from .constants import LIFECYCLE_STATUSES, QC_STATUSES
from .errors import stop
def validate_status(value: Mapping[str,Any]) -> Mapping[str,Any]:
    if value.get("lifecycle_status") not in LIFECYCLE_STATUSES: stop("INVALID_LIFECYCLE","$.lifecycle_status","invalid lifecycle")
    if value.get("qc_status") not in QC_STATUSES or value.get("qc_status") in LIFECYCLE_STATUSES: stop("QC_LIFECYCLE_MIXED","$.qc_status","QC and lifecycle must be separate")
    for role in value.get("usage_roles",[]): assert_asset_usage(value,role)
    assert_exact_asset_operation(value,proposed_drive_file_id=value.get("proposed_drive_file_id",""),generated_or_redrawn=value.get("generated_or_redrawn",False))
    return value
