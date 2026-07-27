"""Validate isolated new-Episode initialization plan candidates."""
from typing import Any, Mapping
from mata_p0.schema_validation import require_enum, require_fields, require_list, require_mapping, require_nonempty_string
from .errors import stop
REQUIRED_FIELDS = ("plan_id","scope_type","scope_id","episode_id","evidence_status","evidence_source","version_refs","owner","timestamp","operation")
def validate_episode_initialization_plan(value: Mapping[str, Any]) -> Mapping[str, Any]:
    record = require_mapping(value)
    require_fields(record, REQUIRED_FIELDS)
    require_nonempty_string(record["plan_id"], "$.plan_id")
    require_enum(record["scope_type"], {"TEST", "PLAN_CANDIDATE"}, "$.scope_type")
    scope_id = require_nonempty_string(record["scope_id"], "$.scope_id")
    episode_id = require_nonempty_string(record["episode_id"], "$.episode_id")
    require_enum(record["evidence_status"], {"VERIFIED"}, "$.evidence_status")
    if not require_list(record["evidence_source"], "$.evidence_source"):
        stop("MISSING_EVIDENCE", "$.evidence_source", "evidence is required")
    if not require_list(record["version_refs"], "$.version_refs"):
        stop("MISSING_VERSION_REFS", "$.version_refs", "version refs are required")
    require_nonempty_string(record["owner"], "$.owner")
    require_nonempty_string(record["timestamp"], "$.timestamp")
    require_enum(record["operation"], {"VALIDATE_PLAN"}, "$.operation")
    if record["scope_type"] == "TEST" and not scope_id.startswith("TEST_"):
        stop("TEST_SCOPE_REQUIRED", "$.scope_id", "TEST scope must start with TEST_")
    if episode_id.startswith(("EP", "episode")) and not episode_id.startswith("TEST_"):
        stop("FORMAL_EPISODE_WRITE_FORBIDDEN", "$.episode_id", "formal Episode writes are not authorized")
    return record
