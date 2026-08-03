from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "runners" / "releases" / "2.0.0" / "history_today_production_runner.py"
SPEC = importlib.util.spec_from_file_location("history_today_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(runner)


class HistoryTodayRunnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.request = {
            "request_id": "history-001", "request_type": "episode", "episode_id": "history-20260801",
            "payload": {"series": "history_today", "episode_date": "2026-08-01", "stage": "topic_selection",
                        "approved_topic_id": None, "flow_asset_ready": False, "subtitle_mode": "zh_tw_en",
                        "delivery_mode": "onedrive", "delivery_root": str(self.root / "delivery")},
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def facts(_day):
        return [{"topic_id": "event-20260801-01", "type": "event", "title": "A historic event", "summary": "A verified fact.", "source_url": "https://example.test", "story_score": 95, "visual_feasibility": "REVIEW_REQUIRED"}]

    def test_topic_selection_waits_for_explicit_approval(self):
        with patch.object(runner, "fetch_candidates", self.facts):
            manifest = runner.run_topic_selection(self.request)
        self.assertEqual(manifest["status"], "WAITING_FOR_TOPIC_APPROVAL")
        self.assertEqual(manifest["completed_stages"], ["TOPIC_SELECTION"])
        self.assertTrue(Path(manifest["topic_candidates_path"]).is_file())
        self.assertNotIn("ANNE_FRANK", json.dumps(manifest))

    def test_production_requires_approved_topic(self):
        self.request["payload"]["stage"] = "production"
        manifest = runner.run_production(self.request, None)
        self.assertEqual(manifest["status"], "BLOCKED")
        self.assertEqual(manifest["last_error"], "APPROVED_TOPIC_ID_REQUIRED")

    def test_waiting_flow_resumes_without_replaying_completed_stages(self):
        self.request["payload"].update({"stage": "production", "approved_topic_id": "event-20260801-01"})
        waiting = runner.run_production(self.request, None)
        self.assertEqual(waiting["status"], "WAITING_FOR_FLOW_ASSET")
        self.request["payload"].update({"stage": "resume", "flow_asset_ready": True})
        resumed = runner.run_production(self.request, waiting)
        self.assertEqual(resumed["status"], "BLOCKED")
        self.assertEqual(resumed["completed_stages"].count("RESEARCH_AND_FACT_CHECK"), 1)
        self.assertIn("REAL_DELIVERABLES_REQUIRED", resumed["last_error"])

    def test_no_missing_media_can_be_success(self):
        self.request["payload"].update({"stage": "production", "approved_topic_id": "generic-topic", "flow_asset_ready": True})
        manifest = runner.run_production(self.request, None)
        self.assertNotEqual(manifest["status"], "SUCCESS")
        self.assertIn("MASTER_NO_MAIN_SUBTITLE.mp4", manifest["last_error"])


if __name__ == "__main__":
    unittest.main()
