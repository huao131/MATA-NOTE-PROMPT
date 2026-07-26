import unittest
from ._support import fixture
from mata_p0.errors import StopAndReport
from mata_p1.handoff_manifest import validate_handoff_manifest
class HandoffTests(unittest.TestCase):
    def test_p1_handoff_01_fields(self): self.assertTrue(validate_handoff_manifest(fixture("TEST_HANDOFF_REQUIRED_FIELDS.json"))["handoff_id"])
    def test_p1_handoff_02_block(self):
        with self.assertRaises(StopAndReport): validate_handoff_manifest(fixture("TEST_HANDOFF_BLOCKED_DEPENDENCY.json"))
    def test_p1_handoff_03_rejected(self):
        with self.assertRaises(StopAndReport): validate_handoff_manifest(fixture("TEST_HANDOFF_REJECTED_INPUT.json"))
    def test_p1_handoff_04_exact(self):
        with self.assertRaises(StopAndReport): validate_handoff_manifest(fixture("TEST_HANDOFF_EXACT_ASSET.json"))
    def test_p1_handoff_05_no_flow(self):
        with self.assertRaises(StopAndReport): validate_handoff_manifest(fixture("TEST_HANDOFF_FLOW_EXECUTION_ATTEMPT.json"))
