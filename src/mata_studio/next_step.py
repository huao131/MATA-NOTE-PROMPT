"""Minimal next-step engine for V1.1."""

from __future__ import annotations

from typing import Any


def evaluate_next_step(
    *,
    episode_id: str,
    brief: dict[str, Any],
    production_state: str,
    gates: dict[str, Any],
    artifacts: list[dict[str, Any]],
    approvals: dict[str, Any],
    locks: dict[str, Any],
    rejected_assets: list[dict[str, Any]],
    dependency_status: dict[str, Any],
    drive_status: dict[str, Any],
    specification_context: dict[str, Any],
) -> dict[str, Any]:
    spec_status = specification_context.get('status') if isinstance(specification_context, dict) else None
    if spec_status == 'SPECIFICATION_CONTEXT_UNAVAILABLE':
        return {
            'episode_id': episode_id,
            'status': 'BLOCKED',
            'next_task_id': 'SPECIFICATION_CONTEXT_UNAVAILABLE',
            'next_task_name_zh_TW': '等待規格上下文可用',
            'current_stage': 'SPECIFICATION_BLOCKED',
            'why_blocked': f"SPECIFICATION_CONTEXT_UNAVAILABLE: {specification_context.get('reason', 'unknown')}",
            'required_inputs': ['specification_context'],
            'missing_inputs': ['specification_context'],
            'allowed_actions': ['resolve_specification_context'],
            'prohibited_actions': ['auto_approve_gate', 'generate_chatgpt_package'],
            'expected_artifact_types': [],
            'expected_output_schema': '',
            'next_gate': 'creative_lock',
            'drive_target_folders': [],
            'context_package_ready': False,
        }

    if production_state in {'AWAITING_CREATIVE_INPUT', 'NEW_EPISODE'}:
        return {
            'episode_id': episode_id,
            'status': 'READY',
            'next_task_id': 'AUDIENCE_INSIGHT_AND_CREATIVE_STRATEGY',
            'next_task_name_zh_TW': '產生 Creative 工作包',
            'current_stage': 'CREATIVE',
            'why_blocked': '尚未建立 Creative Candidate。',
            'required_inputs': ['episode_brief', 'specification_context'],
            'missing_inputs': ['creative_candidate'],
            'allowed_actions': ['generate_chatgpt_package'],
            'prohibited_actions': ['auto_approve_gate'],
            'expected_artifact_types': ['CREATIVE_CANDIDATE'],
            'expected_output_schema': 'creative_candidate.schema.json',
            'next_gate': 'creative_lock',
            'drive_target_folders': [],
            'context_package_ready': True,
        }

    if gates.get('creative_lock', {}).get('gate_status') == 'PASS':
        return {
            'episode_id': episode_id,
            'status': 'READY',
            'next_task_id': 'STORY_AND_VISUAL_DEVELOPMENT',
            'next_task_name_zh_TW': '進入 Story 與 Visual Bible',
            'current_stage': 'STORY',
            'why_blocked': 'Creative Gate 已通過，現在可進入 Story 與 Visual Bible。',
            'required_inputs': ['story_treatment', 'visual_bible'],
            'missing_inputs': ['story_treatment', 'visual_bible'],
            'allowed_actions': ['import_story_artifact'],
            'prohibited_actions': ['auto_approve_gate'],
            'expected_artifact_types': ['STORY_TREATMENT', 'VISUAL_BIBLE'],
            'expected_output_schema': 'story_treatment.schema.json',
            'next_gate': 'story_lock',
            'drive_target_folders': [],
            'context_package_ready': True,
        }

    return {
        'episode_id': episode_id,
        'status': 'READY',
        'next_task_id': 'EPISODE_SUMMARY_AND_ARCHIVE',
        'next_task_name_zh_TW': '進入總結與歸檔',
        'current_stage': 'COMPLETE',
        'why_blocked': '目前流程已達成最小可用範圍。',
        'required_inputs': [],
        'missing_inputs': [],
        'allowed_actions': [],
        'prohibited_actions': ['auto_approve_gate'],
        'expected_artifact_types': [],
        'expected_output_schema': 'episode_summary.schema.json',
        'next_gate': 'final_approved',
        'drive_target_folders': [],
        'context_package_ready': True,
    }
