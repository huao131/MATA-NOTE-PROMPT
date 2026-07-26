"""Validate auditable Production State update proposals."""
from typing import Any, Mapping
from mata_p0.dependency_recheck import assert_segment_ready_does_not_promote_episode
from mata_p0.evidence import assert_canonical_eligible
from mata_p0.schema_validation import require_fields, require_mapping
from .errors import stop
FIELDS=("scope_type","scope_id","version_refs","owner","timestamp","evidence_status","evidence_source","dependency_status","segment_status","episode_status","canonical_candidate","blocked_reason")
def validate_state_proposal(value: Mapping[str,Any]) -> Mapping[str,Any]:
    r=require_mapping(value); require_fields(r,FIELDS)
    assert_segment_ready_does_not_promote_episode(
        segment_status=r["segment_status"],
        current_episode_status=r.get("current_episode_status", "NOT_EVALUATED"),
        proposed_episode_status=r["episode_status"],
        promotion_basis=r.get("episode_ready_basis", ""),
    )
    if r["canonical_candidate"]:
        assert_canonical_eligible(r)
    if r["dependency_status"]!="PASS" and not r["blocked_reason"]:
        stop("BLOCKER_REQUIRED","$.blocked_reason","dependency blocker is required")
    return r
