#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone

LEGAL = {
  ("QC_WAITING", "確認"): "KEYFRAME_GENERATING",
  ("QC_WAITING", "OK"): "QC_WAITING",
  ("QC_WAITING", "PASS"): "ASSET_UPLOADING",
  ("QC_WAITING", "通過"): "ASSET_UPLOADING",
  ("QC_WAITING", "APPROVED"): "NEXT_KEYFRAME",
  ("QC_WAITING", "Approved"): "NEXT_KEYFRAME",
  ("QC_WAITING", "3+4"): "ASSET_UPLOADING"
}

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: transition_state.py episodes/<episode> <command>", file=sys.stderr)
        return 2
    ep, command = Path(sys.argv[1]), sys.argv[2]
    path = ep/"PRODUCTION_STATE.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    key = (state.get("runtime_state"), command)
    if key not in LEGAL:
        print(f"ILLEGAL TRANSITION: {key}", file=sys.stderr)
        return 1
    state["runtime_state"] = LEGAL[key]
    state["next_action"] = "UPLOAD_AND_VERIFY_THEN_ADVANCE" if command == "3+4" else command
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(state["runtime_state"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
