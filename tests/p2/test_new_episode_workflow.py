from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from ._support import ROOT, SRC, demo_brief  # noqa: F401
from mata_p0.constants import GATE_IDS
from mata_p0.errors import StopAndReport
from mata_p2.new_episode import (
    OUTPUT_FILES,
    assert_dependency_ready,
    build_candidate_package,
    main,
    run_workflow,
    validate_brief,
)


class NewEpisodeWorkflowTests(unittest.TestCase):
    def assert_structured_stop(self, callable_, *args, **kwargs):
        with self.assertRaises(StopAndReport) as context:
            callable_(*args, **kwargs)
        self.assertTrue(context.exception.violations)
        self.assertTrue(all(item.code and item.message for item in context.exception.violations))

    def test_positive_01_complete_candidate_package(self):
        package = build_candidate_package(demo_brief())
        self.assertEqual(set(package), set(OUTPUT_FILES))

    def test_positive_02_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "TEST_DRY_RUN"
            result = run_workflow(demo_brief(), output, dry_run=True)
            self.assertTrue(result["dry_run"])
            self.assertFalse(output.exists())

    def test_positive_03_episode_id_is_consistent(self):
        episode_id = demo_brief()["episode_id"]
        package = build_candidate_package(demo_brief())
        for name, record in package.items():
            if isinstance(record, dict) and "episode_id" in record:
                with self.subTest(name=name):
                    self.assertEqual(record["episode_id"], episode_id)

    def test_positive_04_audience_insight_complete(self):
        record = build_candidate_package(demo_brief())[OUTPUT_FILES[1]]
        for field in ("target_audience", "surface_need", "deeper_need", "trust_barrier"):
            self.assertTrue(record[field])

    def test_positive_05_three_hook_strategies(self):
        hooks = build_candidate_package(demo_brief())[OUTPUT_FILES[2]]["candidates"]
        self.assertEqual(
            {item["strategy"] for item in hooks},
            {"HIGH_RETENTION", "HIGH_RESONANCE", "HIGH_CONVERSION"},
        )

    def test_positive_06_gate_order_matches_p1(self):
        gates = build_candidate_package(demo_brief())[OUTPUT_FILES[6]]
        self.assertEqual(tuple(item["gate_id"] for item in gates), tuple(GATE_IDS))

    def test_positive_07_candidate_pending_states_only(self):
        package = build_candidate_package(demo_brief())
        serialized = json.dumps(package)
        for forbidden in ('"LOCKED"', '"FINAL"', '"MASTER"', '"APPROVED"'):
            self.assertNotIn(forbidden, serialized)
        self.assertTrue(all(item["gate_status"] == "PENDING" for item in package[OUTPUT_FILES[6]]))

    def test_positive_08_prompt_is_metadata_only(self):
        prompt = build_candidate_package(demo_brief())[OUTPUT_FILES[8]]
        self.assertNotIn("prompt_content", prompt)
        self.assertEqual(prompt["blocked_reason"], "PROMPT_CONTENT_NOT_GENERATED")

    def test_positive_09_handoff_is_placeholder_only(self):
        handoff = build_candidate_package(demo_brief())[OUTPUT_FILES[9]]
        self.assertFalse(handoff["external_execution"])
        self.assertEqual(handoff["readiness"], "PENDING_HUMAN_REVIEW")

    def test_positive_10_manifest_is_auditable(self):
        manifest = build_candidate_package(demo_brief())[OUTPUT_FILES[10]]
        self.assertEqual(manifest["work_item_id"], "P2-WF-01")
        self.assertEqual(manifest["external_operations"], [])
        self.assertEqual(manifest["output_files"], list(OUTPUT_FILES))

    def test_positive_11_existing_output_never_overwritten(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "TEST_EXISTING"
            output.mkdir()
            sentinel = output / "sentinel.txt"
            sentinel.write_text("KEEP", encoding="utf-8")
            self.assert_structured_stop(run_workflow, demo_brief(), output)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "KEEP")

    def test_positive_12_no_external_operations(self):
        package = build_candidate_package(demo_brief())
        report = package[OUTPUT_FILES[11]]
        self.assertEqual(report["external_operation_count"], 0)
        self.assertEqual(report["human_approval_count"], 0)
        self.assertEqual(report["canonical_write_count"], 0)

    def test_positive_13_cli_dry_run(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "TEST_CLI_DRY_RUN"
            code = main(
                [
                    "--brief",
                    str(ROOT / "examples" / "p2" / "TEST_P2_WF_01_BRIEF.json"),
                    "--output",
                    str(output),
                    "--dry-run",
                ]
            )
            self.assertEqual(code, 0)
            self.assertFalse(output.exists())

    def test_positive_14_writes_twelve_json_files(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "TEST_PACKAGE"
            result = run_workflow(demo_brief(), output)
            self.assertEqual(set(result["written"]), set(OUTPUT_FILES))
            self.assertEqual({item.name for item in output.iterdir()}, set(OUTPUT_FILES))
            for path in output.iterdir():
                json.loads(path.read_text(encoding="utf-8"))

    def test_negative_01_missing_required_field(self):
        brief = demo_brief()
        del brief["purpose"]
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_02_invalid_episode_id(self):
        brief = demo_brief()
        brief["episode_id"] = "EP02"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_03_invalid_duration(self):
        brief = demo_brief()
        brief["duration_seconds"] = 0
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_04_invalid_aspect_ratio(self):
        brief = demo_brief()
        brief["aspect_ratio"] = "3:2"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_05_path_traversal(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / ".." / "TEST_ESCAPE"
            self.assert_structured_stop(run_workflow, demo_brief(), output)

    def test_negative_06_formal_episode_path(self):
        self.assert_structured_stop(
            run_workflow,
            demo_brief(),
            Path("episodes") / "TEST_P2_WF_01",
        )

    def test_negative_07_protected_output_path(self):
        with tempfile.TemporaryDirectory() as parent:
            self.assert_structured_stop(
                run_workflow,
                demo_brief(),
                Path(parent) / "TEST_FINAL_OUTPUT",
            )

    def test_negative_08_approved_candidate_attempt(self):
        brief = demo_brief()
        brief["status"] = "APPROVED"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_09_codex_approver_attempt(self):
        brief = demo_brief()
        brief["approved_by"] = "CODEX"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_10_drive_operation_attempt(self):
        brief = demo_brief()
        brief["drive_operation"] = "CREATE"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_11_flow_operation_attempt(self):
        brief = demo_brief()
        brief["flow_operation"] = "EXECUTE"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_12_capcut_operation_attempt(self):
        brief = demo_brief()
        brief["capcut_operation"] = "EDIT"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_13_media_generation_attempt(self):
        brief = demo_brief()
        brief["media_generation"] = True
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_14_existing_output_conflict(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "TEST_CONFLICT"
            output.mkdir()
            self.assert_structured_stop(run_workflow, demo_brief(), output)

    def test_negative_15_schema_validation_failure(self):
        brief = demo_brief()
        brief["special_requirements"] = "TEST_ONLY"
        self.assert_structured_stop(validate_brief, brief)

    def test_negative_16_dependency_failure(self):
        self.assert_structured_stop(assert_dependency_ready, "FAIL")


if __name__ == "__main__":
    unittest.main()
