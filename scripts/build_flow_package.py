#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: build_flow_package.py episodes/<episode> S1", file=sys.stderr)
        return 2
    ep, segment = Path(sys.argv[1]), sys.argv[2]
    out = ep/"flow_packages"/f"{segment}_FLOW_PACKAGE.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    package = {
      "segment_id": segment,
      "story_task": "FILL_FROM_STORYBOARD",
      "input_images": [],
      "generation_mode": "FIRST_LAST_OR_MULTI_REFERENCE",
      "character_lock": [], "scene_lock": [], "props": [],
      "main_action": "", "secondary_motion": "", "camera_movement": "",
      "lighting_progression": "", "ending_state": "",
      "continuity_risk": [], "negative_constraints": [], "prompt": ""
    }
    out.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
