"""ChatGPT context package generator for V1.1."""

from __future__ import annotations

from typing import Any


def build_context_package(
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
    drive_mapping: dict[str, Any] | None = None,
) -> dict[str, Any]:
    drive_mapping = drive_mapping or {}
    return {
        'SYSTEM_IDENTITY': {
            'system_name': 'MATA AI VIDEO STUDIO',
            'repository': 'huao131/MATA-AI-VIDEO-STUDIO',
            'specification_ref': specification_context.get('source_ref', 'review/v2-system-specification-publication-v2'),
            'specification_commit_sha': specification_context.get('source_commit_sha', 'unknown'),
            'sop_version': specification_context.get('sop_version', 'V2.0'),
            'package_version': 'v1.1-chatgpt-work-package-bridge',
            'generated_at': '2026-07-27T00:00:00Z',
        },
        'ROLE_AND_RESPONSIBILITY': {
            'chatgpt_role': '創意與製片內容生成',
            'mata_role': '人工決策與 Gate',
            'studio_role': '整理與驗證整體流程',
        },
        'GLOBAL_RULES': [
            '一支影片一個 Episode 與一個獨立 Chat',
            'LOCK／FINAL／MASTER／APPROVED 不得覆寫',
            'Exact Asset 不得重繪',
            'ChatGPT 不得自行批准 Gate',
        ],
        'EPISODE_BRIEF': brief,
        'CURRENT_STATE': {
            'production_state': production_state,
            'artifacts': artifacts,
            'gates': gates,
            'approvals': approvals,
            'locks': locks,
            'rejected_assets': rejected_assets,
            'dependency_status': dependency_status,
            'drive_status': drive_status,
            'drive_mapping': drive_mapping,
            'sync_status': 'SYNCED' if drive_status.get('status') in {'CONNECTED', 'SYNCED', 'SYNC_COMPLETE'} else 'NOT_SYNCED',
        },
        'CURRENT_TASK': {
            'task_id': 'AUDIENCE_INSIGHT_AND_CREATIVE_STRATEGY',
            'task_name_zh_TW': '產生 Creative 工作包',
            'required_inputs': ['brief', 'specification_context', 'drive_mapping'],
            'output_contract': {'artifact_type': 'CREATIVE_CANDIDATE'},
            'next_ui_hint_zh_TW': '先產生 Creative 工作包，再在 Creative Studio 驗證並提交 creative_lock Gate。',
        },
        'OUTPUT_CONTRACT': {
            'must_return_json': True,
            'artifact_type': 'CREATIVE_CANDIDATE',
            'schema_hint': 'creative_candidate.schema.json',
        },
    }
