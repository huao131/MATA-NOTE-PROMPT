from __future__ import annotations

import tempfile
import unittest

from mata_studio.app import StudioApp
from mata_studio.errors import StudioError
from tests.local_studio._support import artifact, brief


class SubmissionGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = StudioApp(self.temp.name)
        self.app.create_episode(brief())

    def tearDown(self):
        self.temp.cleanup()

    def test_chatgpt_candidate_import(self):
        item = self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact())
        self.assertEqual(item["artifact_type"], "AUDIENCE_INSIGHT")

    def test_duplicate_artifact_version_blocked(self):
        self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact())
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact())

    def test_identity_mismatch_blocked(self):
        value = artifact()
        value["episode_id"] = "TEST_OTHER"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_invalid_version_blocked(self):
        value = artifact()
        value["version"] = "latest"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_payload_cannot_approve(self):
        value = artifact()
        value["approval_status"] = "APPROVED"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_payload_cannot_lock(self):
        value = artifact()
        value["lock_status"] = "LOCKED"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_payload_cannot_name_approver(self):
        value = artifact()
        value["approved_by"] = "Mata"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_gate_requires_artifact(self):
        with self.assertRaises(StudioError):
            self.app.gates.submit("TEST_LOCAL_STUDIO_MVP", "creative_lock", "V1.0")

    def test_codex_cannot_approve_gate(self):
        self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact())
        self.app.gates.submit("TEST_LOCAL_STUDIO_MVP", "creative_lock", "V1.0")
        event = {"approver": "CODEX", "artifact_version": "V1.0", "evidence": "review", "comment": "pass"}
        with self.assertRaises(StudioError):
            self.app.gates.decide("TEST_LOCAL_STUDIO_MVP", "creative_lock", "PASS", event)

    def test_human_gate_event(self):
        self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact())
        self.app.gates.submit("TEST_LOCAL_STUDIO_MVP", "creative_lock", "V1.0")
        event = {"approver": "Mata老師", "artifact_version": "V1.0", "evidence": "人工審閱", "comment": "測試核准"}
        result = self.app.gates.decide("TEST_LOCAL_STUDIO_MVP", "creative_lock", "PASS", event)
        self.assertEqual(result["gate_status"], "PASS")

    def test_predecessor_gate_required(self):
        self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact("STORY_TREATMENT"))
        self.app.gates.submit("TEST_LOCAL_STUDIO_MVP", "story_lock", "V1.0")
        event = {"approver": "Mata老師", "artifact_version": "V1.0", "evidence": "人工審閱", "comment": "測試"}
        with self.assertRaises(StudioError):
            self.app.gates.decide("TEST_LOCAL_STUDIO_MVP", "story_lock", "PASS", event)

    def test_rejected_source_blocked(self):
        self.app.assets.register("TEST_LOCAL_STUDIO_MVP", {"asset_id": "A1", "version": "V1.0", "lifecycle_status": "REJECTED"})
        value = artifact()
        value["source_asset_ids"] = ["A1"]
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)

    def test_major_change_requires_dependency_recheck(self):
        value = artifact()
        value["change_class"] = "MAJOR"
        with self.assertRaises(StudioError):
            self.app.submissions.submit("TEST_LOCAL_STUDIO_MVP", value)
