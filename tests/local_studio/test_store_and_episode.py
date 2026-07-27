from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mata_studio.app import StudioApp
from mata_studio.errors import StudioError
from mata_studio.store import ProjectStore
from tests.local_studio._support import brief


class StoreEpisodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = StudioApp(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_database_initializes(self):
        self.assertTrue((Path(self.temp.name) / "studio.db").is_file())

    def test_series_unique(self):
        self.app.store.create_series("S1", "系列")
        with self.assertRaises(StudioError):
            self.app.store.create_series("S1", "系列")

    def test_episode_starts_awaiting_creative(self):
        episode = self.app.create_episode(brief())
        self.assertEqual(episode["production_state"], "AWAITING_CREATIVE_INPUT")
        self.assertEqual(self.app.store.artifacts(episode["episode_id"]), [])

    def test_episode_has_six_pending_gates(self):
        self.app.create_episode(brief())
        gates = self.app.store.gates("TEST_LOCAL_STUDIO_MVP")
        self.assertEqual(len(gates), 6)
        self.assertEqual({item["gate_status"] for item in gates}, {"PENDING"})

    def test_duplicate_episode_blocked(self):
        self.app.create_episode(brief())
        with self.assertRaises(StudioError):
            self.app.create_episode(brief())

    def test_manifest_export(self):
        self.app.create_episode(brief())
        result = self.app.store.export_manifest()
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(len(result["episodes"]), 1)

    def test_backup(self):
        target = Path(self.temp.name) / "backup" / "studio.db"
        self.app.store.backup(target)
        self.assertTrue(target.is_file())

    def test_series_foreign_key(self):
        value = brief()
        value["series_id"] = "MISSING"
        self.app.store.create_series("S1", "系列")
        with self.assertRaises(StudioError):
            self.app.create_episode(value)

    def test_patch_uses_allowlist(self):
        self.app.create_episode(brief())
        with self.assertRaises(StudioError):
            self.app.store.update_episode("TEST_LOCAL_STUDIO_MVP", {"approved_by": "CODEX"})
