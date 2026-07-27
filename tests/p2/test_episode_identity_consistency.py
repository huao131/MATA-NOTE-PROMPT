from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ._support import demo_brief  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p2.new_episode import (
    OUTPUT_FILES,
    build_candidate_package,
    run_workflow,
    validate_brief,
    validate_episode_identity,
)


def formal_brief() -> dict:
    brief = demo_brief()
    brief["episode_id"] = "EP003"
    return brief


class EpisodeIdentityConsistencyTests(unittest.TestCase):
    def package(self) -> dict:
        return build_candidate_package(formal_brief())

    def assert_identity_stop(self, package: dict, expected: str = "EP003"):
        with self.assertRaises(StopAndReport) as context:
            validate_episode_identity(package, expected)
        self.assertTrue(context.exception.violations)

    def test_positive_01_all_object_outputs_have_top_level_identity(self):
        package = self.package()
        for name, value in package.items():
            if isinstance(value, dict):
                with self.subTest(name=name):
                    self.assertEqual(value["episode_id"], "EP003")

    def test_positive_02_production_state_has_top_level_identity(self):
        self.assertEqual(self.package()[OUTPUT_FILES[5]]["episode_id"], "EP003")

    def test_positive_03_status_has_top_level_identity(self):
        self.assertEqual(self.package()[OUTPUT_FILES[7]]["episode_id"], "EP003")

    def test_positive_04_prompt_metadata_has_top_level_identity(self):
        self.assertEqual(self.package()[OUTPUT_FILES[8]]["episode_id"], "EP003")

    def test_positive_05_gate_register_remains_array(self):
        self.assertIsInstance(self.package()[OUTPUT_FILES[6]], list)

    def test_positive_06_all_gate_records_have_identity(self):
        gates = self.package()[OUTPUT_FILES[6]]
        self.assertTrue(gates)
        self.assertTrue(all(record.get("episode_id") for record in gates))

    def test_positive_07_all_gate_record_identities_match(self):
        gates = self.package()[OUTPUT_FILES[6]]
        self.assertTrue(all(record["episode_id"] == "EP003" for record in gates))

    def test_positive_08_all_outputs_pass_by_structure(self):
        result = validate_episode_identity(self.package(), "EP003")
        self.assertEqual(result["passed_output_count"], 12)

    def test_positive_09_manifest_records_both_identity_modes(self):
        identity = self.package()[OUTPUT_FILES[10]]["episode_identity_consistency"]
        modes = {item["identity_mode"] for item in identity["file_results"]}
        self.assertEqual(
            modes,
            {"TOP_LEVEL_OBJECT_IDENTITY", "RECORD_LEVEL_ARRAY_IDENTITY"},
        )

    def test_positive_10_validation_report_records_twelve_passes(self):
        identity = self.package()[OUTPUT_FILES[11]]["episode_identity_consistency"]
        self.assertEqual(identity["status"], "PASS")
        self.assertEqual(identity["output_count"], 12)
        self.assertEqual(identity["passed_output_count"], 12)

    def test_positive_11_every_proven_identity_is_ep003(self):
        package = self.package()
        for value in package.values():
            if isinstance(value, dict):
                self.assertEqual(value["episode_id"], "EP003")
            else:
                self.assertTrue(all(item["episode_id"] == "EP003" for item in value))

    def test_positive_12_v11_can_coexist_without_modifying_v10(self):
        with tempfile.TemporaryDirectory() as parent:
            v10 = Path(parent) / "P2_WF_01_V1.0"
            v10.mkdir()
            sentinel = v10 / "historical.json"
            sentinel.write_text('{"version":"V1.0"}', encoding="utf-8")
            before = sentinel.read_bytes()
            v11 = Path(parent) / "P2_WF_01_V1.1"
            run_workflow(formal_brief(), v11)
            self.assertEqual(sentinel.read_bytes(), before)
            self.assertEqual(len(list(v11.glob("*.json"))), 12)

    def test_negative_13_object_missing_top_level_identity(self):
        package = self.package()
        del package[OUTPUT_FILES[5]]["episode_id"]
        self.assert_identity_stop(package)

    def test_negative_14_nested_only_object_identity_is_rejected(self):
        package = self.package()
        del package[OUTPUT_FILES[7]]["episode_id"]
        package[OUTPUT_FILES[7]]["metadata"] = {"episode_id": "EP003"}
        self.assert_identity_stop(package)

    def test_negative_15_array_record_missing_identity(self):
        package = self.package()
        del package[OUTPUT_FILES[6]][0]["episode_id"]
        self.assert_identity_stop(package)

    def test_negative_16_array_record_mismatch(self):
        package = self.package()
        package[OUTPUT_FILES[6]][0]["episode_id"] = "EP004"
        self.assert_identity_stop(package)

    def test_negative_17_array_mixed_episode_ids(self):
        package = self.package()
        package[OUTPUT_FILES[6]][-1]["episode_id"] = "EP999"
        self.assert_identity_stop(package)

    def test_negative_18_empty_gate_array(self):
        package = self.package()
        package[OUTPUT_FILES[6]] = []
        self.assert_identity_stop(package)

    def test_negative_19_empty_episode_id(self):
        package = self.package()
        package[OUTPUT_FILES[8]]["episode_id"] = ""
        self.assert_identity_stop(package)

    def test_negative_20_illegal_episode_id(self):
        package = self.package()
        package[OUTPUT_FILES[8]]["episode_id"] = "EP03"
        self.assert_identity_stop(package)

    def test_negative_21_existing_v10_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as parent:
            v10 = Path(parent) / "P2_WF_01_V1.0"
            v10.mkdir()
            sentinel = v10 / "historical.json"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(StopAndReport):
                run_workflow(formal_brief(), v10)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_negative_22_existing_v11_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as parent:
            v11 = Path(parent) / "P2_WF_01_V1.1"
            run_workflow(formal_brief(), v11)
            before = {path.name: path.read_bytes() for path in v11.iterdir()}
            with self.assertRaises(StopAndReport):
                run_workflow(formal_brief(), v11)
            after = {path.name: path.read_bytes() for path in v11.iterdir()}
            self.assertEqual(after, before)

    def test_negative_23_identity_failure_leaves_no_partial_package(self):
        valid = self.package()
        invalid = copy.deepcopy(valid)
        del invalid[OUTPUT_FILES[5]]["episode_id"]
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "P2_WF_01_V1.1"
            with patch(
                "mata_p2.new_episode.build_candidate_package",
                return_value=invalid,
            ):
                with self.assertRaises(StopAndReport):
                    run_workflow(formal_brief(), output)
            self.assertFalse(output.exists())

    def test_negative_24_formal_status_injection_is_blocked(self):
        brief = formal_brief()
        brief["status"] = "APPROVED"
        with self.assertRaises(StopAndReport):
            validate_brief(brief)

    def test_negative_25_external_operation_is_blocked(self):
        brief = formal_brief()
        brief["drive_operation"] = "CREATE"
        with self.assertRaises(StopAndReport):
            validate_brief(brief)


if __name__ == "__main__":
    unittest.main()
