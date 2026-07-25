#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: build_editing_manifest.py episodes/<episode>", file=sys.stderr)
        return 2
    ep = Path(sys.argv[1])
    out = ep/"editing"/"EDITING_MANIFEST.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("# EDITING MANIFEST\n\n## Approved Segment Order\n\n## Timing\n\n## Voiceover\n\n## Subtitle / SRT\n\n## Logo & CTA\n\n## BGM / SFX\n\n## Transitions\n\n## Final QC\n", encoding="utf-8")
    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
