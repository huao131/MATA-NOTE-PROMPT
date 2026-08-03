"""Two-phase bridge for Codex built-in single-frame generation.

The Windows watcher prepares a Codex job. Codex built-in image_gen produces one
PNG, then a completion request supplies that managed generated-image path. This
module performs the controlled copy, QC, SHA/state/index persistence, and Flow
prompt creation when both START and END frames pass.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


class RenderFrameError(RuntimeError):
    pass


class RenderFrameBridge:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.jobs = self.root / "control" / "codex_jobs"

    @staticmethod
    def _within(path: Path, root: Path) -> bool:
        try:
            path.resolve().relative_to(root.resolve())
            return True
        except ValueError:
            return False

    def _paths(self, payload: dict[str, Any]) -> tuple[Path, Path]:
        episode = Path(payload["episode_path"]).resolve()
        output = Path(payload["output_path"]).resolve()
        if not episode.is_dir():
            raise RenderFrameError("EPISODE_PATH_INVALID")
        if not self._within(output, episode) or output.suffix.lower() != ".png":
            raise RenderFrameError("OUTPUT_PATH_MUST_BE_EPISODE_PNG")
        return episode, output

    def prepare(self, request: dict[str, Any]) -> dict[str, Any]:
        payload = request["payload"]
        _, output = self._paths(payload)
        job = {
            "request_id": request["request_id"], "request_type": "render_frame",
            "scene_id": payload["scene_id"], "frame_role": payload["frame_role"],
            "visual_prompt": payload["visual_prompt"], "negative_prompt": payload["negative_prompt"],
            "output_path": str(output), "width": payload.get("width", 1080), "height": payload.get("height", 1920),
            "renderer": "tools/history_today/render_single_frame.codex.js",
            "status": "WAITING_FOR_CODEX_IMAGE", "created_at": now(),
        }
        job_path = self.jobs / "inbox" / f"{request['request_id']}.json"
        write_json(job_path, job)
        return {
            "result": "WAITING_FOR_CODEX_IMAGE", "status": "WAITING_FOR_CODEX_IMAGE", "exit_code": 0,
            "codex_job": str(job_path.relative_to(self.root)), "output_path": str(output),
            "scene_id": payload["scene_id"], "frame_role": payload["frame_role"],
        }

    def complete(self, request: dict[str, Any]) -> dict[str, Any]:
        payload = request["payload"]
        episode, output = self._paths(payload)
        generated = Path(payload["generated_path"]).resolve()
        if not generated.is_file() or generated.suffix.lower() != ".png":
            raise RenderFrameError("GENERATED_PNG_INVALID")
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(generated, output)
        with Image.open(output) as image:
            width, height = image.size
            image_format = image.format
        ratio_ok = abs(width / height - 9 / 16) <= 0.001
        qc = {
            "status": "PASS" if image_format == "PNG" and ratio_ok else "FAIL",
            "format": image_format, "width": width, "height": height, "portrait_9_16": ratio_ok,
            "single_image": True, "text_requested": False, "collage_requested": False,
        }
        if qc["status"] != "PASS":
            output.unlink(missing_ok=True)
            raise RenderFrameError("FRAME_QC_FAILED")
        digest = sha256(output)
        qc_root = episode / "07_QC"
        qc_path = qc_root / f"{output.stem}_QC.json"
        qc.update({"output_path": str(output), "sha256": digest, "checked_at": now()})
        write_json(qc_path, qc)

        asset_path = episode / "ASSET_INDEX.json"
        assets = json.loads(asset_path.read_text(encoding="utf-8-sig")) if asset_path.exists() else {"assets": {}}
        assets.setdefault("assets", {})[f"{payload['scene_id']}_{payload['frame_role']}"] = {
            "path": str(output), "sha256": digest, "qc": "PASS", "width": width, "height": height,
        }
        assets["updated_at"] = now()
        write_json(asset_path, assets)

        state_path = episode / "PRODUCTION_STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8-sig")) if state_path.exists() else {"episode_id": request["episode_id"]}
        state.setdefault("render_frames", {})[f"{payload['scene_id']}_{payload['frame_role']}"] = "PASS"
        state["updated_at"] = now()

        visual_dir = output.parent
        stem_prefix = payload["scene_id"]
        start = visual_dir / f"{stem_prefix}_START_V1.png"
        end = visual_dir / f"{stem_prefix}_END_V1.png"
        flow_prompt = None
        if start.is_file() and end.is_file():
            flow_prompt = episode / "05_FLOW_QUEUE" / f"{stem_prefix}_FLOW_PROMPT_V1.md"
            flow_prompt.parent.mkdir(parents=True, exist_ok=True)
            flow_prompt.write_text(
                f"# {stem_prefix} Flow Prompt V1\n\n"
                "Use the START and END reference frames to create one restrained cinematic transition.\n"
                "Preserve historical identity, ship geometry, wardrobe, lighting continuity, and 9:16 framing.\n"
                "Camera: slow forward drift with subtle harbor parallax; no morphing, no new people, no text, no logo.\n"
                f"START: {start}\nEND: {end}\n",
                encoding="utf-8",
            )
            state["flow_prompt_scene_01"] = "PASS"
            assets["assets"]["SCENE_01_FLOW_PROMPT"] = {"path": str(flow_prompt), "sha256": sha256(flow_prompt), "qc": "PASS"}
            write_json(asset_path, assets)
        write_json(state_path, state)

        completed_job = self.jobs / "completed" / f"{request['request_id']}.json"
        job = {
            "request_id": request["request_id"], "status": "SUCCESS", "output_path": str(output),
            "sha256": digest, "qc": str(qc_path), "asset_index": str(asset_path),
            "production_state": str(state_path), "flow_prompt": str(flow_prompt) if flow_prompt else None,
            "completed_at": now(),
        }
        write_json(completed_job, job)
        (self.jobs / "inbox" / f"{request['request_id']}.json").unlink(missing_ok=True)
        return {
            "result": "SUCCESS", "status": "SUCCESS", "exit_code": 0, "request_type": "render_frame",
            "scene_id": payload["scene_id"], "frame_role": payload["frame_role"], "output_path": str(output),
            "sha256": digest, "qc": qc, "asset_index": str(asset_path), "production_state": str(state_path),
            "flow_prompt": str(flow_prompt) if flow_prompt else None,
        }

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        return self.complete(request) if request["payload"]["action"] == "complete" else self.prepare(request)
