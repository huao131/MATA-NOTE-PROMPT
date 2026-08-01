from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "control" / "chatgpt_runner_bridge.py"
REQUEST = ROOT / "control" / "requests" / "connection_test.json"
CURRENT_RELEASE = ROOT / "runners" / "CURRENT_RELEASE.json"


class BridgeSmokeTest(unittest.TestCase):
    def invoke(self, request: Path = REQUEST) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(BRIDGE), "--request", str(request)], cwd=ROOT, capture_output=True, text=True, check=False)

    def test_connection_test_succeeds(self) -> None:
        completed = self.invoke()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        outcome = json.loads(completed.stdout)
        self.assertEqual(outcome["result"], "CONNECTION_TEST_SUCCESS")
        self.assertEqual(outcome["exit_code"], 0)
        self.assertTrue((ROOT / outcome["log_path"]).is_file())
        self.assertTrue((ROOT / outcome["output_manifest"]).is_file())

    def test_rejects_unapproved_and_tampered_release(self) -> None:
        original = CURRENT_RELEASE.read_text(encoding="utf-8")
        release = json.loads(original)
        try:
            release["status"] = "CANDIDATE"
            CURRENT_RELEASE.write_text(json.dumps(release), encoding="utf-8")
            self.assertIn("CURRENT_RELEASE_NOT_APPROVED", self.invoke().stdout)
            release["status"] = "APPROVED"
            release["sha256"] = "0" * 64
            CURRENT_RELEASE.write_text(json.dumps(release), encoding="utf-8")
            self.assertIn("RUNNER_SHA256_MISMATCH", self.invoke().stdout)
        finally:
            CURRENT_RELEASE.write_text(original, encoding="utf-8")

    def test_next_run_reads_new_release_but_previous_lock_is_unchanged(self) -> None:
        original = CURRENT_RELEASE.read_text(encoding="utf-8")
        try:
            first = json.loads(self.invoke().stdout)
            release = json.loads(original)
            release["runner_version"] = "1.0.1-test"
            CURRENT_RELEASE.write_text(json.dumps(release), encoding="utf-8")
            second = json.loads(self.invoke().stdout)
            self.assertEqual(first["locked_release"]["runner_version"], "1.0.0")
            self.assertEqual(second["locked_release"]["runner_version"], "1.0.1-test")
        finally:
            CURRENT_RELEASE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
