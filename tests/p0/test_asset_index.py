from __future__ import annotations

import copy
import unittest

from ._support import ROOT, SRC, registry_by_code, valid_asset  # noqa: F401
from mata_p0.asset_index import (
    assert_asset_usage,
    assert_exact_asset_operation,
    read_asset_index,
    validate_asset_index,
    validate_asset_record,
)
from mata_p0.errors import StopAndReport


class AssetIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = registry_by_code()

    def test_valid_asset_contract_passes(self) -> None:
        validate_asset_record(valid_asset(), self.registry, canonical_candidate=True)

    def test_fixture_reader_passes(self) -> None:
        path = ROOT / "tests" / "p0" / "fixtures" / "TEST_VALID_ASSET_INDEX.json"
        self.assertEqual(len(read_asset_index(str(path), self.registry)), 1)

    def test_filename_is_not_required_identity(self) -> None:
        asset = valid_asset()
        self.assertNotIn("filename", asset)
        validate_asset_record(asset, self.registry)

    def test_invalid_lifecycle_stops(self) -> None:
        asset = valid_asset()
        asset["lifecycle_status"] = "QC_PENDING"
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry)

    def test_qc_cannot_use_lifecycle_value(self) -> None:
        asset = valid_asset()
        asset["qc_status"] = "APPROVED"
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry)

    def test_folder_reference_must_match_registry(self) -> None:
        asset = valid_asset()
        asset["folder_ref"]["display_name_zh_TW"] = "TEST_WRONG_NAME"
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry)

    def test_missing_drive_id_stops(self) -> None:
        asset = valid_asset()
        asset["google_drive_file_id"] = ""
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry)

    def test_missing_checksum_stops(self) -> None:
        asset = valid_asset()
        asset["checksum"] = ""
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry)

    def test_duplicate_asset_id_stops(self) -> None:
        first = valid_asset()
        second = copy.deepcopy(first)
        with self.assertRaises(StopAndReport):
            validate_asset_index([first, second], self.registry)

    def test_rejected_cannot_be_reference_dependency_or_final(self) -> None:
        asset = valid_asset()
        asset["lifecycle_status"] = "REJECTED"
        for role in ("REFERENCE", "DEPENDENCY", "FINAL_ASSET_LIST"):
            with self.subTest(role=role), self.assertRaises(StopAndReport):
                assert_asset_usage(asset, role)

    def test_rejected_cannot_be_canonical(self) -> None:
        asset = valid_asset()
        asset["lifecycle_status"] = "REJECTED"
        with self.assertRaises(StopAndReport):
            validate_asset_record(asset, self.registry, canonical_candidate=True)

    def test_exact_asset_contract_passes(self) -> None:
        validate_asset_record(valid_asset(exact=True), self.registry)

    def test_exact_asset_generated_replacement_stops(self) -> None:
        asset = valid_asset(exact=True)
        with self.assertRaises(StopAndReport):
            assert_exact_asset_operation(
                asset,
                proposed_drive_file_id=asset["approved_original_drive_file_id"],
                generated_or_redrawn=True,
            )

    def test_exact_asset_file_replacement_stops(self) -> None:
        asset = valid_asset(exact=True)
        with self.assertRaises(StopAndReport):
            assert_exact_asset_operation(
                asset,
                proposed_drive_file_id="TEST_DIFFERENT_FILE",
                generated_or_redrawn=False,
            )


if __name__ == "__main__":
    unittest.main()
