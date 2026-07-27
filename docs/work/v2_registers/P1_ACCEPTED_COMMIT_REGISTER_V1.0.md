# P1 Accepted Commit Register V1.0

## Identity

- Record ID: `P1-ACCEPTED-COMMIT-REGISTER-V1.0-20260727-001`
- Schema Version: `1.0`
- Register Status: `PENDING_FINAL_BASELINE`
- Created At UTC: `2026-07-27T01:15:26Z`

## Commit Chain

1. P0 Accepted Commit:
   `296a70fd87e4bde4b3bcc064e9aa6612531a4cb1`
2. P0 Integration Merge Commit:
   `4e2c971ff109b7a861dd2fdfee82478704d69c61`
3. P1 Governance Source Head:
   `9df0b7f1ea2637e02f53656e795b2c66cfa8aaae`
4. P1 Governance Cherry-pick Baseline:
   `db464570ffd828e9793e6d67db01dc7e19e83f80`
5. P1 Accepted Implementation Head:
   `271c16d9f107b69f3c27fc67656e7e1b464e65c6`
6. P1 Integration Merge Commit:
   `d299b970abe75c52f29941cd1838854c4e7d5956`
7. Governed P1 Accepted Baseline: `PENDING`

## Baseline Rules

- The P1 Accepted Implementation Head is not the final P2 baseline.
- The P1 Integration Merge Commit is not the final P2 baseline.
- Only the exact publication branch SHA produced after these six governance
  records are formally merged may become the P2 baseline.
- PR #4 remains governance source evidence and must not be merged again.
- Rollback must use revert; reset and history rewriting are prohibited.
- P2 and P3 remain `BLOCKED`.
