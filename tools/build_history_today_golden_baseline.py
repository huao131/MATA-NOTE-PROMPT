#!/usr/bin/env python3
"""Create the immutable J.K. Rowling V6.2 baseline exactly once."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TARGET = REPO / "golden" / "history_today" / "jk_rowling_v6_2"
EPISODE = Path(r"C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0731\0731_JK_ROWLING")
RUNTIME = Path(r"C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\_SYSTEM\GOLDEN_PATH_RUNTIME_V1")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy(source: Path, relative: str, records: list[dict[str, object]]) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    destination = TARGET / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    records.append({"path": relative.replace("\\", "/"), "size_bytes": destination.stat().st_size, "sha256": sha256(destination)})


def command_output(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, check=False)
    return (result.stdout or result.stderr).decode("utf-8", errors="replace").strip()


def main() -> int:
    if TARGET.exists() and any(TARGET.iterdir()):
        print("GOLDEN_BASELINE_ALREADY_EXISTS_REFUSING_OVERWRITE")
        return 2
    TARGET.mkdir(parents=True, exist_ok=False)
    records: list[dict[str, object]] = []

    for source in sorted((RUNTIME / "scripts").glob("*")):
        if source.is_file():
            copy(source, f"source_programs/{source.name}", records)

    fixed = {
        "configuration/audio_style.json": EPISODE / "audio_style.json",
        "configuration/motion_presets.json": EPISODE / "motion_presets.json",
        "configuration/narration_style.json": EPISODE / "narration_style.json",
        "configuration/subtitle_style.json": EPISODE / "subtitle_style.json",
        "configuration/header_style_v5_2.json": EPISODE / "HEADER_STYLE_V5_2.json",
        "configuration/canonical_render_format.json": EPISODE / "HISTORY_TODAY_CANONICAL_RENDER_FORMAT_V1.json",
        "configuration/final_timeline_asset_map.json": EPISODE / "FINAL_TIMELINE_ASSET_MAP.json",
        "story/narration.txt": EPISODE / "02_腳本" / "narration.txt",
        "story/scene_plan.json": EPISODE / "02_腳本" / "scene_plan.json",
        "flow/FLOW_PROMPT.txt": EPISODE / "05_FLOW_QUEUE" / "SCENE_03" / "FLOW_PROMPT.txt",
        "flow/FLOW_SETTINGS.json": EPISODE / "05_FLOW_QUEUE" / "SCENE_03" / "FLOW_SETTINGS.json",
        "flow/README_ACTION.txt": EPISODE / "05_FLOW_QUEUE" / "SCENE_03" / "README_ACTION.txt",
        "flow/SOURCE_IMAGE.png": EPISODE / "05_FLOW_QUEUE" / "SCENE_03" / "SOURCE_IMAGE.png",
        "flow/FLOW_SCENE_03.mp4": EPISODE / "05_FLOW_QUEUE" / "SCENE_03" / "FLOW_SCENE_03.mp4",
        "subtitles/SUBTITLE_ZH_TW_V5_2.srt": EPISODE / "SUBTITLE_ZH_TW_V5_2.srt",
        "subtitles/SUBTITLE_ZH_TW_EN_V5_2.ass": EPISODE / "SUBTITLE_ZH_TW_EN_V5_2.ass",
        "subtitles/DISPLAY_SUBTITLE_V5_2_ZH_TW_EN.json": EPISODE / "DISPLAY_SUBTITLE_V5_2_ZH_TW_EN.json",
        "audio/BGM.wav": EPISODE / "05_剪映素材包" / "BGM.wav",
        "audio/AMBIENCE_SPACE.wav": EPISODE / "05_剪映素材包" / "SPACE.wav",
        "audio/SFX.wav": EPISODE / "05_剪映素材包" / "SFX.wav",
        "ending/ENDING_NORMALIZED.mp4": EPISODE / "05_剪映素材包" / "ENDING_NORMALIZED.mp4",
        "masters/MASTER_V6_2_NO_MAIN_SUBTITLE.mp4": EPISODE / "06_成品" / "MASTER_V6_2_NO_MAIN_SUBTITLE.mp4",
        "masters/MASTER_PREVIEW_V6_2_ZH_TW_EN_SUBTITLE.mp4": EPISODE / "06_成品" / "MASTER_PREVIEW_V6_2_ZH_TW_EN_SUBTITLE.mp4",
        "qc/CANONICAL_FORMAT_QC_V6_2.json": EPISODE / "CANONICAL_FORMAT_QC_V6_2.json",
        "qc/BILINGUAL_SUBTITLE_QC_V5_2.json": EPISODE / "BILINGUAL_SUBTITLE_QC_V5_2.json",
        "qc/QC_MONTAGE_V6_2.jpg": EPISODE / "06_成品" / "QC_MONTAGE_V6_2.jpg",
        "delivery/DELIVERY_CONFIG_V1.0.json": EPISODE / "06_成品" / "05_交付紀錄" / "DELIVERY_CONFIG_V1.0.json",
        "delivery/DELIVERY_MANIFEST_V5_2.json": EPISODE / "06_成品" / "05_交付紀錄" / "DELIVERY_MANIFEST_V5_2.json",
        "evidence/V5_2_BILINGUAL_BUILD_LOG.txt": EPISODE / "V5_2_BILINGUAL_BUILD_LOG.txt",
        "evidence/V5_2_FREEZE_MANIFEST.json": EPISODE / "V5_2_FREEZE_MANIFEST.json",
    }
    for index in range(1, 6):
        fixed[f"scenes/Scene_{index:02}.png"] = EPISODE / "03_視覺素材" / f"Scene_{index:02}.png"
    for relative, source in fixed.items():
        copy(source, relative, records)

    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    ffprobe = shutil.which("ffprobe")
    probes: dict[str, object] = {}
    for relative in ("masters/MASTER_V6_2_NO_MAIN_SUBTITLE.mp4", "masters/MASTER_PREVIEW_V6_2_ZH_TW_EN_SUBTITLE.mp4", "flow/FLOW_SCENE_03.mp4", "ending/ENDING_NORMALIZED.mp4"):
        path = TARGET / relative
        if ffprobe:
            raw = command_output([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
            probes[relative] = json.loads(raw)
        else:
            decode = subprocess.run([ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, check=False)
            probes[relative] = {"decode_exit_code": decode.returncode, "ffprobe_unavailable": True}
    (TARGET / "evidence" / "MEDIA_PROBES.json").write_text(json.dumps(probes, ensure_ascii=False, indent=2), encoding="utf-8")
    records.append({"path": "evidence/MEDIA_PROBES.json", "size_bytes": (TARGET / "evidence" / "MEDIA_PROBES.json").stat().st_size, "sha256": sha256(TARGET / "evidence" / "MEDIA_PROBES.json")})

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "ffmpeg": command_output([ffmpeg, "-version"]).splitlines()[0],
        "ffprobe": command_output([ffprobe, "-version"]).splitlines()[0] if ffprobe else "not available; decode verification recorded",
        "edge_tts": importlib.metadata.version("edge-tts"),
        "faster_whisper": importlib.metadata.version("faster-whisper"),
    }
    (TARGET / "ENVIRONMENT.json").write_text(json.dumps(environment, ensure_ascii=False, indent=2), encoding="utf-8")
    records.append({"path": "ENVIRONMENT.json", "size_bytes": (TARGET / "ENVIRONMENT.json").stat().st_size, "sha256": sha256(TARGET / "ENVIRONMENT.json")})

    manifest = {
        "baseline_id": "history_today/jk_rowling_v6_2",
        "classification": "APPROVED_IMMUTABLE_GOLDEN_BASELINE",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_episode": str(EPISODE),
        "prohibited_source_prefixes": ["_SYSTEM_TRUE_REGRESSION_RERUN", "_VALIDATION_RUNS"],
        "immutability": {"overwrite": False, "delete": False, "rename": False, "direct_edit": False},
        "files": sorted(records, key=lambda item: str(item["path"])),
    }
    (TARGET / "GOLDEN_BASELINE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (TARGET / "IMMUTABLE.lock").write_text("APPROVED GOLDEN BASELINE — DO NOT MODIFY\n", encoding="utf-8")
    print(f"GOLDEN_BASELINE_CREATED files={len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
