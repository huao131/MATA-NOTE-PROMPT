from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
FIXTURES = ROOT / "tests" / "p1" / "fixtures"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))
