from __future__ import annotations

import tempfile
import unittest

from mata_studio.app import StudioApp
from mata_studio.drive import DriveAdapter, MockDriveTransport
from tests.local_studio._support import artifact, brief


class LocalStudioEndToEndTests(unittest.TestCase):
    def test_complete_mock_contract_path(self):
        root = {"id": "canonical", "name": "MATA AI 原創影片製片系統 V2", "parents": ["outside"]}
        video_library = {"id": "video-library", "name": "02_原創影片資料庫", "parents": ["canonical"]}
        transport = MockDriveTransport({"canonical": root, "video-library": video_library})
        registry = {
            "MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2": {
                "google_drive_folder_id": "canonical", "verification_status": "VERIFIED"
            }
        }
        with tempfile.TemporaryDirectory() as temp:
            app = StudioApp(temp, DriveAdapter(registry, transport))
            episode = app.create_episode(brief())
            self.assertEqual(episode["production_state"], "AWAITING_CREATIVE_INPUT")

            for index, kind in enumerate(
                ("EPISODE_BRIEF", "AUDIENCE_INSIGHT", "HOOK_STRATEGY", "CREATIVE_CANDIDATE"),
                start=1,
            ):
                app.submissions.submit(
                    episode["episode_id"], artifact(kind, f"V1.{index}")
                )
            app.gates.submit(episode["episode_id"], "creative_lock", "V1.4")
            approved = app.gates.decide(
                episode["episode_id"], "creative_lock", "PASS",
                {"approver": "Mata老師", "artifact_version": "V1.4", "evidence": "TEST_SCOPE 人工驗收", "comment": "E2E"},
            )
            self.assertEqual(approved["gate_status"], "PASS")

            for index, kind in enumerate(
                ("STORY_TREATMENT", "STORYBOARD", "TIMELINE", "VOICEOVER", "SRT_MANIFEST", "KEYFRAME_DEFINITION"),
                start=5,
            ):
                app.submissions.submit(episode["episode_id"], artifact(kind, f"V1.{index}"))

            keyframes = app.drive.ensure_child("07_Keyframes", "video-library", True)
            uploaded = app.drive.upload("TEST_KEYFRAME.png", keyframes["id"], b"test-image", "image/png")
            asset = app.assets.register(
                episode["episode_id"],
                {
                    "asset_id": "TEST_ASSET_KEYFRAME_001", "version": "V1.0",
                    "lifecycle_status": "DRAFT", "drive_file_id": uploaded["id"],
                    "drive_folder_id": keyframes["id"], "mime_type": "image/png",
                    "file_size": uploaded["size"], "web_view_link": uploaded["webViewLink"],
                    "exact_asset": False,
                },
            )
            self.assertEqual(asset["drive_file_id"], uploaded["id"])
            self.assertEqual(app.handoff.export(episode["episode_id"], "flow-package")["status"], "CANDIDATE")
            self.assertEqual(app.handoff.export(episode["episode_id"], "editing-package")["status"], "CANDIDATE")
            self.assertEqual(app.drive.status()["status"], "CONNECTED")
