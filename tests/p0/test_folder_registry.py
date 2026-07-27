from __future__ import annotations

import copy
import unittest

from ._support import ROOT, SRC, folder_records  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p0.folder_registry import (
    read_folder_registry,
    resolve_folder,
    validate_folder_registry,
)


class FolderRegistryTests(unittest.TestCase):
    def test_current_effective_registry_passes(self) -> None:
        registry = validate_folder_registry(folder_records())
        self.assertEqual(len(registry), 7)

    def test_fixture_reader_passes(self) -> None:
        path = ROOT / "tests" / "p0" / "fixtures" / "TEST_VALID_FOLDER_REGISTRY.json"
        self.assertEqual(len(read_folder_registry(str(path))), 7)

    def test_duplicate_stable_code_stops(self) -> None:
        records = folder_records()
        records[1]["stable_folder_code"] = records[0]["stable_folder_code"]
        with self.assertRaises(StopAndReport):
            validate_folder_registry(records)

    def test_duplicate_drive_id_stops(self) -> None:
        records = folder_records()
        records[1]["google_drive_folder_id"] = records[0]["google_drive_folder_id"]
        with self.assertRaises(StopAndReport):
            validate_folder_registry(records)

    def test_unverified_entry_stops(self) -> None:
        records = folder_records()
        records[0]["verification_status"] = "UNVERIFIED"
        with self.assertRaises(StopAndReport):
            validate_folder_registry(records)

    def test_parent_mismatch_stops(self) -> None:
        records = folder_records()
        records[1]["parent_folder_id"] = "TEST_WRONG_PARENT"
        with self.assertRaises(StopAndReport):
            validate_folder_registry(records)

    def test_display_name_is_not_identity(self) -> None:
        registry = validate_folder_registry(folder_records())
        with self.assertRaises(StopAndReport):
            resolve_folder(registry)

    def test_resolves_by_stable_code_and_drive_id(self) -> None:
        registry = validate_folder_registry(folder_records())
        expected = registry["GLOBAL_OS"]
        actual = resolve_folder(
            registry,
            stable_folder_code="GLOBAL_OS",
            google_drive_folder_id=expected["google_drive_folder_id"],
        )
        self.assertEqual(actual["stable_folder_code"], "GLOBAL_OS")

    def test_unknown_folder_stops(self) -> None:
        registry = validate_folder_registry(folder_records())
        with self.assertRaises(StopAndReport):
            resolve_folder(registry, stable_folder_code="UNKNOWN")


if __name__ == "__main__":
    unittest.main()
