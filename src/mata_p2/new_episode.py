"""P2-WF-01 New Episode Workflow MVP.

The workflow creates local candidate JSON only. It never calls external
services and never declares a human Gate approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import uuid
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePath
from typing import Any

from mata_p0.constants import GATE_IDS
from mata_p0.errors import ContractViolation, StopAndReport
from mata_p0.schema_validation import require_fields, require_mapping
from mata_p0.version_lock import protected_designations
from mata_p1.episode_initialization import validate_episode_initialization_plan
from mata_p1.gate_register import validate_gate_register
from mata_p1.production_state import validate_state_proposal
from mata_p1.prompt_metadata import validate_prompt_metadata
from mata_p1.status_handling import validate_status

WORK_ITEM_ID = "P2-WF-01"
TECHNICAL_ID = "p2_wf_01"
BRIEF_FIELDS = (
    "episode_id",
    "title",
    "purpose",
    "target_audience",
    "duration_seconds",
    "platform",
    "aspect_ratio",
    "desired_action",
    "series_name",
    "existing_character_usage",
    "special_requirements",
)
ASPECT_RATIOS = frozenset({"9:16", "16:9", "1:1", "4:5"})
EPISODE_ID = re.compile(r"^(?:TEST_[A-Z0-9_]+|EP[0-9]{3,})$")
FORBIDDEN_INPUT_FIELDS = frozenset(
    {
        "approved_by",
        "approval_type",
        "status",
        "gate_status",
        "drive_operation",
        "flow_operation",
        "capcut_operation",
        "media_generation",
        "external_api",
    }
)
FORBIDDEN_OUTPUT_COMPONENTS = frozenset(
    {"episodes", "system", "templates", "legacy"}
)
OUTPUT_FILES = (
    "01_episode_initialization_plan.json",
    "02_audience_insight.json",
    "03_hook_strategy_candidates.json",
    "04_creative_candidate.json",
    "05_story_treatment_candidate.json",
    "06_production_state_candidate.json",
    "07_gate_register_candidate.json",
    "08_segment_asset_status_candidate.json",
    "09_prompt_metadata_placeholder.json",
    "10_storyboard_flow_handoff_placeholder.json",
    "11_execution_manifest.json",
    "12_validation_report.json",
)


def stop(code: str, path: str, message: str) -> None:
    raise StopAndReport(ContractViolation(code, path, message))


def _nonempty_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        stop("INVALID_BRIEF_FIELD", path, "expected a non-empty string")
    return value.strip()


def validate_brief(value: Mapping[str, Any]) -> dict[str, Any]:
    brief = dict(require_mapping(value, "$"))
    require_fields(brief, BRIEF_FIELDS)
    extras = sorted(set(brief) - set(BRIEF_FIELDS))
    if extras:
        if FORBIDDEN_INPUT_FIELDS.intersection(extras):
            stop(
                "FORBIDDEN_OPERATION_REQUEST",
                "$",
                f"external, approval, or status controls are forbidden: {extras}",
            )
        stop("BRIEF_SCHEMA_INVALID", "$", f"unexpected fields: {extras}")

    for field in (
        "episode_id",
        "title",
        "purpose",
        "target_audience",
        "platform",
        "aspect_ratio",
        "desired_action",
        "series_name",
        "existing_character_usage",
    ):
        brief[field] = _nonempty_string(brief[field], f"$.{field}")

    if not EPISODE_ID.fullmatch(brief["episode_id"]):
        stop(
            "INVALID_EPISODE_ID",
            "$.episode_id",
            "use TEST_... or an EP identifier with at least three digits",
        )
    duration = brief["duration_seconds"]
    if isinstance(duration, bool) or not isinstance(duration, int) or not 1 <= duration <= 3600:
        stop(
            "INVALID_DURATION",
            "$.duration_seconds",
            "duration must be an integer from 1 to 3600",
        )
    if brief["aspect_ratio"] not in ASPECT_RATIOS:
        stop(
            "INVALID_ASPECT_RATIO",
            "$.aspect_ratio",
            f"allowed values: {sorted(ASPECT_RATIOS)}",
        )
    requirements = brief["special_requirements"]
    if not isinstance(requirements, list) or not all(
        isinstance(item, str) and item.strip() for item in requirements
    ):
        stop(
            "INVALID_SPECIAL_REQUIREMENTS",
            "$.special_requirements",
            "expected an array of non-empty strings",
        )
    return brief


def _safe_output_path(output: str | Path) -> Path:
    raw = str(output)
    if not raw.strip():
        stop("OUTPUT_PATH_REQUIRED", "$.output", "output directory is required")
    normalized = raw.replace("\\", "/")
    if any(part == ".." for part in normalized.split("/")):
        stop("PATH_TRAVERSAL", "$.output", "parent traversal is forbidden")
    target = Path(raw)
    lowered = {part.lower() for part in PurePath(target).parts}
    if lowered.intersection(FORBIDDEN_OUTPUT_COMPONENTS):
        stop(
            "FORMAL_PATH_FORBIDDEN",
            "$.output",
            "formal Episode, system, template, and Legacy paths are forbidden",
        )
    if any(protected_designations(part) for part in PurePath(target).parts):
        stop(
            "PROTECTED_PATH_FORBIDDEN",
            "$.output",
            "LOCK/FINAL/MASTER/APPROVED paths are immutable",
        )
    resolved = target.resolve(strict=False)
    if resolved.exists():
        stop(
            "OUTPUT_CONFLICT",
            "$.output",
            "existing output cannot be overwritten",
        )
    if not resolved.parent.exists() or not resolved.parent.is_dir():
        stop(
            "OUTPUT_PARENT_MISSING",
            "$.output",
            "output parent directory must already exist",
        )
    return resolved


def _candidate(item_type: str, episode_id: str, **values: Any) -> dict[str, Any]:
    return {
        "work_item_id": WORK_ITEM_ID,
        "artifact_type": item_type,
        "episode_id": episode_id,
        "status": "CANDIDATE",
        **values,
    }


def _build_gate_register(episode_id: str) -> list[dict[str, Any]]:
    records = [
        {
            "gate_id": gate_id,
            "gate_status": "PENDING",
            "approved_version": "",
            "approved_by": "",
            "approved_at": "",
            "basis_documents": [],
            "evidence_status": "UNVERIFIED",
            "dependency_recheck_result": "NOT_REQUIRED",
            "blocked_reason": "PENDING_HUMAN_REVIEW",
            "episode_id": episode_id,
        }
        for gate_id in GATE_IDS
    ]
    validate_gate_register(records)
    return records


def assert_dependency_ready(status: str) -> None:
    if status != "PASS":
        stop(
            "DEPENDENCY_NOT_PASS",
            "$.dependency_status",
            "downstream execution requires dependency PASS",
        )


def build_candidate_package(brief_value: Mapping[str, Any]) -> dict[str, Any]:
    brief = validate_brief(brief_value)
    episode_id = brief["episode_id"]
    plan = {
        "plan_id": f"{episode_id}_PLAN_V1",
        "scope_type": "PLAN_CANDIDATE",
        "scope_id": episode_id,
        "episode_id": episode_id,
        "evidence_status": "VERIFIED",
        "evidence_source": ["P2_WF_01_VALIDATED_BRIEF"],
        "version_refs": ["P2_WF_01_V1"],
        "owner": "PENDING_HUMAN_REVIEW",
        "timestamp": "PENDING_RUNTIME_TIMESTAMP",
        "operation": "VALIDATE_PLAN",
    }
    validate_episode_initialization_plan(plan)

    audience = _candidate(
        "AUDIENCE_INSIGHT",
        episode_id,
        lifecycle_status="DRAFT",
        target_audience=brief["target_audience"],
        surface_need=f"Understand: {brief['purpose']}",
        deeper_need=f"Act toward: {brief['desired_action']}",
        trust_barrier="PENDING_HUMAN_RESEARCH",
        original_value_source=brief["purpose"],
        evidence_status="INFERRED",
    )
    hooks = _candidate(
        "HOOK_STRATEGY_CANDIDATES",
        episode_id,
        lifecycle_status="DRAFT",
        candidates=[
            {"strategy": "HIGH_RETENTION", "hook": f"Stop scrolling: {brief['title']}"},
            {"strategy": "HIGH_RESONANCE", "hook": f"For {brief['target_audience']}: {brief['purpose']}"},
            {"strategy": "HIGH_CONVERSION", "hook": f"Next step: {brief['desired_action']}"},
        ],
    )
    creative = _candidate(
        "CREATIVE_LOCK_CANDIDATE",
        episode_id,
        lifecycle_status="DRAFT",
        review_status="PENDING_HUMAN_REVIEW",
        approved_by=None,
        selected_hook=None,
        core_claim=brief["purpose"],
        desired_action=brief["desired_action"],
    )
    story = _candidate(
        "STORY_TREATMENT_CANDIDATE",
        episode_id,
        lifecycle_status="DRAFT",
        treatment={
            "opening": "PENDING_HUMAN_REVIEW",
            "conflict": "PENDING_HUMAN_REVIEW",
            "escalation": "PENDING_HUMAN_REVIEW",
            "turning_point": "PENDING_HUMAN_REVIEW",
            "solution": brief["purpose"],
            "result": brief["desired_action"],
            "ending": "PENDING_HUMAN_REVIEW",
            "retention": "PENDING_HUMAN_REVIEW",
            "cta": brief["desired_action"],
        },
    )
    state = {
        "scope_type": "EPISODE",
        "scope_id": episode_id,
        "version_refs": ["P2_WF_01_V1"],
        "owner": "PENDING_HUMAN_REVIEW",
        "timestamp": "PENDING_RUNTIME_TIMESTAMP",
        "evidence_status": "INFERRED",
        "evidence_source": ["P2_WF_01_CANDIDATE_PACKAGE"],
        "dependency_status": "NOT_EVALUATED",
        "segment_status": None,
        "episode_status": "NOT_STARTED",
        "canonical_candidate": False,
        "blocked_reason": "PENDING_HUMAN_REVIEW",
    }
    validate_state_proposal(state)
    gates = _build_gate_register(episode_id)
    status = {
        "asset_id": f"{episode_id}_ASSET_PLACEHOLDER",
        "lifecycle_status": "DRAFT",
        "qc_status": "PENDING",
        "usage_roles": [],
        "exact_asset": False,
        "approved_original_drive_file_id": "",
        "proposed_drive_file_id": "",
        "generated_or_redrawn": False,
    }
    validate_status(status)
    prompt = {
        "prompt_metadata_id": f"{episode_id}_PROMPT_METADATA_PLACEHOLDER",
        "scope": episode_id,
        "approved_input_refs": [f"{episode_id}_VALIDATED_BRIEF"],
        "evidence_status": "VERIFIED",
        "evidence_source": ["P2_WF_01_VALIDATED_BRIEF"],
        "version_refs": ["P2_WF_01_V1"],
        "owner": "PENDING_HUMAN_REVIEW",
        "timestamp": "PENDING_RUNTIME_TIMESTAMP",
        "blocked_reason": "PROMPT_CONTENT_NOT_GENERATED",
    }
    validate_prompt_metadata(prompt)
    handoff = _candidate(
        "STORYBOARD_FLOW_HANDOFF_PLACEHOLDER",
        episode_id,
        lifecycle_status="DRAFT",
        readiness="PENDING_HUMAN_REVIEW",
        evidence_status="UNVERIFIED",
        dependency_status="NOT_EVALUATED",
        gate_approval=None,
        input_refs=[],
        output_refs=[],
        failure_action="STOP_AND_REPORT",
        external_execution=False,
    )

    package = {
        OUTPUT_FILES[0]: plan,
        OUTPUT_FILES[1]: audience,
        OUTPUT_FILES[2]: hooks,
        OUTPUT_FILES[3]: creative,
        OUTPUT_FILES[4]: story,
        OUTPUT_FILES[5]: state,
        OUTPUT_FILES[6]: gates,
        OUTPUT_FILES[7]: status,
        OUTPUT_FILES[8]: prompt,
        OUTPUT_FILES[9]: handoff,
    }
    manifest = _candidate(
        "EXECUTION_MANIFEST",
        episode_id,
        lifecycle_status="DRAFT",
        work_item_id=WORK_ITEM_ID,
        external_operations=[],
        output_files=list(OUTPUT_FILES),
        checks={
            "brief": "PASS",
            "p1_contracts": "PASS",
            "candidate_only": "PASS",
            "external_operations": "ZERO",
        },
    )
    package[OUTPUT_FILES[10]] = manifest
    package[OUTPUT_FILES[11]] = _candidate(
        "VALIDATION_REPORT",
        episode_id,
        lifecycle_status="DRAFT",
        result="PASS",
        candidate_artifact_count=10,
        manifest_status="PASS",
        external_operation_count=0,
        human_approval_count=0,
        canonical_write_count=0,
    )
    return package


def _serialize(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def run_workflow(
    brief_value: Mapping[str, Any],
    output: str | Path,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    package = build_candidate_package(brief_value)
    target = _safe_output_path(output)
    if dry_run:
        return {
            "work_item_id": WORK_ITEM_ID,
            "dry_run": True,
            "output": str(target),
            "would_write": list(OUTPUT_FILES),
            "package": package,
        }

    staging = target.parent / f".{target.name}.p2-wf-01-{uuid.uuid4().hex}.tmp"
    try:
        staging.mkdir()
        for filename in OUTPUT_FILES:
            (staging / filename).write_text(
                _serialize(package[filename]),
                encoding="utf-8",
                newline="\n",
            )
        staging.rename(target)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return {
        "work_item_id": WORK_ITEM_ID,
        "dry_run": False,
        "output": str(target),
        "written": list(OUTPUT_FILES),
        "sha256": {
            filename: hashlib.sha256((target / filename).read_bytes()).hexdigest()
            for filename in OUTPUT_FILES
        },
    }


def _load_brief(path: str | Path) -> Mapping[str, Any]:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        stop("BRIEF_READ_FAILED", "$.brief", str(exc))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P2-WF-01 local candidate workflow")
    parser.add_argument("--brief", required=True, help="Brief JSON path")
    parser.add_argument("--output", required=True, help="New output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = run_workflow(
            _load_brief(args.brief),
            args.output,
            dry_run=args.dry_run,
        )
    except StopAndReport as exc:
        print(
            json.dumps(
                {
                    "status": "STOP_AND_REPORT",
                    "violations": [
                        {
                            "code": item.code,
                            "path": item.path,
                            "message": item.message,
                        }
                        for item in exc.violations
                    ],
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
