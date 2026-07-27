import unittest
from ._support import fixture
from mata_p0.errors import StopAndReport
from mata_p1.production_state import validate_state_proposal
class ProductionStateTests(unittest.TestCase):
    def test_p1_state_01_verified(self): self.assertTrue(validate_state_proposal(fixture("TEST_VERIFIED_CANONICAL_CANDIDATE.json"))["canonical_candidate"])
    def test_p1_state_02_non_verified_stops(self):
        with self.assertRaises(StopAndReport): validate_state_proposal(fixture("TEST_NON_VERIFIED_STATE.json"))
    def test_p1_state_03_segment_does_not_promote(self):
        with self.assertRaises(StopAndReport): validate_state_proposal(fixture("TEST_SEGMENT_READY.json"))
    def test_p1_state_04_dependency_blocks(self):
        r=validate_state_proposal(fixture("TEST_DEPENDENCY_NOT_PASS.json")); self.assertFalse(r["canonical_candidate"])
