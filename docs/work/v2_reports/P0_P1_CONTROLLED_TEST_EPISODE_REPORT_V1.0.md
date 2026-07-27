# P0 + P1 Controlled Test Episode Report V1.0

## 1. Test ID

- Controlled Test ID: `TEST_EP_P0P1_001`
- Test Scope ID: `TEST_CONTROLLED_EPISODE_001`
- Test Plan ID: `TEST_PLAN_P0P1_001`
- Classification: `TEST ONLY`

## 2. Base SHA

`0a977f59a04df37c5c1285ebf0c1fc47890f0ef0`

The remote publication branch resolved to the exact required SHA before the
isolated test worktree was created.

## 3. Test Branch

`test/v2-p0-p1-controlled-episode-001`

## 4. Test Scope

This execution validates the existing P0 and P1 contracts with synthetic,
repository-local JSON data. It does not create a formal Episode, Canonical
Production State, media, Prompt body, or external-system operation.

## 5. Positive Cases

- Result: **14 passed / 14**
- Covered TEST Episode initialization, VERIFIED Production State candidate,
  ordered six-Gate simulated evaluation, lifecycle/QC separation, Reference
  and Exact Asset controls, Prompt Metadata, Storyboard/Flow handoff metadata,
  Dependency Recheck, Folder Registry, Asset Index, version/supersession,
  JSON Schema document parsing, protected-artifact guards, and repository path
  guards.
- `HUMAN_TEST_APPROVER` and `TEST_ONLY_SIMULATED_APPROVAL` are synthetic test
  markers and do not constitute formal human approval.

## 6. Negative Cases

- Result: **30 blocked / 30**
- Every required negative case raised structured `STOP_AND_REPORT` with one or
  more contract violations.
- No raw `AttributeError`, `TypeError`, or other unhandled exception escaped.

## 7. P0 Result

- Existing P0 regression: **62 passed / 0 failed**
- Controlled P0 contract probes passed.
- P0 source, Schema, existing tests, and fixtures modified: **0**

## 8. P1 Result

- Full P1 suite including Controlled Test: **74 passed / 0 failed**
- Existing P1 regression portion: **29 passed / 0 failed**
- Controlled Test portion: **45 passed / 0 failed**
- P1 source, Schema, existing tests, and fixtures modified: **0**

## 9. Regression and Static Validation

- P0 regression: PASS
- P1 regression: PASS
- Compileall: PASS
- Git diff check: PASS
- Controlled Test JSON parse: **9 passed / 0 failed**

## 10. External Operations

- Google Drive operations: 0
- Flow operations: 0
- CapCut / 剪映 operations: 0
- External API calls: 0
- Media generation operations: 0
- Paid API operations: 0
- Third-party packages added: 0

## 11. Formal Asset Changes

- Existing files modified: 0
- Protected artifact changes: 0
- Legacy changes: 0
- Formal Episode changes: 0
- Media changes: 0
- Formal Exact Asset changes: 0
- Canonical Production State changes: 0
- Main branch changes: 0

All Exact Asset identifiers and Drive identifiers in the fixtures are synthetic
`TEST_` values. No real Drive File ID or formal Exact Asset is referenced.

## 12. Stop Conditions

One governance conflict was detected. The execution therefore stops before
Commit, Push, and Draft PR creation:

- The Controlled Test authorization requires all test data to use
  `scope_type: TEST`.
- `schemas/p1/production_state.schema.json` currently permits only
  `EPISODE`, `SEGMENT`, and `ASSET` for `scope_type`.
- The authorized `TEST_PRODUCTION_STATE_CANDIDATE.json` fixture therefore
  cannot simultaneously satisfy the TEST-only authorization and the existing
  Production State JSON Schema.

No Schema or product implementation was changed to conceal or bypass this
conflict.

## 13. Finding Classification

| Classification | Count | Result |
| --- | ---: | --- |
| PASS | 44 case outcomes | 14 positive and 30 negative expectations met |
| TEST_DATA_DEFECT | 0 | None |
| P0_REMEDIATION_CANDIDATE | 0 | None |
| P1_REMEDIATION_CANDIDATE | 0 | None recorded separately from governance conflict |
| P2_CANDIDATE | 0 | None |
| GOVERNANCE_CONFLICT | 1 | Production State `scope_type` mismatch |
| STOP_AND_REPORT | 1 | Commit/Push/PR prohibited by conflict |

## 14. P0 Remediation Candidates

None.

## 15. P1 Remediation Candidates

None classified independently. Governance must first determine whether the
Production State Schema or the Controlled Test authorization owns the intended
TEST-scope representation.

## 16. P2 Candidates

None. No P2 behavior was required or exercised.

## 17. Governance Conflicts

`GOVERNANCE_CONFLICT-001`:

The Controlled Test authorization mandates `scope_type: TEST`, while the locked
P1 Production State Schema excludes `TEST`. This is not safely resolvable by
test code because changing either side would exceed the authorized write scope.

