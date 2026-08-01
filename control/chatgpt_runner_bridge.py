#!/usr/bin/env python3
"""Controlled bridge from a transport request to an approved local runner."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_VERSION = "1.1.0"
VALID_STATES = {"RUNNING", "WAITING_FOR_FLOW_ASSET", "SUCCESS", "BLOCKED"}


class BridgeError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class Bridge:
    def __init__(self, root: Path = ROOT, release_path: Path | None = None) -> None:
        self.root = root.resolve()
        self.state_dir = self.root / "control" / "state"
        self.log_dir = self.root / "control" / "logs"
        self.schema_path = self.root / "control" / "schemas" / "episode_request.schema.json"
        self.release_path = release_path or Path(os.environ.get("MATA_CURRENT_RELEASE", self.root / "runners" / "CURRENT_RELEASE.json"))

    def load_release(self) -> tuple[dict[str, Any], Path]:
        try:
            release = json.loads(self.release_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise BridgeError(f"CURRENT_RELEASE_INVALID: {error}") from error
        required = {"runner_version", "runner_path", "status", "sha256", "released_at", "minimum_bridge_version"}
        if missing := sorted(required - release.keys()):
            raise BridgeError(f"CURRENT_RELEASE_MISSING_FIELDS: {', '.join(missing)}")
        if release["status"] != "APPROVED":
            raise BridgeError(f"CURRENT_RELEASE_NOT_APPROVED: {release['status']}")
        runner = (self.root / str(release["runner_path"])).resolve()
        approved_root = (self.root / "runners" / "releases").resolve()
        if approved_root not in runner.parents or not runner.is_file():
            raise BridgeError("RUNNER_PATH_INVALID")
        if hashlib.sha256(runner.read_bytes()).hexdigest() != release["sha256"]:
            raise BridgeError("RUNNER_SHA256_MISMATCH")
        return release, runner

    def validate_request(self, request: Any) -> dict[str, Any]:
        try:
            schema = json.loads(self.schema_path.read_text(encoding="utf-8"))
            errors = sorted(Draft202012Validator(schema).iter_errors(request), key=lambda item: list(item.path))
        except (OSError, json.JSONDecodeError) as error:
            raise BridgeError(f"REQUEST_SCHEMA_UNAVAILABLE: {error}") from error
        if errors:
            location = "/".join(map(str, errors[0].path)) or "$"
            raise BridgeError(f"REQUEST_SCHEMA_INVALID at {location}: {errors[0].message}")
        return request

    def _resume(self, request: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        resume_run_id = request.get("resume_run_id")
        if not resume_run_id:
            return None, None
        state_path = self.state_dir / f"{resume_run_id}.state.json"
        manifest_path = self.state_dir / f"{resume_run_id}.manifest.json"
        try:
            state, manifest = json.loads(state_path.read_text(encoding="utf-8")), json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise BridgeError(f"RESUME_STATE_INVALID: {error}") from error
        if state.get("status") != "WAITING_FOR_FLOW_ASSET" or state.get("episode_id") != request["episode_id"]:
            raise BridgeError("RESUME_NOT_ALLOWED")
        return state, manifest

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        request = self.validate_request(request)
        previous_state, previous_manifest = self._resume(request)
        release, runner = self.load_release()
        locked = previous_state["locked_release"] if previous_state else {"runner_version": release["runner_version"], "runner_path": release["runner_path"], "runner_sha256": release["sha256"]}
        if previous_state:
            runner = (self.root / locked["runner_path"]).resolve()
            if not runner.is_file() or hashlib.sha256(runner.read_bytes()).hexdigest() != locked["runner_sha256"]:
                raise BridgeError("LOCKED_RUNNER_UNAVAILABLE")
        run_id = f"{request['request_id']}-{uuid.uuid4().hex[:8]}"
        request_path, state_path = self.state_dir / f"{run_id}.request.json", self.state_dir / f"{run_id}.state.json"
        manifest_path, log_path = self.state_dir / f"{run_id}.manifest.json", self.log_dir / f"{run_id}.log"
        write_json(request_path, request)
        state = {"run_id": run_id, "request_id": request["request_id"], "episode_id": request["episode_id"], "status": "RUNNING", "started_at": now(), "locked_release": locked, "resumed_from": previous_state and previous_state["run_id"]}
        write_json(state_path, state)
        command = [sys.executable, str(runner), "--request", str(request_path), "--output-manifest", str(manifest_path)]
        if previous_manifest:
            command.extend(["--resume-manifest", str(self.state_dir / f"{previous_state['run_id']}.manifest.json")])
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text("COMMAND: " + " ".join(command) + "\nSTDOUT:\n" + completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8")
        status, error = "BLOCKED", None
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            candidate = manifest.get("status")
            if candidate not in VALID_STATES:
                error = f"MANIFEST_STATUS_INVALID: {candidate!r}"
            elif manifest.get("runner_version") != locked["runner_version"]:
                error = "MANIFEST_RUNNER_VERSION_MISMATCH"
            elif completed.returncode != 0 and candidate != "BLOCKED":
                error = "RUNNER_EXIT_NONZERO"
            else:
                status = candidate
        except (OSError, json.JSONDecodeError) as exc:
            error = f"MANIFEST_INVALID: {exc}"
        if error:
            status = "BLOCKED"
        state.update({"status": status, "finished_at": now(), "exit_code": completed.returncode, "log_path": str(log_path.relative_to(self.root)), "output_manifest": str(manifest_path.relative_to(self.root)), "error": error})
        write_json(state_path, state)
        result = "CONNECTION_TEST_SUCCESS" if request["request_type"] == "connection_test" and status == "SUCCESS" else status
        return {"result": result, "status": status, "exit_code": completed.returncode, "log_path": state["log_path"], "output_manifest": state["output_manifest"], "state_path": str(state_path.relative_to(self.root)), "locked_release": locked, "error": error}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--release-path", type=Path)
    args = parser.parse_args()
    try:
        outcome = Bridge(release_path=args.release_path).run(json.loads(Path(args.request).read_text(encoding="utf-8")))
        print(json.dumps(outcome, ensure_ascii=False))
        return 0 if outcome["status"] != "BLOCKED" else 1
    except (BridgeError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"result": "BLOCKED", "status": "BLOCKED", "error": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
