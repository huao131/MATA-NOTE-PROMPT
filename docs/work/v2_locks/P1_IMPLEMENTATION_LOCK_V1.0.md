# P1 Implementation Lock V1.0

## Identity

- Lock ID: `P1-IMPLEMENTATION-LOCK-V1.0-20260727-001`
- Schema Version: `1.0`
- Lock Status: `LOCKED`
- Created At UTC: `2026-07-27T01:15:26Z`

## Locked Commits

- Locked Implementation Head: `271c16d9f107b69f3c27fc67656e7e1b464e65c6`
- Locked Integration Merge Commit: `d299b970abe75c52f29941cd1838854c4e7d5956`

## Locked Scope

- `src/mata_p1/`
- `schemas/p1/`
- `tests/p1/`
- `docs/work/v2_reports/P1_IMPLEMENTATION_VALIDATION_REPORT_V1.0.md`
- `docs/work/v2_reports/P1_GATE_REGISTER_REMEDIATION_REPORT_V1.1.md`
- The six P1 governance documents authorized by
  `CODEX-P1-AUTH-V1.0-20260727-001` and its approved addenda

## Lock Rules

- Locked artifacts must not be overwritten directly.
- Any later correction requires a new version and new formal authorization.
- P2 must not modify the P1 Locked Scope without formal Remediation
  Authorization.
- Rejected or unapproved versions must not replace this Lock.
- `main` is not included in this Lock.
- PR #4 remains source evidence and does not establish a second formal
  governance baseline.
- P2 and P3 remain `BLOCKED`.
