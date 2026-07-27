from __future__ import annotations

import json
import unittest

from ._support import ROOT, SRC  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p0.version_lock import (
    assert_file_operation_allowed,
    assert_unique_versions,
    protected_designations,
    validate_supersession,
)


class VersionLockTests(unittest.TestCase):
    def test_protected_designations_are_detected(self) -> None:
        marks = protected_designations("specs/EXAMPLE_MASTER_V1.0_FINAL.md")
        self.assertEqual(marks, {"MASTER", "FINAL"})

    def test_protected_file_operations_stop(self) -> None:
        for operation in ("WRITE", "OVERWRITE", "RENAME", "MOVE", "DELETE"):
            with self.subTest(operation=operation), self.assertRaises(StopAndReport):
                assert_file_operation_allowed(
                    operation, "specs/EXAMPLE_V1.0_LOCK.md"
                )

    def test_unprotected_new_p0_file_is_allowed(self) -> None:
        assert_file_operation_allowed("WRITE", "src/mata_p0/example.py")

    def test_lowercase_lock_module_name_is_not_protected_designation(self) -> None:
        assert_file_operation_allowed("WRITE", "src/mata_p0/version_lock.py")

    def test_duplicate_version_stops(self) -> None:
        records = [
            {"scope_id": "TEST", "artifact_id": "A", "version": "V1.0"},
            {"scope_id": "TEST", "artifact_id": "A", "version": "V1.0"},
        ]
        with self.assertRaises(StopAndReport):
            assert_unique_versions(records)

    def test_version_fixture_passes(self) -> None:
        path = (
            ROOT
            / "tests"
            / "p0"
            / "fixtures"
            / "TEST_VALID_VERSION_LOCK_REGISTER.json"
        )
        records = json.loads(path.read_text(encoding="utf-8"))["records"]
        assert_unique_versions(records)

    def test_same_version_for_different_artifact_is_allowed(self) -> None:
        assert_unique_versions(
            [
                {"scope_id": "TEST", "artifact_id": "A", "version": "V1.0"},
                {"scope_id": "TEST", "artifact_id": "B", "version": "V1.0"},
            ]
        )

    def test_supersession_requires_new_version(self) -> None:
        old = {"scope_id": "TEST", "artifact_id": "A", "version": "V1.0"}
        with self.assertRaises(StopAndReport):
            validate_supersession(old, dict(old))

    def test_supersession_cannot_mutate_old_artifact(self) -> None:
        old = {"scope_id": "TEST", "artifact_id": "A", "version": "V1.0"}
        new = {"scope_id": "TEST", "artifact_id": "A", "version": "V1.1"}
        with self.assertRaises(StopAndReport):
            validate_supersession(old, new, old_artifact_mutated=True)


if __name__ == "__main__":
    unittest.main()