## 18. Success Criteria

- TEST-only isolation: PASS for all created fixtures
- Positive cases: PASS
- Negative structured blocking: PASS
- P0/P1 regression: PASS
- Compileall and diff check: PASS
- External operations and formal asset changes remain zero: PASS
- No governance conflict: **FAIL**
- Eligibility to Commit: **FAIL**

Overall result: **STOP_AND_REPORT / GOVERNANCE_CONFLICT**

## 19. Recommendation

- Accept current P0 and P1 runtime guard behavior demonstrated by the completed
  safe tests: **YES, with the stated governance condition**
- Create Remediation Authorization: **YES**
- Enter P2 Authorization Planning: **NO**

Recommended governance action: formally resolve whether controlled Production
State test fixtures may use `scope_type: EPISODE` under an explicit TEST scope
marker, or whether the P1 Production State Schema should authorize
`scope_type: TEST`. No implementation choice should be inferred.

## 20. TEST ONLY Declaration

Every fixture, identifier, approval, folder reference, Drive reference, asset,
segment, output, and evidence reference created by this execution is synthetic
and **TEST ONLY**. None may be promoted, copied, or interpreted as a formal
Episode, Gate approval, Exact Asset, Production State, or media asset.

P2 and P3 remain `BLOCKED`.

## Governance Conflict Remediation History

### First STOP_AND_REPORT

- Conflict: the original Controlled Test Authorization required every
  `scope_type` to be `TEST`.
- Formal contract: `production_state.schema.json` permits only `EPISODE`,
  `SEGMENT`, and `ASSET`.
- Classification: `GOVERNANCE_TEST_CONTRACT_DEFECT`.
- Decision: the formal Schema and product implementation remained unchanged.

### Second STOP_AND_REPORT

- Conflict: the first remediation instruction required Episode Initialization
  Plan data to use `scope_type: EPISODE`.
- Formal contract: `episode_initialization.schema.json` permits only `TEST` and
  `PLAN_CANDIDATE`.
- Classification: `GOVERNANCE_TEST_CONTRACT_DEFECT`.
- Decision: no value was inferred, and the formal Schema and product
  implementation remained unchanged.

Both stop events above are retained as permanent audit history. They are not
reclassified as P0, P1, or P2 product defects.

## Schema-Specific Scope Resolution V1.0

- Resolution ID: `SCHEMA-SPECIFIC-SCOPE-RESOLUTION-V1.0`
- Episode Initialization Plan permitted scope values: `TEST`,
  `PLAN_CANDIDATE`
- Controlled positive Initialization scope: `TEST`
- Production State permitted scope values: `EPISODE`, `SEGMENT`, `ASSET`
- Controlled Production State payloads: one `EPISODE`, one `SEGMENT`, and one
  `ASSET` candidate
- Other contracts: each fixture maps to its own formal Schema or Validator;
  contracts without `scope_type` record `NOT_APPLICABLE`
- Global shared `scope_type` rule: removed
- Test isolation: test branch, controlled fixture path, `TEST_` identifiers,
  test envelope, `test_only: true`, test namespace, and `VALIDATE_PLAN`
- Test Metadata is removed before formal Payload validation
- Schema changes: 0
- Product implementation changes: 0
- Existing tracked-file changes: 0
- Formal asset changes: 0

### Remediation Validation

- Positive cases: **17 passed / 17**
- Negative cases: **44 blocked / 44**
- Scope-resolution audit case: **1 passed / 1**
- Controlled Test total: **62 passed / 0 failed**
- Existing P1 regression: **29 passed / 0 failed**
- Full P1 suite including Controlled Test: **91 passed / 0 failed**
- P0 regression: **62 passed / 0 failed**
- JSON parse: **9 passed / 0 failed**
- Fixture-to-Schema/Validator mapping: **9 passed / 0 failed**
- Compileall: PASS
- Git diff check: PASS
- Unhandled exceptions: 0
- Protected changes: 0
- Legacy, formal Episode, media, and formal Exact Asset changes: 0
- Drive, Flow, CapCut, and media operations: 0
- Third-party packages added: 0
- Paid API operations: 0

### Final Classification After Remediation

| Classification | Count / Status |
| --- | ---: |
| TEST_DATA_DEFECT | 0 |
| P0_REMEDIATION_CANDIDATE | 0 |
| P1_REMEDIATION_CANDIDATE | 0 |
| P2_CANDIDATE | 0 |
| GOVERNANCE_CONFLICT | RESOLVED |
| Unhandled exceptions | 0 |

Final result after the authorized schema-specific remediation:
**PASS / GOVERNANCE_CONFLICT RESOLVED**.

The earlier `STOP_AND_REPORT` result remains historically correct for the two
superseded test-governance contracts. This final result applies only after
`SCHEMA-SPECIFIC-SCOPE-RESOLUTION-V1.0`.

P2 and P3 remain `BLOCKED`; this report does not authorize P2.
