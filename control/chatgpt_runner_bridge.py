#!/usr/bin/env python3
"""Fixed entry point: validates and launches only the approved Current Release."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_VERSION = "1.0.0"
STATE_DIR = ROOT / "control" / "state"
LOG_DIR = ROOT / "control" / "logs"
SCHEMA_PATH = ROOT / "control" / "schemas" / "episode_request.schema.json"
RELEASE_PATH = ROOT / "runners" / "CURRENT_RELEASE.json"


class BridgeError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def version_at_least(actual: str, required: str) -> bool:
    def parts(value: str) -> tuple[int, ...]:
        return tuple(int(part) for part in value.split("."))
    return parts(actual) >= parts(required)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ffmpeg_command() -> str | None:
    """Prefer a portable project binary, then fall back to the system PATH."""
    bundled = ROOT / "tools" / "ffmpeg" / ("ffmpeg.exe" if sys.platform == "win32" else "ffmpeg")
    return str(bundled) if bundled.is_file() else shutil.which("ffmpeg")


def load_release() -> tuple[dict[str, Any], Path]:
    try:
        release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BridgeError(f"CURRENT_RELEASE_INVALID: {error}") from error
    required = {"runner_version", "runner_path", "status", "sha256", "released_at", "minimum_bridge_version"}
    missing = sorted(required - release.keys())
    if missing:
        raise BridgeError(f"CURRENT_RELEASE_MISSING_FIELDS: {', '.join(missing)}")
    if release["status"] != "APPROVED":
        raise BridgeError(f"CURRENT_RELEASE_NOT_APPROVED: {release['status']}")
    if not version_at_least(BRIDGE_VERSION, str(release["minimum_bridge_version"])):
        raise BridgeError("BRIDGE_VERSION_TOO_OLD")
    runner = (ROOT / str(release["runner_path"])).resolve()
    approved_root = (ROOT / "runners" / "releases").resolve()
    if approved_root not in runner.parents or not runner.is_file():
        raise BridgeError("RUNNER_PATH_INVALID")
    if sha256(runner) != release["sha256"]:
        raise BridgeError("RUNNER_SHA256_MISMATCH")
    return release, runner


def validate_request(request: Any) -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise BridgeError("REQUEST_SCHEMA_INVALID: request must be an object")
    allowed = set(schema["properties"])
    unknown = set(request) - allowed
    missing = set(schema["required"]) - set(request)
    if unknown or missing or not isinstance(request.get("request_id"), str) or not request["request_id"].replace("_", "").replace("-", "").isalnum() or len(request["request_id"]) < 3:
        raise BridgeError("REQUEST_SCHEMA_INVALID")
    if request.get("request_type") not in {"connection_test", "episode"} or not isinstance(request.get("episode_id"), str) or not request["episode_id"]:
        raise BridgeError("REQUEST_SCHEMA_INVALID")
    if request["request_type"] == "connection_test" and request["episode_id"] != "CONNECTION_TEST":
        raise BridgeError("REQUEST_SCHEMA_INVALID")
    if "payload" in request and not isinstance(request["payload"], dict):
        raise BridgeError("REQUEST_SCHEMA_INVALID")
    return request


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def run(request: dict[str, Any]) -> dict[str, Any]:
    release, runner = load_release()
    request = validate_request(request)
    if request["request_type"] == "connection_test":
        ffmpeg = ffmpeg_command()
        if not ffmpeg:
            raise BridgeError("FFMPEG_NOT_FOUND")
        python_version = subprocess.run([sys.executable, "--version"], capture_output=True, text=True, check=False)
        if python_version.returncode != 0:
            raise BridgeError("PYTHON_NOT_AVAILABLE")
        ffmpeg_version = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True, check=False)
        if ffmpeg_version.returncode != 0:
            raise BridgeError("FFMPEG_NOT_AVAILABLE")

    run_id = f"{request['request_id']}-{uuid.uuid4().hex[:8]}"
    request_path = STATE_DIR / f"{run_id}.request.json"
    state_path = STATE_DIR / f"{run_id}.state.json"
    manifest_path = STATE_DIR / f"{run_id}.manifest.json"
    log_path = LOG_DIR / f"{run_id}.log"
    locked = {"runner_version": release["runner_version"], "runner_path": release["runner_path"], "runner_sha256": release["sha256"]}
    write_json(request_path, request)
    state = {"run_id": run_id, "request_id": request["request_id"], "episode_id": request["episode_id"], "status": "RUNNING", "started_at": now(), "locked_release": locked}
    write_json(state_path, state)
    command = [sys.executable, str(runner), "--request", str(request_path), "--output-manifest", str(manifest_path)]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("COMMAND: " + " ".join(command) + "\nSTDOUT:\n" + completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8")
    result = "BLOCKED" if completed.returncode else "SUCCESS"
    state.update({"status": result, "finished_at": now(), "exit_code": completed.returncode, "log_path": str(log_path.relative_to(ROOT)), "output_manifest": str(manifest_path.relative_to(ROOT))})
    write_json(state_path, state)
    return {"result": "CONNECTION_TEST_SUCCESS" if completed.returncode == 0 and request["request_type"] == "connection_test" else result, "exit_code": completed.returncode, "log_path": state["log_path"], "output_manifest": state["output_manifest"], "state_path": str(state_path.relative_to(ROOT)), "locked_release": locked}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, help="Path to an Episode Request JSON file")
    args = parser.parse_args()
    try:
        outcome = run(json.loads(Path(args.request).read_text(encoding="utf-8")))
        print(json.dumps(outcome, ensure_ascii=False))
        return 0
    except (BridgeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"result": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
