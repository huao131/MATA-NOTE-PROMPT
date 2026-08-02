#!/usr/bin/env python3
"""Cloud-safe verification of committed Windows local-production evidence."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / "reports" / "true_jk_rowling_runner_manifest.json").read_text(encoding="utf-8"))
golden = json.loads((ROOT / "golden" / "history_today" / "jk_rowling_v6_2" / "GOLDEN_BASELINE_MANIFEST.json").read_text(encoding="utf-8"))
required = {"EDGE_TTS", "FASTER_WHISPER_ALIGNMENT", "FLOW_HERO", "CAMERA_MOTION_SCENE_01", "AUDIO_MIX_DUCKING", "BILINGUAL_SUBTITLE_BAND", "ENDING", "QC_MONTAGE"}
assert golden["classification"] == "APPROVED_IMMUTABLE_GOLDEN_BASELINE"
assert manifest["status"] == "SUCCESS"
assert required <= set(manifest["completed_stages"])
assert manifest["error"] is None
print("local_production_evidence=PASS")
