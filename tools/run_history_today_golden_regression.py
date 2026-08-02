#!/usr/bin/env python3
"""Fail-closed Golden Regression gate for History Today releases."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "golden" / "history_today" / "jk_rowling_v6_2"
REPORT_DIR = ROOT / "reports" / "golden_regression"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def result(check_id: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {"check_id": check_id, "result": "PASS" if passed else "FAIL", "evidence": evidence}


def media_decode(path: Path, ffmpeg: str) -> tuple[bool, str]:
    completed = subprocess.run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, check=False)
    return completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")[-1000:]


def main() -> int:
    checks: list[dict[str, Any]] = []
    manifest_path = GOLDEN / "GOLDEN_BASELINE_MANIFEST.json"
    if not manifest_path.is_file():
        print("release_gate=FAIL missing golden manifest")
        return 1
    manifest = json.loads(text(manifest_path))
    mismatches = []
    declared = set()
    for item in manifest["files"]:
        path = GOLDEN / item["path"]
        declared.add(item["path"])
        if not path.is_file() or path.stat().st_size != item["size_bytes"] or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    actual = {path.relative_to(GOLDEN).as_posix() for path in GOLDEN.rglob("*") if path.is_file()}
    allowed_control = {"GOLDEN_BASELINE_MANIFEST.json", "IMMUTABLE.lock"}
    undeclared = sorted(actual - declared - allowed_control)
    checks.append(result("golden_baseline_untouched", not mismatches and not undeclared, {"mismatches": mismatches, "undeclared": undeclared}))

    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = shutil.which("ffmpeg") or "ffmpeg"

    motion = text(GOLDEN / "source_programs" / "run_v6_motion.py")
    motion_ok = all(token in motion.lower() for token in ("scene_01", "scene_02", "scene_04", "scene_05")) and any(token in motion.lower() for token in ("zoompan", "push", "pan", "crop"))
    checks.append(result("camera_motion_direction", motion_ok, "run_v6_motion.py contains scene-specific motion implementation"))

    flow_path = GOLDEN / "flow" / "FLOW_SCENE_03.mp4"
    flow_decode, flow_error = media_decode(flow_path, ffmpeg)
    checks.append(result("approved_flow_scene", flow_decode, {"path": str(flow_path), "sha256": sha256(flow_path), "decode_error": flow_error}))

    package_root = ROOT / "runners" / "release_candidates" / "2.1.0-rc.1" / "flow"
    schema = json.loads(text(package_root / "FLOW_ASSET_PACKAGE.schema.json"))
    package = json.loads(text(package_root / "jk_rowling_scene_03" / "FLOW_ASSET_PACKAGE.json"))
    schema_errors = sorted(Draft202012Validator(schema).iter_errors(package), key=lambda item: list(item.path))
    source_image = ROOT / package["source_image_path"]
    required_negative = {
        "任何文字", "任何字幕", "任何Logo", "任何水印", "Storyboard版面", "資訊圖表",
        "現代物件", "角色變臉", "多餘人物", "多餘肢體或手指", "水平鏡像", "過度誇張動作"
    }
    flow_capability = {
        "schema_valid": not schema_errors,
        "english_prompt": len(package["flow_prompt_en"]) >= 300,
        "chinese_prompt": len(package["flow_prompt_zh_tw"]) >= 300 and bool(re.search(r"[\u4e00-\u9fff]", package["flow_prompt_zh_tw"])),
        "negative_prompt": required_negative.issubset(set(package["negative_prompt"])),
        "source_image_sha256": source_image.is_file() and sha256(source_image) == package["source_image_sha256"],
        "approved_regression_asset": package["flow_asset_mode"] == "APPROVED_REGRESSION_ASSET" and flow_decode,
        "queue_and_filename": package["output_filename"] == "FLOW_SCENE_03.mp4" and bool(package["resume_watch_folder"]),
        "manual_resume": len(package["manual_steps"]) == 1 and "唯一人工步驟" in package["manual_steps"][0],
    }
    checks.append(result("flow_prompt_package", all(flow_capability.values()), flow_capability))

    environment = json.loads(text(GOLDEN / "ENVIRONMENT.json"))
    checks.append(result("edge_tts_environment", bool(environment.get("edge_tts")), environment.get("edge_tts")))
    checks.append(result("faster_whisper_environment", bool(environment.get("faster_whisper")), environment.get("faster_whisper")))

    required_audio = [GOLDEN / "audio" / name for name in ("BGM.wav", "AMBIENCE_SPACE.wav", "SFX.wav")]
    audio_ok = all(path.is_file() and path.stat().st_size > 1024 for path in required_audio)
    build_script = text(GOLDEN / "source_programs" / "build_mata_video.py").lower()
    ducking_ok = "sidechaincompress" in build_script or "duck" in build_script
    checks.append(result("audio_layers_and_ducking", audio_ok and ducking_ok, {"audio": [str(path) for path in required_audio], "ducking_implementation": ducking_ok}))

    subtitle_ass = text(GOLDEN / "subtitles" / "SUBTITLE_ZH_TW_EN_V5_2.ass")
    header_config = text(GOLDEN / "configuration" / "header_style_v5_2.json")
    checks.append(result("canonical_header_and_gold_line", "gold" in header_config.lower() or "#" in header_config, "header_style_v5_2.json"))
    checks.append(result("traditional_chinese_subtitle", bool(re.search(r"[\u4e00-\u9fff]", subtitle_ass)), "bilingual ASS contains CJK text"))
    checks.append(result("english_small_subtitle", bool(re.search(r"[A-Za-z]{4,}", subtitle_ass)), "bilingual ASS contains English"))
    checks.append(result("dark_translucent_band", any(token in subtitle_ass.upper() for token in ("&H80", "&H90", "&HA0", "BACKCOLOUR")), "ASS background style"))

    ending = GOLDEN / "ending" / "ENDING_NORMALIZED.mp4"
    ending_ok, ending_error = media_decode(ending, ffmpeg)
    checks.append(result("fixed_time_page_ending", ending_ok, {"sha256": sha256(ending), "decode_error": ending_error}))

    master_results = {}
    for name in ("MASTER_V6_2_NO_MAIN_SUBTITLE.mp4", "MASTER_PREVIEW_V6_2_ZH_TW_EN_SUBTITLE.mp4"):
        path = GOLDEN / "masters" / name
        decoded, error = media_decode(path, ffmpeg)
        master_results[name] = {"decode": decoded, "sha256": sha256(path), "error": error}
    checks.append(result("two_approved_masters", all(value["decode"] for value in master_results.values()), master_results))

    qc = GOLDEN / "qc" / "QC_MONTAGE_V6_2.jpg"
    delivery = GOLDEN / "delivery" / "DELIVERY_MANIFEST_V5_2.json"
    checks.append(result("qc_and_onedrive_classification", qc.is_file() and qc.stat().st_size > 1024 and delivery.is_file(), {"qc": str(qc), "delivery": str(delivery)}))

    transport_files = [ROOT / "control" / name for name in ("github_api_transport.py", "local_watcher.py", "chatgpt_runner_bridge.py")]
    transport_text = "\n".join(text(path) for path in transport_files)
    transport_ok = all(path.is_file() for path in transport_files) and all(token in transport_text for token in ("GitHubApiTransport", "LocalWatcher", "Bridge"))
    checks.append(result("chatgpt_transport_chain", transport_ok, [str(path) for path in transport_files]))

    flags = json.loads(text(ROOT / "config" / "history_today_feature_flags.json"))["defaults"]
    checks.append(result("feature_flags_default_off", flags and all(value is False for value in flags.values()), flags))

    required_ids = {item["check_id"] for item in checks}
    gate = "PASS" if all(item["result"] == "PASS" for item in checks) and len(required_ids) == len(checks) else "FAIL"
    report = {
        "report_type": "HISTORY_TODAY_GOLDEN_REGRESSION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "release_gate": gate,
        "current_release_update_allowed": gate == "PASS",
        "checks": checks,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# History Today Golden Regression", "", f"release_gate = **{gate}**", ""]
    lines.extend(f"- {item['check_id']}: {item['result']}" for item in checks)
    (REPORT_DIR / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"release_gate={gate}")
    return 0 if gate == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
