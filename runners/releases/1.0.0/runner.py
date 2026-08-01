#!/usr/bin/env python3
"""Approved demonstration runner with explicit manifest state semantics."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True); parser.add_argument("--output-manifest", required=True)
    parser.add_argument("--resume-manifest")
    args = parser.parse_args()
    request = json.loads(Path(args.request).read_text(encoding="utf-8")); payload = request.get("payload", {})
    completed = []
    if args.resume_manifest:
        completed = json.loads(Path(args.resume_manifest).read_text(encoding="utf-8")).get("completed_stages", [])
    if request["request_type"] == "connection_test": status, completed = "SUCCESS", ["connection_test"]
    elif not payload.get("flow_asset_ready", False): status, completed = "WAITING_FOR_FLOW_ASSET", completed or ["preflight"]
    else: status, completed = "SUCCESS", completed + [stage for stage in ["preflight", "render", "manifest"] if stage not in completed]
    manifest = {"request_id": request["request_id"], "episode_id": request["episode_id"], "runner_version": "1.0.0", "status": status, "completed_at": datetime.now(timezone.utc).isoformat(), "completed_stages": completed, "generated_assets": []}
    Path(args.output_manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(status); return 0
if __name__ == "__main__": raise SystemExit(main())
