import unittest
from ._support import fixture
from mata_p0.errors import StopAndReport
from mata_p1.status_handling import validate_status
class StatusTests(unittest.TestCase):
    def test_p1_status_01_domains(self): self.assertEqual(validate_status(fixture("TEST_LIFECYCLE_QC_SEPARATION.json"))["qc_status"],"PASS")
    def test_p1_status_02_reference(self):
        with self.assertRaises(StopAndReport): validate_status(fixture("TEST_REJECTED_REFERENCE.json"))
    def test_p1_status_03_dependency(self):
        with self.assertRaises(StopAndReport): validate_status(fixture("TEST_REJECTED_DEPENDENCY.json"))
    def test_p1_status_04_final(self):
        with self.assertRaises(StopAndReport): validate_status(fixture("TEST_REJECTED_FINAL_ASSET.json"))
    def test_p1_status_05_exact(self):
        with self.assertRaises(StopAndReport): validate_status(fixture("TEST_EXACT_ASSET_REPLACEMENT.json"))
