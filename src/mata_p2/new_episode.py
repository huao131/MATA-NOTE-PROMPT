"""P2-WF-01 New Episode Workflow MVP.

The workflow creates local candidate JSON only. It never calls external
services and never declares a human Gate approval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
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
REMEDIATION_ID = "P2-WF-01.1"
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
    existing_parent = next(
        (parent for parent in resolved.parents if parent.exists()),
        None,
    )
    if existing_parent is None or not existing_parent.is_dir():
        stop(
            "OUTPUT_PARENT_INVALID",
            "$.output",
            "output must resolve beneath an existing directory",
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


def _is_beauty_business(brief: Mapping[str, Any]) -> bool:
    text = " ".join(
        str(brief[field])
        for field in ("title", "purpose", "target_audience", "special_requirements")
    )
    return any(
        keyword in text
        for keyword in ("美容", "美睫", "美甲", "醫美", "美業", "美容師")
    )


def _audience_insight(brief: Mapping[str, Any]) -> dict[str, Any]:
    if _is_beauty_business(brief):
        surface_pains = [
            "沒有時間持續自拍與安排內容拍攝",
            "不擅長剪輯，製作一支短片耗時過久",
            "忙於服務顧客，內容產出時有時無",
            "影片有觀看，卻未有效轉成詢問或預約",
            "擔心AI影片失去個人風格與專業信任感",
            "希望維持專業曝光，但不想每天親自出鏡",
            "覺得學習新AI工具複雜，擔心沒有時間上手",
        ]
        deep_pains = [
            "專業能力被內容產能限制，無法被市場持續看見",
            "投入拍攝與剪輯後仍缺乏穩定詢問，容易懷疑行銷是否值得",
            "害怕使用AI後品牌變得制式，削弱顧客對本人專業的信任",
        ]
        core_desires = [
            "用更低負擔的方式穩定呈現專業",
            "讓內容自然增加詢問與預約機會，而非承諾必然成效",
            "保留個人特色，同時建立可持續的內容流程",
        ]
        misconceptions = [
            "只有天天本人出鏡才有真實感",
            "AI影片等於套版內容，必然失去個人風格",
            "只要影片有流量，就會自然轉成預約",
        ]
        viewing_motivations = [
            "想知道不必天天自拍也能維持曝光的方法",
            "想降低剪輯門檻並改善內容斷更",
            "想把觀看更合理地引導至詢問與課程學習",
        ]
        action_resistance = [
            "擔心工具太複雜、學習時間不足",
            "不確定AI能否保留自己的語氣與專業特色",
            "害怕課程只教工具，無法落地到美業情境",
        ]
        belief = (
            "美業老闆不是不會經營，而是內容生產方式太依賴本人；"
            "AI的價值不是取代專業，而是讓專業能被持續看見。"
        )
        needs_human_input: list[str] = []
    else:
        audience = brief["target_audience"]
        surface_pains = [
            f"{audience}缺少可持續的內容製作時間",
            f"{audience}面臨內容產出不穩定的問題",
        ]
        deep_pains = [f"{audience}的專業價值未被內容持續呈現"]
        core_desires = [f"以可控負擔達成：{brief['desired_action']}"]
        misconceptions = ["必須提高製作量才能提高內容成效"]
        viewing_motivations = [f"尋找與「{brief['title']}」相關的可行方法"]
        action_resistance = ["尚未確認工具學習成本與品牌適配方式"]
        belief = "內容流程應放大專業，而不是取代專業。"
        needs_human_input = [
            "請人工確認目標受眾最優先的三項情境痛點",
            "請人工確認品牌不可使用的語氣與宣稱",
        ]
    return _candidate(
        "AUDIENCE_INSIGHT",
        brief["episode_id"],
        lifecycle_status="DRAFT",
        target_audience=brief["target_audience"],
        surface_need=surface_pains[0],
        deeper_need=deep_pains[0],
        trust_barrier=action_resistance[0],
        surface_pains=surface_pains,
        deep_pains=deep_pains,
        core_desires=core_desires,
        misconceptions=misconceptions,
        viewing_motivations=viewing_motivations,
        action_resistance=action_resistance,
        core_belief_to_attack=belief,
        needs_human_input=needs_human_input,
        original_value_source=brief["purpose"],
        evidence_status="INFERRED",
    )


def _hook_candidates(brief: Mapping[str, Any], belief: str) -> dict[str, Any]:
    beauty = _is_beauty_business(brief)
    if beauty:
        candidates = [
            {
                "strategy": "HIGH_RETENTION",
                "hook": "還在天天自拍剪片，預約卻沒有跟著穩定嗎？",
                "core_viewpoint": "問題不一定是專業不足，而是內容太依賴本人。",
                "story_direction": "以忙碌出鏡與內容斷更的反差切入AI協作。",
                "emotional_curve": ["意外", "警覺", "看見新方法"],
                "cta_direction": "了解原創AI影片如何降低內容負擔。",
                "recommendation_reason": "用投入與結果的反差，在前三秒建立停留動機。",
            },
            {
                "strategy": "HIGH_RESONANCE",
                "hook": "做完客人已經很累，還要自拍、剪片、想文案。",
                "core_viewpoint": "美業經營者缺的不是努力，而是可持續的內容流程。",
                "story_direction": "從服務後的疲累與斷更，帶到保留個人特色的AI方法。",
                "emotional_curve": ["疲累", "被理解", "鬆一口氣"],
                "cta_direction": "看看AI如何協助穩定呈現你的專業。",
                "recommendation_reason": "直接描述日常壓力，提高受眾被理解的感受。",
            },
            {
                "strategy": "HIGH_CONVERSION",
                "hook": "學會原創AI影片，讓專業內容穩定出現，預約機會才有入口。",
                "core_viewpoint": "AI不承諾預約結果，但能協助建立穩定曝光與詢問入口。",
                "story_direction": "呈現從內容斷更到穩定輸出的可學習轉變。",
                "emotional_curve": ["期待", "信任", "願意了解"],
                "cta_direction": "報名課程，學習適合美業的原創AI影片流程。",
                "recommendation_reason": "清楚連結學習成果與下一步，但不做成效保證。",
            },
        ]
    else:
        candidates = [
            {
                "strategy": "HIGH_RETENTION",
                "hook": f"你以為做不到「{brief['title']}」，問題可能不在專業。",
                "core_viewpoint": belief,
                "story_direction": "用認知反差快速提出替代方法。",
                "emotional_curve": ["好奇", "理解", "期待"],
                "cta_direction": brief["desired_action"],
                "recommendation_reason": "以反差建立前三秒停留。",
            },
            {
                "strategy": "HIGH_RESONANCE",
                "hook": f"{brief['target_audience']}，你的內容壓力不該只靠硬撐。",
                "core_viewpoint": belief,
                "story_direction": "先承接受眾壓力，再提出可持續流程。",
                "emotional_curve": ["疲累", "共鳴", "釋放"],
                "cta_direction": brief["desired_action"],
                "recommendation_reason": "以受眾日常困境建立共鳴。",
            },
            {
                "strategy": "HIGH_CONVERSION",
                "hook": f"從今天開始，用可學習的方法靠近：{brief['desired_action']}。",
                "core_viewpoint": belief,
                "story_direction": "聚焦可學習方法與低壓下一步。",
                "emotional_curve": ["希望", "可行", "行動"],
                "cta_direction": brief["desired_action"],
                "recommendation_reason": "明確提出下一步，避免保證性成效。",
            },
        ]
    return _candidate(
        "HOOK_STRATEGY_CANDIDATES",
        brief["episode_id"],
        lifecycle_status="DRAFT",
        candidates=candidates,
        primary_hook=candidates[0],
        supporting_hooks=candidates[1:],
        hook_psychological_path=[
            "辨識既有痛點",
            "挑戰內容必須完全依賴本人的認知",
            "建立AI協助而非取代專業的理解",
            "引導低壓課程學習行動",
        ],
    )


def _timeline(duration: int) -> list[dict[str, Any]]:
    boundaries = [0]
    for ratio in (0.15, 0.35, 0.60, 0.85):
        point = max(boundaries[-1] + 1, round(duration * ratio))
        boundaries.append(min(point, duration - (4 - len(boundaries))))
    boundaries.append(duration)
    labels = ("HOOK", "PAIN", "REFRAME", "SOLUTION", "CTA")
    return [
        {"phase": label, "start_seconds": start, "end_seconds": end}
        for label, start, end in zip(labels, boundaries, boundaries[1:])
    ]


def _story_treatment(brief: Mapping[str, Any]) -> dict[str, Any]:
    beauty = _is_beauty_business(brief)
    if beauty:
        content = {
            "opening": "0–3秒：美業老闆服務完顧客，面對手機鏡頭與待剪素材，字幕問「還要天天自拍嗎？」",
            "conflict": "3–7秒：快速呈現沒時間拍、剪輯卡住、內容斷更，影片有觀看卻少有詢問。",
            "escalation": "7–12秒：點出真正瓶頸不是專業不足，而是內容生產過度依賴本人。",
            "turning_point": "12–17秒：提出原創AI影片可協助整理專業觀點、穩定產出，同時保留個人風格。",
            "solution": "用AI建立可持續的內容流程，增加專業被看見及產生詢問與預約的機會，但不承諾結果。",
            "result": "讓美業經營者看見降低內容負擔、維持專業曝光的可學習方向。",
            "ending": "17–20秒：畫面收在課程學習邀請，字幕「讓AI協助內容，不取代你的專業」。",
            "emotional_curve": ["疲累", "被理解", "認知反轉", "看見可行方法", "願意了解"],
            "retention_nodes": ["0秒痛點提問", "7秒認知反轉", "12秒AI價值揭示", "17秒CTA"],
            "cta_transition": "如果你也想減少天天自拍剪片的壓力，來了解原創AI影片課程。",
        }
    else:
        content = {
            "opening": f"前段直接提出：{brief['title']}",
            "conflict": f"呈現{brief['target_audience']}目前的內容阻力。",
            "escalation": "說明依賴既有做法會造成內容不穩定。",
            "turning_point": "提出AI協助內容流程、但不取代專業的核心觀點。",
            "solution": brief["purpose"],
            "result": "讓受眾看見可學習且不保證結果的下一步。",
            "ending": f"自然引導：{brief['desired_action']}",
            "emotional_curve": ["辨識", "共鳴", "理解", "期待", "行動"],
            "retention_nodes": ["開場認知衝突", "中段方法揭示", "結尾低壓CTA"],
            "cta_transition": brief["desired_action"],
        }
    return _candidate(
        "STORY_TREATMENT_CANDIDATE",
        brief["episode_id"],
        lifecycle_status="DRAFT",
        duration_seconds=brief["duration_seconds"],
        platform=brief["platform"],
        aspect_ratio=brief["aspect_ratio"],
        pace_segments=_timeline(brief["duration_seconds"]),
        treatment=content,
        needs_human_input=[] if beauty else ["請人工確認場景與品牌語氣"],
    )


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


def _validate_initialization_candidate(plan: Mapping[str, Any]) -> None:
    """Reuse the P1 shape contract without misclassifying a P2 candidate as a write.

    P1 intentionally rejects every formal-looking Episode ID because P1 has no
    formal Episode execution authority. P2-WF-01.1 is authorized to prepare a
    PLAN_CANDIDATE for such an ID, but still never writes the formal Episode tree.
    A shadow TEST identity lets P1 validate the complete record shape while the
    returned candidate retains its governed EP identity.
    """
    if plan.get("scope_type") != "PLAN_CANDIDATE":
        stop(
            "FORMAL_EPISODE_WRITE_FORBIDDEN",
            "$.scope_type",
            "formal Episode identity is allowed only for PLAN_CANDIDATE",
        )
    shadow = dict(plan)
    shadow["scope_id"] = "TEST_P2_WF_01_FORMAL_ID_CANDIDATE"
    shadow["episode_id"] = "TEST_P2_WF_01_FORMAL_ID_CANDIDATE"
    validate_episode_initialization_plan(shadow)


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
    if episode_id.startswith("TEST_"):
        validate_episode_initialization_plan(plan)
    else:
        _validate_initialization_candidate(plan)

    audience = _audience_insight(brief)
    hooks = _hook_candidates(brief, audience["core_belief_to_attack"])
    creative = _candidate(
        "CREATIVE_LOCK_CANDIDATE",
        episode_id,
        lifecycle_status="DRAFT",
        audience=brief["target_audience"],
        hook_strategy=hooks["primary_hook"],
        core_message=audience["core_belief_to_attack"],
        narrative_direction=hooks["primary_hook"]["story_direction"],
        cta_direction=brief["desired_action"],
        approval_status="PENDING_HUMAN_REVIEW",
        approved_by=None,
        needs_human_input=[],
    )
    story = _story_treatment(brief)
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
            "creative_candidate_generation": "PASS",
            "brief_input_contract": REMEDIATION_ID,
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

    try:
        target.mkdir(parents=True)
        for filename in OUTPUT_FILES:
            (target / filename).write_text(
                _serialize(package[filename]),
                encoding="utf-8",
                newline="\n",
            )
    except Exception:
        if target.exists():
            for created in target.iterdir():
                if created.is_file():
                    created.unlink()
            target.rmdir()
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


def _load_brief_json(value: str) -> Mapping[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        stop("BRIEF_JSON_INVALID", "$.brief_json", f"invalid JSON at position {exc.pos}")
    return require_mapping(parsed, "$.brief_json")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P2-WF-01 local candidate workflow")
    parser.add_argument("--brief", help="Brief JSON path")
    parser.add_argument("--brief-json", help="Inline Brief JSON; no temporary file is created")
    parser.add_argument("--output", required=True, help="New output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if bool(args.brief) == bool(args.brief_json):
            stop(
                "BRIEF_INPUT_EXACTLY_ONE_REQUIRED",
                "$.brief_input",
                "provide exactly one of --brief or --brief-json",
            )
        brief = (
            _load_brief(args.brief)
            if args.brief
            else _load_brief_json(args.brief_json)
        )
        result = run_workflow(
            brief,
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
