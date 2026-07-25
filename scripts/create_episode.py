#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: create_episode.py EP03 產業名稱", file=sys.stderr)
        return 2
    episode_id, name = sys.argv[1], "_".join(sys.argv[2:])
    dst = ROOT / "episodes" / f"{episode_id}_{name}"
    if dst.exists():
        print(f"Episode already exists: {dst}", file=sys.stderr)
        return 1
    shutil.copytree(ROOT / "templates" / "episode", dst)
    state_path = dst / "PRODUCTION_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["episode_id"] = episode_id
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    asset_path = dst / "ASSET_INDEX.json"
    assets = json.loads(asset_path.read_text(encoding="utf-8"))
    assets["episode_id"] = episode_id
    asset_path.write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
    print(dst)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
