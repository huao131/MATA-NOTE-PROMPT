"""Validate the fixed six-Gate register."""
from typing import Any, Mapping, Sequence
from mata_p0.schema_validation import require_fields, require_mapping
from .constants import GATE_ORDER
from .errors import stop
FIELDS=("gate_id","gate_status","approved_version","approved_by","approved_at","basis_documents","evidence_status","dependency_recheck_result","blocked_reason")
def validate_gate_register(value: Sequence[Mapping[str,Any]]) -> Sequence[Mapping[str,Any]]:
    if len(value)!=6 or tuple(x.get("gate_id") for x in value)!=GATE_ORDER: stop("GATE_ORDER_INVALID","$.gates","exactly six ordered Gates required")
    for i,item in enumerate(value):
        if isinstance(item,bool): stop("GATE_RECORD_REQUIRED",f"$.gates[{i}]","boolean is forbidden")
        r=require_mapping(item,f"$.gates[{i}]"); require_fields(r,FIELDS,f"$.gates[{i}]")
        if r["gate_status"]=="PASS" and (r["approved_by"]=="CODEX" or not all((r["approved_version"],r["approved_by"],r["approved_at"],r["basis_documents"]))):
            stop("HUMAN_APPROVAL_REQUIRED",f"$.gates[{i}]","Codex cannot declare Gate PASS")
    return value
