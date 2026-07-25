from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "episode_v1.1"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_id")
    parser.add_argument("title")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = ROOT / "episodes" / f"{args.episode_id}_{args.title}"
    if target.exists():
        parser.error(f"already exists: {target}")
    if args.dry_run:
        print(f"DRY RUN: would create {target}")
        return 0
    target.mkdir(parents=True)
    for item in TEMPLATE.iterdir():
        if item.is_file():
            (target / item.name).write_bytes(item.read_bytes())
    for name in ("prompts", "flow_packages", "editing"):
        (target / name).mkdir()
    print(f"Created {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
