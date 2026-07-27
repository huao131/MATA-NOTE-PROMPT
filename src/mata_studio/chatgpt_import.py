"""ChatGPT JSON import and validation helpers for V1.1."""

from __future__ import annotations

import json
import re
from typing import Any

from .errors import StudioError


class ChatGPTImportParser:
    def __init__(self, store):
        self.store = store

    def _extract_candidates(self, raw_text: str) -> list[dict[str, Any]]:
        candidates = []

        # 1. Extract markdown code blocks
        blocks = re.findall(r'```(?:json)?\s*(.*?)\s*```', raw_text, re.S)
        for block in blocks:
            try:
                obj = json.loads(block)
                if isinstance(obj, dict):
                    candidates.append(obj)
            except json.JSONDecodeError:
                continue

        # 2. If no valid JSON in blocks, scan for objects using raw_decode
        if not candidates:
            decoder = json.JSONDecoder()
            idx = 0
            while idx < len(raw_text):
                try:
                    obj, end = decoder.raw_decode(raw_text[idx:])
                    if isinstance(obj, dict):
                        candidates.append(obj)
                    idx += end
                except (json.JSONDecodeError, ValueError):
                    idx += 1

        # De-duplicate identical objects
        unique_candidates = []
        for c in candidates:
            if c not in unique_candidates:
                unique_candidates.append(c)
        return unique_candidates

    def import_payload(self, episode_id: str, raw_text: str) -> dict[str, Any]:
        candidates = self._extract_candidates(raw_text)

        if not candidates:
            raise StudioError("NO_JSON_FOUND", "未找到有效的 JSON 內容")

        if len(candidates) > 1:
            raise StudioError("MULTIPLE_JSON_OBJECTS_CONFLICT", "偵測到多個不同的 JSON Object")

        payload = candidates[0]

        payload.setdefault('episode_id', episode_id)
        if payload.get('episode_id') != episode_id:
            raise StudioError("EPISODE_ID_MISMATCH", "Episode ID 不一致")
        if payload.get('artifact_type') not in {'CREATIVE_CANDIDATE', 'STORY_TREATMENT', 'FLOW_PRODUCTION_PACKAGE'}:
            raise StudioError("INVALID_ARTIFACT_TYPE", "Artifact Type 錯誤")
        if 'version' not in payload:
            raise StudioError("VERSION_MISSING", "Version 缺失")
        if 'approved_by' in payload:
            raise StudioError("FORBIDDEN_FIELD", "Payload 不得包含 approved_by")

        return payload
