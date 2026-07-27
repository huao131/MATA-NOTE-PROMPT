import unittest
from ._support import fixture
from mata_p0.errors import StopAndReport
from mata_p1.gate_register import validate_gate_register
class GateRegisterTests(unittest.TestCase):
    def test_p1_gate_01_six_complete(self): self.assertEqual(len(validate_gate_register(fixture("TEST_SIX_GATES_COMPLETE.json"))),6)
    def test_p1_gate_02_order(self):
        with self.assertRaises(StopAndReport): validate_gate_register(fixture("TEST_GATE_ORDER.json"))
    def test_p1_gate_03_fields(self):
        with self.assertRaises(StopAndReport): validate_gate_register(fixture("TEST_GATE_AUDIT_FIELDS.json"))
    def test_p1_gate_04_codex_cannot_pass(self):
        with self.assertRaises(StopAndReport): validate_gate_register(fixture("TEST_CODEX_GATE_PASS_ATTEMPT.json"))

    def test_p1_gate_03_pass_requires_verified_evidence(self):
        with self.assertRaises(StopAndReport):
            validate_gate_register(fixture("TEST_GATE_PASS_NON_VERIFIED.json"))

    def test_p1_gate_03_pass_requires_dependency_pass(self):
        with self.assertRaises(StopAndReport):
            validate_gate_register(
                fixture("TEST_GATE_PASS_DEPENDENCY_NOT_PASS.json")
            )

    def test_p1_gate_02_predecessor_must_pass(self):
        with self.assertRaises(StopAndReport):
            validate_gate_register(fixture("TEST_GATE_PREDECESSOR_NOT_PASS.json"))

    def test_p1_gate_03_non_mapping_is_structured_stop(self):
        records = fixture("TEST_SIX_GATES_COMPLETE.json")
        records[2] = "not-a-mapping"
        with self.assertRaises(StopAndReport):
            validate_gate_register(records)
