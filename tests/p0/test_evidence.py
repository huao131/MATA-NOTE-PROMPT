from __future__ import annotations

import unittest

from ._support import SRC  # noqa: F401
from mata_p0.errors import StopAndReport
from mata_p0.evidence import assert_canonical_eligible, validate_evidence_record


class EvidenceTests(unittest.TestCase):
    def test_all_four_evidence_values_are_accepted(self) -> None:
        for status in ("VERIFIED", "INFERRED", "UNVERIFIED", "CONFLICTED"):
            with self.subTest(status=status):
                validate_evidence_record(
                    {"evidence_status": status, "evidence_source": ["TEST_REF"]}
                )

    def test_unknown_evidence_value_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            validate_evidence_record(
                {"evidence_status": "ASSUMED", "evidence_source": ["TEST_REF"]}
            )

    def test_verified_with_pass_dependency_is_canonical_eligible(self) -> None:
        assert_canonical_eligible(
            {
                "evidence_status": "VERIFIED",
                "evidence_source": ["TEST_REF"],
                "dependency_status": "PASS",
            }
        )

    def test_non_verified_cannot_support_canonical(self) -> None:
        for status in ("INFERRED", "UNVERIFIED", "CONFLICTED"):
            with self.subTest(status=status), self.assertRaises(StopAndReport):
                assert_canonical_eligible(
                    {
                        "evidence_status": status,
                        "evidence_source": ["TEST_REF"],
                        "dependency_status": "PASS",
                    }
                )

    def test_non_pass_dependency_blocks_canonical(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_canonical_eligible(
                {
                    "evidence_status": "VERIFIED",
                    "evidence_source": ["TEST_REF"],
                    "dependency_status": "DEPENDENCY_RECHECK_REQUIRED",
                }
            )


if __name__ == "__main__":
    unittest.main()
