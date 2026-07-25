from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "system" / "protection" / "V1.0_PROTECTED_FILES.sha256"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    failed = False
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        actual = ROOT / relative
        if not actual.is_file() or digest(actual) != expected:
            print(f"FAIL {relative}")
            failed = True
    if failed:
        return 1
    print("V1.0 PROTECTION PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
