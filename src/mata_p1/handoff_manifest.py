"""Validate file-based Storyboard/Flow handoff manifests."""
from typing import Any, Mapping
from mata_p0.schema_validation import require_fields, require_mapping
from .errors import stop
FIELDS=("handoff_id","from","to","scope","input_refs","output_refs","owner","version_refs","evidence_status","dependency_status","gate_approval","timestamp","failure_action")
def validate_handoff_manifest(value: Mapping[str,Any]) -> Mapping[str,Any]:
    r=require_mapping(value); require_fields(r,FIELDS)
    if r["evidence_status"]!="VERIFIED" or r["dependency_status"]!="PASS" or not r["gate_approval"].get("approved_by") or r["gate_approval"].get("approved_by")=="CODEX": stop("HANDOFF_BLOCKED","$","verified evidence, dependency PASS and human Gate approval required")
    for ref in r["input_refs"]:
        if ref.get("lifecycle_status")=="REJECTED": stop("REJECTED_HANDOFF","$.input_refs","Rejected input forbidden")
        if ref.get("exact_asset") and (ref.get("generated_or_redrawn") or ref.get("file_id")!=ref.get("approved_original_file_id")): stop("EXACT_ASSET_HANDOFF","$.input_refs","controlled original required")
    if any(k in r for k in ("execute_flow","capcut_operation","generate_media")): stop("EXTERNAL_EXECUTION_FORBIDDEN","$","handoff is file-only")
    return r
