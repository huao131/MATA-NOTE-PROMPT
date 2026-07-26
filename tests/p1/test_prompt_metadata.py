import unittest
from ._support import fixture
from mata_p0.errors import StopAndReport
from mata_p1.prompt_metadata import validate_prompt_metadata
class PromptTests(unittest.TestCase):
    def test_p1_prompt_01_inputs(self): self.assertTrue(validate_prompt_metadata(fixture("TEST_PROMPT_APPROVED_INPUTS.json"))["approved_input_refs"])
    def test_p1_prompt_02_refs(self): self.assertTrue(validate_prompt_metadata(fixture("TEST_PROMPT_EVIDENCE_VERSION_REFS.json"))["version_refs"])
    def test_p1_prompt_03_non_verified(self):
        with self.assertRaises(StopAndReport): validate_prompt_metadata(fixture("TEST_PROMPT_NON_VERIFIED.json"))
    def test_p1_prompt_04_no_flow(self):
        with self.assertRaises(StopAndReport): validate_prompt_metadata(fixture("TEST_PROMPT_FLOW_CONTROL_ATTEMPT.json"))
