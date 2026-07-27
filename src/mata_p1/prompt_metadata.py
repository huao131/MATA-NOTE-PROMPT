"""Validate traceable Prompt Library metadata without execution."""
from typing import Any, Mapping
from mata_p0.evidence import validate_evidence_record
from mata_p0.schema_validation import require_fields, require_mapping
from .errors import stop
FIELDS=("prompt_metadata_id","scope","approved_input_refs","evidence_status","evidence_source","version_refs","owner","timestamp","blocked_reason")
def validate_prompt_metadata(value: Mapping[str,Any]) -> Mapping[str,Any]:
    r=require_mapping(value); require_fields(r,FIELDS); validate_evidence_record(r)
    if not r["approved_input_refs"] or not r["version_refs"]: stop("TRACEABILITY_REQUIRED","$","approved inputs and versions required")
    if r["evidence_status"]!="VERIFIED": stop("NON_VERIFIED_PROMPT","$.evidence_status","VERIFIED required")
    forbidden={"flow_command","execute_flow","prompt_content"}
    if forbidden.intersection(r): stop("EXECUTION_FIELD_FORBIDDEN","$","metadata cannot control Flow or generate Prompt content")
    return r
