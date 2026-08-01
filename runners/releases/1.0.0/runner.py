#!/usr/bin/env python3
"""Approved, side-effect-free runner for the bridge connection test."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--output-manifest", required=True)
    args = parser.parse_args()
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    manifest = {
        "request_id": request["request_id"],
        "episode_id": request["episode_id"],
        "runner_version": "1.0.0",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "result": "CONNECTION_TEST_SUCCESS" if request["request_type"] == "connection_test" else "RUNNER_READY",
        "generated_assets": [],
    }
    Path(args.output_manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(manifest["result"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
