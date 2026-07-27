from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ._support import ROOT, demo_brief  # noqa: F401
from mata_p2.new_episode import OUTPUT_FILES, build_candidate_package, main, run_workflow


def beauty_brief() -> dict:
    return {
        "episode_id": "EP003",
        "title": "美業老闆如何用AI影片自動預約，不用天天自拍剪片",
        "purpose": (
            "透過原創AI影片呈現美業經營者如何降低內容製作負擔、提升預約效率，"
            "引起美容師、美睫師、美甲師及醫美診所經營者學習AI影片行銷的興趣。"
        ),
        "target_audience": "美容師、美睫師、美甲師、醫美診所經營者",
        "duration_seconds": 20,
        "platform": "Facebook／Instagram／YouTube Shorts",
        "aspect_ratio": "9:16",
        "desired_action": "引起觀眾學習AI原創影片的興趣，並報名參加課程",
        "series_name": "如果學會原創AI影片",
        "existing_character_usage": "NONE",
        "special_requirements": [
            "聚焦沒時間天天自拍、剪片與經營內容；不得宣稱完全自動預約或保證成交。"
        ],
    }


class EpisodeInputAndCreativeRemediationTests(unittest.TestCase):
    def cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def package(self) -> dict:
        return build_candidate_package(beauty_brief())

    def test_input_01_brief_json_executes(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "OUT"
            code, stdout, _ = self.cli(
                "--brief-json", json.dumps(beauty_brief(), ensure_ascii=False),
                "--output", str(output), "--dry-run",
            )
            self.assertEqual(code, 0)
            self.assertTrue(json.loads(stdout)["dry_run"])

    def test_input_02_brief_and_brief_json_are_mutually_exclusive(self):
        with tempfile.TemporaryDirectory() as parent:
            code, _, stderr = self.cli(
                "--brief", str(ROOT / "examples/p2/TEST_P2_WF_01_BRIEF.json"),
                "--brief-json", json.dumps(beauty_brief()),
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 2)
            self.assertIn("BRIEF_INPUT_EXACTLY_ONE_REQUIRED", stderr)

    def test_input_03_missing_brief_input_is_blocked(self):
        with tempfile.TemporaryDirectory() as parent:
            code, _, stderr = self.cli(
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 2)
            self.assertIn("BRIEF_INPUT_EXACTLY_ONE_REQUIRED", stderr)

    def test_input_04_invalid_inline_json_is_blocked(self):
        with tempfile.TemporaryDirectory() as parent:
            code, _, stderr = self.cli(
                "--brief-json", "{invalid",
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 2)
            self.assertIn("BRIEF_JSON_INVALID", stderr)
            self.assertNotIn("{invalid", stderr)

    def test_input_05_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "OUT"
            code, _, _ = self.cli(
                "--brief-json", json.dumps(beauty_brief()),
                "--output", str(output), "--dry-run",
            )
            self.assertEqual(code, 0)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(parent).iterdir()), [])

    def test_input_06_no_temp_brief_is_created(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "OUT"
            before = set(Path(parent).rglob("*"))
            self.cli(
                "--brief-json", json.dumps(beauty_brief()),
                "--output", str(output), "--dry-run",
            )
            self.assertEqual(set(Path(parent).rglob("*")), before)

    def test_input_07_file_brief_remains_compatible(self):
        with tempfile.TemporaryDirectory() as parent:
            code, _, _ = self.cli(
                "--brief", str(ROOT / "examples/p2/TEST_P2_WF_01_BRIEF.json"),
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 0)

    def test_input_07a_dry_run_accepts_missing_nested_parent_without_writes(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "work/episode_candidates/EP003/P2_WF_01_V1.0"
            code, _, _ = self.cli(
                "--brief-json", json.dumps(beauty_brief()),
                "--output", str(output), "--dry-run",
            )
            self.assertEqual(code, 0)
            self.assertEqual(list(Path(parent).iterdir()), [])

    def test_creative_08_audience_fields_are_nonempty(self):
        audience = self.package()[OUTPUT_FILES[1]]
        fields = (
            "surface_pains", "deep_pains", "core_desires", "misconceptions",
            "viewing_motivations", "action_resistance", "core_belief_to_attack",
        )
        self.assertTrue(all(audience[field] for field in fields))

    def test_creative_09_all_seven_beauty_pains_are_covered(self):
        text = " ".join(self.package()[OUTPUT_FILES[1]]["surface_pains"])
        for phrase in ("自拍", "剪輯", "產出", "詢問或預約", "個人風格", "親自出鏡", "工具複雜"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_creative_10_three_hook_strategies_exist(self):
        hooks = self.package()[OUTPUT_FILES[2]]["candidates"]
        self.assertEqual(
            [item["strategy"] for item in hooks],
            ["HIGH_RETENTION", "HIGH_RESONANCE", "HIGH_CONVERSION"],
        )

    def test_creative_11_hooks_are_materially_different(self):
        hooks = [item["hook"] for item in self.package()[OUTPUT_FILES[2]]["candidates"]]
        self.assertEqual(len(set(hooks)), 3)
        self.assertTrue(all(len(set(left.split()) ^ set(right.split())) > 0 for left, right in zip(hooks, hooks[1:])))

    def test_creative_12_each_hook_has_required_fields(self):
        fields = {
            "hook", "core_viewpoint", "story_direction", "emotional_curve",
            "cta_direction", "recommendation_reason",
        }
        for hook in self.package()[OUTPUT_FILES[2]]["candidates"]:
            self.assertTrue(fields.issubset(hook))
            self.assertTrue(all(hook[field] for field in fields))

    def test_creative_13_primary_and_supporting_hooks_exist(self):
        record = self.package()[OUTPUT_FILES[2]]
        self.assertTrue(record["primary_hook"])
        self.assertEqual(len(record["supporting_hooks"]), 2)

    def test_creative_14_hook_psychological_path_exists(self):
        self.assertGreaterEqual(
            len(self.package()[OUTPUT_FILES[2]]["hook_psychological_path"]), 3
        )

    def test_creative_15_lock_candidate_pending_human_review(self):
        creative = self.package()[OUTPUT_FILES[3]]
        self.assertEqual(creative["approval_status"], "PENDING_HUMAN_REVIEW")
        self.assertIsNone(creative["approved_by"])

    def test_creative_16_lock_candidate_required_fields(self):
        creative = self.package()[OUTPUT_FILES[3]]
        for field in ("audience", "hook_strategy", "core_message", "narrative_direction", "cta_direction"):
            self.assertTrue(creative[field])

    def test_creative_17_story_fields_are_nonempty(self):
        treatment = self.package()[OUTPUT_FILES[4]]["treatment"]
        fields = (
            "opening", "conflict", "escalation", "turning_point", "solution",
            "result", "ending", "emotional_curve", "retention_nodes", "cta_transition",
        )
        self.assertTrue(all(treatment[field] for field in fields))

    def test_creative_18_timeline_ends_at_twenty_seconds(self):
        story = self.package()[OUTPUT_FILES[4]]
        self.assertEqual(story["pace_segments"][0]["start_seconds"], 0)
        self.assertEqual(story["pace_segments"][-1]["end_seconds"], 20)
        self.assertEqual(
            sum(item["end_seconds"] - item["start_seconds"] for item in story["pace_segments"]),
            20,
        )

    def test_creative_19_cta_is_course_interest_direction(self):
        cta = self.package()[OUTPUT_FILES[4]]["treatment"]["cta_transition"]
        self.assertIn("課程", cta)
        self.assertIn("了解", cta)

    def test_creative_20_no_guaranteed_booking_or_sale_claim(self):
        serialized = json.dumps(self.package(), ensure_ascii=False)
        for forbidden in ("保證預約", "保證成交", "必然成交", "完全自動預約"):
            self.assertNotIn(forbidden, serialized)

    def test_creative_21_no_health_product_sales(self):
        serialized = json.dumps(self.package(), ensure_ascii=False)
        for forbidden in ("大健康產品", "保健品", "直銷產品"):
            self.assertNotIn(forbidden, serialized)

    def test_creative_22_no_empty_todo_tbd_or_generic_placeholder(self):
        records = [
            self.package()[OUTPUT_FILES[index]]
            for index in (1, 2, 3, 4)
        ]
        serialized = json.dumps(records, ensure_ascii=False)
        for forbidden in ('""', "TODO", "TBD", "PLACEHOLDER"):
            self.assertNotIn(forbidden, serialized.upper())

    def test_creative_23_needs_human_input_for_generic_audience(self):
        brief = demo_brief()
        package = build_candidate_package(brief)
        self.assertTrue(package[OUTPUT_FILES[1]]["needs_human_input"])
        self.assertTrue(package[OUTPUT_FILES[4]]["needs_human_input"])

    def test_safety_24_no_human_approval_or_external_operations(self):
        package = self.package()
        self.assertEqual(package[OUTPUT_FILES[10]]["external_operations"], [])
        self.assertEqual(package[OUTPUT_FILES[11]]["human_approval_count"], 0)

    def test_safety_25_no_external_api_is_called(self):
        with patch("urllib.request.urlopen", side_effect=AssertionError("network called")):
            package = self.package()
        self.assertEqual(package[OUTPUT_FILES[11]]["external_operation_count"], 0)

    def test_safety_26_manifest_is_auditable(self):
        manifest = self.package()[OUTPUT_FILES[10]]
        self.assertEqual(manifest["checks"]["brief_input_contract"], "P2-WF-01.1")
        self.assertEqual(manifest["checks"]["creative_candidate_generation"], "PASS")
        self.assertEqual(manifest["output_files"], list(OUTPUT_FILES))

    def test_safety_27_formal_status_injection_is_blocked(self):
        brief = beauty_brief()
        brief["status"] = "APPROVED"
        with tempfile.TemporaryDirectory() as parent:
            code, _, stderr = self.cli(
                "--brief-json", json.dumps(brief),
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 2)
            self.assertIn("FORBIDDEN_OPERATION_REQUEST", stderr)

    def test_safety_28_external_operation_injection_is_blocked(self):
        brief = beauty_brief()
        brief["flow_operation"] = "EXECUTE"
        with tempfile.TemporaryDirectory() as parent:
            code, _, stderr = self.cli(
                "--brief-json", json.dumps(brief),
                "--output", str(Path(parent) / "OUT"), "--dry-run",
            )
            self.assertEqual(code, 2)
            self.assertIn("FORBIDDEN_OPERATION_REQUEST", stderr)

    def test_safety_29_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "OUT"
            output.mkdir()
            sentinel = output / "sentinel"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(Exception):
                run_workflow(beauty_brief(), output)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_safety_30_package_writes_exactly_twelve_files(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "OUT"
            result = run_workflow(beauty_brief(), output)
            self.assertEqual(len(result["written"]), 12)
            self.assertEqual({path.name for path in output.iterdir()}, set(OUTPUT_FILES))

    def test_safety_31_nested_output_creates_no_sibling_files(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "work/episode_candidates/EP003/P2_WF_01_V1.0"
            run_workflow(beauty_brief(), output)
            files = [path for path in Path(parent).rglob("*") if path.is_file()]
            self.assertEqual({path.parent for path in files}, {output})
            self.assertEqual({path.name for path in files}, set(OUTPUT_FILES))


if __name__ == "__main__":
    unittest.main()
