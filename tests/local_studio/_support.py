from __future__ import annotations

from typing import Any


def brief(episode_id: str = "TEST_LOCAL_STUDIO_MVP") -> dict[str, Any]:
    return {
        "episode_id": episode_id,
        "series_id": "SERIES_TEST",
        "series_name": "測試系列",
        "title": "本機製片整合測試",
        "purpose": "驗證候選資料、人工 Gate 與交接流程",
        "target_audience": "測試受眾",
        "duration_seconds": 30,
        "platform": "YouTube Shorts",
        "aspect_ratio": "9:16",
        "desired_action": "了解課程",
        "existing_character_usage": "NONE",
        "special_requirements": ["TEST_SCOPE"],
    }


def artifact(artifact_type: str = "AUDIENCE_INSIGHT", version: str = "V1.0") -> dict[str, Any]:
    return {
        "episode_id": "TEST_LOCAL_STUDIO_MVP",
        "series_id": "SERIES_TEST",
        "artifact_type": artifact_type,
        "version": version,
        "lifecycle_status": "DRAFT",
        "approval_status": "PENDING_HUMAN_REVIEW",
        "lock_status": "UNLOCKED",
        "production_state": "CREATIVE_REVIEW",
        "source_asset_ids": [],
        "payload": {"content": "ChatGPT 測試候選內容"},
    }
