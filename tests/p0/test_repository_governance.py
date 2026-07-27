from __future__ import annotations

import unittest

from ._support import SRC  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p0.repository_governance import (
    assert_changed_paths_are_p0_only,
    assert_p0_write_path,
)


class RepositoryGovernanceTests(unittest.TestCase):
    def test_all_planned_p0_roots_are_allowed(self) -> None:
        for path in (
            "src/mata_p0/example.py",
            "schemas/p0/example.schema.json",
            "tests/p0/test_example.py",
            "docs/work/v2_reports/example.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(assert_p0_write_path(path), path)

    def test_parent_directory_components_stop(self) -> None:
        for path in (
            "src/mata_p0/../../episodes/EP02/file.json",
            "tests/p0/../outside.json",
            "schemas/p0/../../../README.md",
            r"src\mata_p0\..\..\episodes\EP02\file.json",
        ):
            with self.subTest(path=path):
                with self.assertRaises(StopAndReport):
                    assert_p0_write_path(path)

    def test_absolute_and_windows_drive_paths_stop(self) -> None:
        for path in (
            r"C:\MATA-AI-VIDEO-STUDIO-V2-P0\episodes\EP02\file.json",
            r"\\server\share\file.json",
            "/src/mata_p0/example.py",
        ):
            with self.subTest(path=path):
                with self.assertRaises(StopAndReport):
                    assert_p0_write_path(path)

    def test_empty_path_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_p0_write_path("")

    def test_legacy_write_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_p0_write_path("legacy/TEST.json")

    def test_media_write_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_p0_write_path("tests/p0/fixtures/TEST_IMAGE.png")

    def test_protected_write_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_p0_write_path("docs/work/v2_reports/P0_FINAL.md")

    def test_explicit_test_fixture_may_name_protected_scenario(self) -> None:
        path = "tests/p0/fixtures/TEST_VALID_VERSION_LOCK_REGISTER.json"
        self.assertEqual(assert_p0_write_path(path), path)

    def test_main_repository_files_are_out_of_p0_surface(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_p0_write_path("README.md")

    def test_changed_path_collection_stops_on_any_violation(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_changed_paths_are_p0_only(
                ["src/mata_p0/example.py", "episodes/EP02/ASSET_INDEX.json"]
            )


if __name__ == "__main__":
    unittest.main()
