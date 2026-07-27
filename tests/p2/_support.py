from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def demo_brief() -> dict:
    return json.loads(
        (ROOT / "examples" / "p2" / "TEST_P2_WF_01_BRIEF.json").read_text(
            encoding="utf-8"
        )
    )
