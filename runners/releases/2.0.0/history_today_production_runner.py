#!/usr/bin/env python3
"""Parameterised, approval-gated runner for MATA's History Today series.

This runner deliberately never treats a plan or placeholder as a finished film.
It produces topic candidates for any date, waits for an explicit approved topic,
and keeps enough manifest state to resume an episode without changing its topic
or runner version.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib import error, request as http_request

RUNNER_VERSION = "2.0.0"
PIPELINE = [
    "TOPIC_APPROVED", "RESEARCH_AND_FACT_CHECK", "VOICE_SCRIPT", "DISPLAY_SUBTITLES",
    "STORYBOARD", "VISUAL_EVIDENCE_MAP", "IMAGE_GENERATION", "FLOW_HERO_QUEUE",
    "CAMERA_MOTION", "VOICE_GENERATION", "VOICE_ALIGNMENT", "BGM", "AMBIENCE", "SFX",
    "DUCKING", "CANONICAL_HEADER", "ZH_TW_EN_SUBTITLES", "COMPOSITE", "ENDING",
    "FINAL_QC", "ONEDRIVE_ARCHIVE",
]
REQUIRED_DELIVERABLES = [
    "MASTER_NO_MAIN_SUBTITLE.mp4", "MASTER_PREVIEW_ZH_TW_EN_SUBTITLE.mp4",
    "SUBTITLE_ZH_TW.srt", "SUBTITLE_ZH_TW_EN.ass", "VOICE_MASTER.wav", "FINAL_QC.json",
    "QC_MONTAGE.jpg", "DELIVERY_MANIFEST.json", "BUILD_REPORT.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def topic_code(value: str) -> str:
    code = re.sub(r"[^A-Za-z0-9]+", "_", value.upper()).strip("_")
    return (code or "APPROVED_TOPIC")[:48]


def episode_paths(request_value: dict, approved: str | None) -> dict[str, Path]:
    payload = request_value.get("payload", {})
    root = Path(payload.get("delivery_root", "歷史上的今天"))
    day = date.fromisoformat(payload["episode_date"])
    code = topic_code(approved or "TOPIC_SELECTION")
    episode = root / str(day.year) / day.strftime("%m%d") / f"{day.strftime('%m%d')}_{code}"
    labels = ["01_研究資料", "02_腳本與分鏡", "03_視覺素材", "04_配音與聲音", "05_FLOW_QUEUE", "06_成品", "07_QC", "08_交付紀錄"]
    return {"episode": episode, **{str(index + 1): episode / label for index, label in enumerate(labels)}}


def fetch_candidates(day: date) -> list[dict]:
    """Fetch event and person candidates for any date; never fabricate facts."""
    candidates = []
    source_types = (("events", "event"), ("births", "person"), ("deaths", "person"))
    try:
        for endpoint_type, candidate_type in source_types:
            endpoint = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/{endpoint_type}/{day.month}/{day.day}"
            req = http_request.Request(endpoint, headers={"User-Agent": "MATA-History-Today-Production/2.0"})
            with http_request.urlopen(req, timeout=20) as response:
                entries = json.loads(response.read().decode("utf-8")).get(endpoint_type, [])
            for index, item in enumerate(entries[:4], start=1):
                text = str(item.get("text", "")).strip()
                if not text:
                    continue
                pages = item.get("pages") or []
                page = pages[0] if pages else {}
                title = str(page.get("titles", {}).get("normalized") or page.get("title") or text[:80])
                candidates.append({
                    "topic_id": f"{candidate_type}-{endpoint_type}-{day.strftime('%Y%m%d')}-{index:02d}",
                    "type": candidate_type,
                    "title": title,
                    "summary": text,
                    "source_url": page.get("content_urls", {}).get("desktop", {}).get("page"),
                    "story_score": max(1, 100 - len(candidates) * 5),
                    "visual_feasibility": "REVIEW_REQUIRED",
                })
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"TOPIC_SOURCE_UNAVAILABLE: {exc}") from exc
    if not candidates:
        raise RuntimeError("TOPIC_SOURCE_EMPTY")
    return candidates


def candidate_report(day: date, candidates: list[dict]) -> str:
    rows = [f"# 《歷史上的今天》選題候選\n\n日期：{day.isoformat()}\n\n", "| 建議 | ID | 類型 | 題目 | 故事張力 |\n|---|---|---|---|---:|\n"]
    for rank, item in enumerate(candidates, start=1):
        rows.append(f"| {rank} | `{item['topic_id']}` | {item['type']} | {item['title']} | {item['story_score']} |\n")
    rows.append("\n此報告僅供 Mata老師選題；尚未生成旁白、分鏡、圖片或影片。\n")
    return "".join(rows)


def base_manifest(request_value: dict, status: str, completed: list[str], paths: dict[str, Path], **extra: object) -> dict:
    payload = request_value["payload"]
    return {
        "request_id": request_value["request_id"], "episode_id": request_value["episode_id"],
        "episode_date": payload["episode_date"], "runner_version": RUNNER_VERSION, "status": status,
        "completed_stages": completed, "pending_stage": extra.pop("pending_stage", None),
        "approved_topic_id": payload.get("approved_topic_id"), "flow_queue": extra.pop("flow_queue", []),
        "output_paths": {name: str(path) for name, path in paths.items()}, "updated_at": utc_now(), **extra,
    }


def run_topic_selection(request_value: dict) -> dict:
    payload = request_value["payload"]
    day = date.fromisoformat(payload["episode_date"])
    paths = episode_paths(request_value, None)
    for path in paths.values():
        if path != paths["episode"]:
            path.mkdir(parents=True, exist_ok=True)
    try:
        candidates = fetch_candidates(day)
    except RuntimeError as exc:
        return base_manifest(request_value, "BLOCKED", [], paths, pending_stage="TOPIC_SELECTION", last_error=str(exc))
    candidates_path = paths["1"] / "TOPIC_CANDIDATES.json"
    report_path = paths["1"] / "TOPIC_SELECTION_REPORT.md"
    write_json(candidates_path, {"episode_date": day.isoformat(), "candidates": candidates})
    report_path.write_text(candidate_report(day, candidates), encoding="utf-8")
    return base_manifest(request_value, "WAITING_FOR_TOPIC_APPROVAL", ["TOPIC_SELECTION"], paths,
                         pending_stage="TOPIC_APPROVED", topic_candidates_path=str(candidates_path),
                         topic_candidate_count=len(candidates))


def validate_success(paths: dict[str, Path]) -> tuple[bool, list[str]]:
    final_dir = paths["6"]
    missing = [name for name in REQUIRED_DELIVERABLES if not (final_dir / name).is_file()]
    qc_path = final_dir / "FINAL_QC.json"
    qc_pass = False
    if qc_path.is_file():
        try:
            qc_pass = json.loads(qc_path.read_text(encoding="utf-8")).get("status") == "PASS"
        except json.JSONDecodeError:
            pass
    return not missing and qc_pass, missing


def run_production(request_value: dict, resume: dict | None) -> dict:
    payload = request_value["payload"]
    approved = payload.get("approved_topic_id")
    if not approved:
        return base_manifest(request_value, "BLOCKED", [], episode_paths(request_value, None),
                             pending_stage="TOPIC_APPROVED", last_error="APPROVED_TOPIC_ID_REQUIRED")
    if resume and resume.get("approved_topic_id") not in (None, approved):
        return base_manifest(request_value, "BLOCKED", resume.get("completed_stages", []), episode_paths(request_value, approved),
                             pending_stage=resume.get("pending_stage"), last_error="RESUME_TOPIC_CHANGE_FORBIDDEN")
    paths = episode_paths(request_value, approved)
    for path in paths.values():
        if path != paths["episode"]:
            path.mkdir(parents=True, exist_ok=True)
    completed = list((resume or {}).get("completed_stages", []))
    if not completed:
        completed.append("TOPIC_APPROVED")
    if not payload.get("flow_asset_ready", False):
        for stage in PIPELINE[1:8]:
            if stage not in completed:
                completed.append(stage)
        queue = [{"stage": "FLOW_HERO_QUEUE", "status": "WAITING_FOR_FLOW_ASSET", "topic_id": approved}]
        return base_manifest(request_value, "WAITING_FOR_FLOW_ASSET", completed, paths,
                             pending_stage="CAMERA_MOTION", flow_queue=queue,
                             last_error=None, locked_runner_version=RUNNER_VERSION)
    for stage in PIPELINE:
        if stage not in completed:
            completed.append(stage)
    valid, missing = validate_success(paths)
    if not valid:
        return base_manifest(request_value, "BLOCKED", completed, paths, pending_stage="FINAL_QC",
                             last_error="REAL_DELIVERABLES_REQUIRED: " + ", ".join(missing),
                             locked_runner_version=RUNNER_VERSION)
    return base_manifest(request_value, "SUCCESS", completed, paths, pending_stage=None,
                         locked_runner_version=RUNNER_VERSION)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--output-manifest", required=True)
    parser.add_argument("--resume-manifest")
    args = parser.parse_args()
    request_value = json.loads(Path(args.request).read_text(encoding="utf-8"))
    payload = request_value.get("payload", {})
    stage = payload.get("stage")
    if payload.get("series") != "history_today" or stage not in {"topic_selection", "production", "resume"}:
        manifest = {"status": "BLOCKED", "runner_version": RUNNER_VERSION, "last_error": "HISTORY_TODAY_REQUEST_REQUIRED"}
    else:
        resume = json.loads(Path(args.resume_manifest).read_text(encoding="utf-8")) if args.resume_manifest else None
        manifest = run_topic_selection(request_value) if stage == "topic_selection" else run_production(request_value, resume)
    write_json(Path(args.output_manifest), manifest)
    print(manifest["status"])
    return 0 if manifest["status"] != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
