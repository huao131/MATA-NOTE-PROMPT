from __future__ import annotations

import tempfile
import unittest

from mata_studio.app import StudioApp
from mata_studio.drive import DriveAdapter, MockDriveTransport
from mata_studio.errors import StudioError
from tests.local_studio._support import artifact, brief


class DriveHandoffTests(unittest.TestCase):
    def setUp(self):
        self.root = {"id": "root-id", "name": "MATA", "parents": ["outside"]}
        self.transport = MockDriveTransport({"root-id": self.root, "folder-a": {"id": "folder-a", "parents": ["root-id"]}})
        self.registry = {"MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2": {"google_drive_folder_id": "root-id", "verification_status": "VERIFIED"}}
        self.drive = DriveAdapter(self.registry, self.transport)

    def test_not_connected_is_explicit(self):
        self.assertEqual(DriveAdapter({}).status()["status"], "NOT_CONNECTED")

    def test_root_upload_forbidden(self):
        with self.assertRaises(StudioError):
            self.drive.upload("x.json", "root", b"{}", "application/json")

    def test_unknown_folder_stops(self):
        with self.assertRaises(StudioError):
            self.drive.folder("missing")

    def test_parent_mismatch_stops(self):
        with self.assertRaises(StudioError):
            self.drive.folder("folder-a", "wrong")

    def test_create_requires_authorization(self):
        with self.assertRaises(StudioError):
            self.drive.ensure_child("EP003", "folder-a", False)

    def test_duplicate_folder_reused(self):
        created = self.drive.ensure_child("EP003", "folder-a", True)
        reused = self.drive.ensure_child("EP003", "folder-a", True)
        self.assertEqual(created["id"], reused["id"])

    def test_upload_roundtrip_ids(self):
        result = self.drive.upload("brief.json", "folder-a", b"{}", "application/json")
        self.assertTrue(result["id"])
        self.assertIn("folder-a", result["parents"])

    def test_canonical_root_verified(self):
        self.assertEqual(self.drive.validate_canonical_root()["id"], "root-id")

    def test_handoff_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            app = StudioApp(temp)
            app.create_episode(brief())
            with self.assertRaises(StudioError):
                app.handoff.export("TEST_LOCAL_STUDIO_MVP", "flow-package")

    def test_episode_summary_export(self):
        with tempfile.TemporaryDirectory() as temp:
            app = StudioApp(temp)
            app.create_episode(brief())
            app.submissions.submit("TEST_LOCAL_STUDIO_MVP", artifact("EPISODE_BRIEF"))
            result = app.handoff.export("TEST_LOCAL_STUDIO_MVP", "episode-summary")
            self.assertFalse(result["external_execution"])
