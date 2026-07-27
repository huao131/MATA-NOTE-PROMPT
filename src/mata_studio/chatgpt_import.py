"""ChatGPT JSON import and validation helpers for V1.1."""

from __future__ import annotations

import json
import re
from typing import Any


class ChatGPTImportParser:
    def __init__(self, store):
        self.store = store

    def import_payload(self, episode_id: str, raw_text: str) -> dict[str, Any]:
        match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', raw_text, re.S)
        if not match:
            raise ValueError('未找到 JSON code block')
        payload = json.loads(match.group(1))
        payload.setdefault('episode_id', episode_id)
        if payload.get('episode_id') != episode_id:
            raise ValueError('Episode ID 不一致')
        if payload.get('artifact_type') not in {'CREATIVE_CANDIDATE', 'STORY_TREATMENT', 'FLOW_PRODUCTION_PACKAGE'}:
            raise ValueError('Artifact Type 錯誤')
        if 'version' not in payload:
            raise ValueError('Version 缺失')
        return payload
