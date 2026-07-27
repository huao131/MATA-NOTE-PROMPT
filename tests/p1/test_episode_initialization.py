from __future__ import annotations
import json, unittest
from ._support import ROOT, fixture
from mata_p0.errors import StopAndReport
from mata_p1.episode_initialization import validate_episode_initialization_plan
class EpisodeInitializationTests(unittest.TestCase):
    def test_p1_epi_01_schema_valid(self):
        record=fixture("TEST_EPISODE_INITIALIZATION_VALID.json")
        self.assertEqual(validate_episode_initialization_plan(record),record)
        json.loads((ROOT/"schemas/p1/episode_initialization.schema.json").read_text(encoding="utf-8"))
    def test_p1_epi_02_test_scope_isolated(self):
        record=fixture("TEST_EPISODE_SCOPE_ISOLATION.json")
        self.assertEqual(validate_episode_initialization_plan(record),record)
    def test_p1_epi_03_formal_episode_write_stops(self):
        with self.assertRaises(StopAndReport):
            validate_episode_initialization_plan(fixture("TEST_FORMAL_EPISODE_WRITE_ATTEMPT.json"))
if __name__=="__main__": unittest.main()
