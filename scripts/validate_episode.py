#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

REQUIRED = ["EPISODE_MASTER.md", "PRODUCTION_STATE.json", "ASSET_INDEX.json", "STORYBOARD_MASTER.md", "PRODUCTION_LOG.md"]
VALID_STATES = {"NEW_EPISODE","BRIEF_REVIEW","CREATIVE_GATE","STORY_DEVELOPMENT","STORY_VISUAL_GATE","KEYFRAME_READY","KEYFRAME_GENERATING","QC_WAITING","ASSET_UPLOADING","NEXT_KEYFRAME","KEYFRAME_LOCKED","FLOW_PACKAGE_READY","FLOW_GENERATION","FLOW_QC","PRODUCTION_LOCKED","EDITING_PACKAGE_READY","FINAL_QC","FINAL_APPROVED","EPISODE_CLOSED"}

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_episode.py episodes/<episode>", file=sys.stderr)
        return 2
    ep = Path(sys.argv[1])
    errors = [f"Missing {n}" for n in REQUIRED if not (ep/n).exists()]
    if not errors:
        state = json.loads((ep/"PRODUCTION_STATE.json").read_text(encoding="utf-8"))
        if state.get("runtime_state") not in VALID_STATES:
            errors.append(f"Invalid runtime_state: {state.get('runtime_state')}")
        if state.get("runtime_state") == "QC_WAITING" and not state.get("current_keyframe"):
            errors.append("QC_WAITING requires current_keyframe")
        assets = json.loads((ep/"ASSET_INDEX.json").read_text(encoding="utf-8"))
        if assets.get("episode_id") != state.get("episode_id"):
            errors.append("Episode ID mismatch between state and asset index")
    if errors:
        print("VALIDATION FAIL")
        for e in errors: print(f"- {e}")
        return 1
    print("VALIDATION PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
