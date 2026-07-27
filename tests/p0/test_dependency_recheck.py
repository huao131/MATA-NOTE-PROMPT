from __future__ import annotations

import json
import unittest

from ._support import ROOT, SRC  # noqa: F401
from mata_p0.dependency_recheck import (
    assert_gate_allowed,
    assert_segment_ready_does_not_promote_episode,
    create_recheck_record,
    validate_recheck_record,
)
from mata_p0.errors import StopAndReport


def recheck_record() -> dict:
    return create_recheck_record(
        affected_assets=["TEST_ASSET"],
        affected_segments=["TEST_SEGMENT"],
        affected_outputs=["TEST_OUTPUT"],
        recheck_owner="TEST_OWNER",
        evidence_source=["TEST_COMMIT"],
    )


class DependencyRecheckTests(unittest.TestCase):
    def test_upstream_change_creates_required_recheck(self) -> None:
        record = recheck_record()
        self.assertEqual(
            record["dependency_status"], "DEPENDENCY_RECHECK_REQUIRED"
        )
        self.assertEqual(
            record["recheck_result"], "DEPENDENCY_RECHECK_REQUIRED"
        )

    def test_recheck_fixture_passes(self) -> None:
        path = (
            ROOT
            / "tests"
            / "p0"
            / "fixtures"
            / "TEST_VALID_DEPENDENCY_RECHECK.json"
        )
        validate_recheck_record(json.loads(path.read_text(encoding="utf-8")))

    def test_empty_affected_scope_stops(self) -> None:
        with self.assertRaises(StopAndReport):
            create_recheck_record(
                affected_assets=[],
                affected_segments=[],
                affected_outputs=[],
                recheck_owner="TEST_OWNER",
                evidence_source=["TEST_COMMIT"],
            )

    def test_gate_pass_blocked_before_recheck_pass(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_gate_allowed("PASS", recheck_record())

    def test_blocked_gate_allowed_while_recheck_pending(self) -> None:
        assert_gate_allowed("BLOCKED", recheck_record())

    def test_gate_pass_allowed_after_recheck_pass(self) -> None:
        record = recheck_record()
        record["recheck_result"] = "PASS"
        assert_gate_allowed("PASS", record)

    def test_segment_ready_cannot_promote_episode_ready(self) -> None:
        with self.assertRaises(StopAndReport):
            assert_segment_ready_does_not_promote_episode(
                segment_status="READY",
                current_episode_status="IN_PROGRESS",
                proposed_episode_status="READY",
                promotion_basis="SEGMENT_READY",
            )

    def test_episode_ready_is_not_blocked_when_not_segment_driven(self) -> None:
        assert_segment_ready_does_not_promote_episode(
            segment_status="READY",
            current_episode_status="IN_PROGRESS",
            proposed_episode_status="READY",
            promotion_basis="EPISODE_GATE_AGGREGATE",
        )


if __name__ == "__main__":
    unittest.main()
