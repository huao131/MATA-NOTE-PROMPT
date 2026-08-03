from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class GoldenGovernanceTest(unittest.TestCase):
    def test_feature_flags_fail_closed(self) -> None:
        value = json.loads((ROOT / "config" / "history_today_feature_flags.json").read_text(encoding="utf-8"))
        self.assertTrue(value["defaults"])
        self.assertTrue(all(flag is False for flag in value["defaults"].values()))
        self.assertIs(value["defaults"]["flow_prompt_package_v2"], False)

    def test_flow_package_rc_is_complete_but_default_off(self) -> None:
        root = ROOT / "runners" / "release_candidates" / "2.1.0-rc.1" / "flow"
        schema = json.loads((root / "FLOW_ASSET_PACKAGE.schema.json").read_text(encoding="utf-8"))
        package = json.loads((root / "jk_rowling_scene_03" / "FLOW_ASSET_PACKAGE.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(package))
        self.assertEqual(errors, [])
        self.assertEqual(package["flow_asset_mode"], "APPROVED_REGRESSION_ASSET")
        self.assertGreaterEqual(len(package["flow_prompt_zh_tw"]), 300)
        self.assertGreaterEqual(len(package["flow_prompt_en"]), 300)
        self.assertEqual(len(package["manual_steps"]), 1)

    def test_release_governance_requires_all_gates(self) -> None:
        value = json.loads((ROOT / "config" / "release_governance.json").read_text(encoding="utf-8"))
        self.assertNotIn("APPROVED", value["allowed_preapproval_statuses"])
        self.assertEqual(value["current_release_mutation"], "PROHIBITED_UNTIL_APPROVAL")
        self.assertTrue(value["rollback"]["required_for_approved_release"])

    def test_golden_manifest_is_immutable_and_self_contained(self) -> None:
        root = ROOT / "golden" / "history_today" / "jk_rowling_v6_2"
        value = json.loads((root / "GOLDEN_BASELINE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(value["classification"], "APPROVED_IMMUTABLE_GOLDEN_BASELINE")
        self.assertTrue((root / "IMMUTABLE.lock").is_file())
        self.assertFalse(value["immutability"]["overwrite"])
        self.assertFalse(value["immutability"]["direct_edit"])
        self.assertFalse(any("_VALIDATION_RUNS" in item["path"] or "_SYSTEM_TRUE_REGRESSION_RERUN" in item["path"] for item in value["files"]))


if __name__ == "__main__":
    unittest.main()
