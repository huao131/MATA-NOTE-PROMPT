# CODEX P1 TEST MAPPING ADDENDUM V1.0

## 1. Addendum Identity

| Field | Value |
|---|---|
| Addendum ID | `CODEX-P1-TEST-MAPPING-ADDENDUM-V1.0-20260727-001` |
| Parent authorization | `CODEX-P1-AUTH-V1.0-20260727-001` |
| Status | `AUTHORIZED` |
| Effective date | `2026-07-27` |
| Repository | `huao131/MATA-AI-VIDEO-STUDIO` |

本 Addendum 依 D04、D05、D06、D08、D09、D11、D12 與 P0 Accepted
Implementation，建立 P1-01～P1-06 的一對一驗收測試契約。它不修改
D12，而是解除父授權中 P1 專用 test mapping 的治理缺口。

## 2. P1-01 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-EPI-01` | 驗證初始化計畫 Schema | `TEST_EPISODE_INITIALIZATION_VALID.json` | Schema 驗證通過 | 缺 scope／identity／必要欄位時阻塞 | D04、D11 P1-01 |
| `P1-EPI-02` | 隔離 TEST 與正式 Episode | `TEST_EPISODE_SCOPE_ISOLATION.json` | 只允許 `TEST_` scope | 測試資料指向正式 Episode | D06、D11 P1-01 |
| `P1-EPI-03` | 禁止正式 Episode 寫入 | `TEST_FORMAL_EPISODE_WRITE_ATTEMPT.json` | `STOP_AND_REPORT` | 正式 Episode 寫入被接受 | D06、D11 P1-01 |

## 3. P1-02 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-STATE-01` | 驗證 VERIFIED Canonical 候選 | `TEST_VERIFIED_CANONICAL_CANDIDATE.json` | 候選可進入後續人工 Gate | 缺證據仍被視為 Canonical | D05、D12 EVD-01 |
| `P1-STATE-02` | 阻塞非 VERIFIED 證據 | `TEST_NON_VERIFIED_STATE.json` | State／Gate 阻塞 | 非 VERIFIED 寫入 Canonical | D05、D12 EVD-01／03／04 |
| `P1-STATE-03` | 隔離 Segment 與 Episode READY | `TEST_SEGMENT_READY.json` | Episode 不自動 READY | Episode 被自動推升 | D05、D12 EVD-02 |
| `P1-STATE-04` | 阻塞未通過 Dependency | `TEST_DEPENDENCY_NOT_PASS.json` | 受影響 Gate 不得 PASS | recheck 未 PASS 仍推進 | D05、D12 REC-05 |

## 4. P1-03 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-GATE-01` | 驗證六 Gate 定義完整 | `TEST_SIX_GATES_COMPLETE.json` | 六個固定 Gate 全部存在 | 缺少、增加或改名 Gate | D05 |
| `P1-GATE-02` | 驗證 Gate 順序 | `TEST_GATE_ORDER.json` | 嚴格遵守正式順序 | 前置 Gate 未 PASS 即推進 | D05 |
| `P1-GATE-03` | 驗證稽核欄位完整 | `TEST_GATE_AUDIT_FIELDS.json` | 必填欄位完整 | 以布林值或缺欄位取代 record | D05、D11 P1-03 |
| `P1-GATE-04` | 禁止 Codex 宣告人工 Gate PASS | `TEST_CODEX_GATE_PASS_ATTEMPT.json` | `STOP_AND_REPORT` | Codex 自行核准 Gate | D05、D08 |

## 5. P1-04 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-STATUS-01` | 分離 Lifecycle 與 QC | `TEST_LIFECYCLE_QC_SEPARATION.json` | 兩種狀態域獨立 | QC 值混入 lifecycle | D05 |
| `P1-STATUS-02` | 禁止 Rejected Reference | `TEST_REJECTED_REFERENCE.json` | 驗證失敗並隔離 | Rejected 成為 Reference | D05、D12 AST-01 |
| `P1-STATUS-03` | 禁止 Rejected Dependency | `TEST_REJECTED_DEPENDENCY.json` | 驗證失敗並隔離 | Rejected 成為 Dependency | D05 |
| `P1-STATUS-04` | 禁止 Rejected Final Asset | `TEST_REJECTED_FINAL_ASSET.json` | Final Gate 阻塞 | Rejected 進入 Final Asset List | D05、D12 AST-04 |
| `P1-STATUS-05` | 禁止 Exact Asset 替代 | `TEST_EXACT_ASSET_REPLACEMENT.json` | 驗證失敗 | 生成、重繪或替代被接受 | D09、D12 AST-02 |

## 6. P1-05 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-PROMPT-01` | 驗證 approved input traceability | `TEST_PROMPT_APPROVED_INPUTS.json` | 所有輸入可追溯 | Prompt 無 approved input | D04、D11 P1-05 |
| `P1-PROMPT-02` | 驗證 Evidence／Version refs | `TEST_PROMPT_EVIDENCE_VERSION_REFS.json` | refs 完整且可稽核 | 缺 Evidence 或版本 | D04、D08 |
| `P1-PROMPT-03` | 阻塞非 VERIFIED Prompt metadata | `TEST_PROMPT_NON_VERIFIED.json` | metadata 阻塞 | 非 VERIFIED 被核准 | D04、D05 |
| `P1-PROMPT-04` | 禁止控制 Flow | `TEST_PROMPT_FLOW_CONTROL_ATTEMPT.json` | `STOP_AND_REPORT`，無外部呼叫 | 執行 Flow 或消耗點數 | D08、D11 P1-05 |

## 7. P1-06 Test Mapping

| Test ID | Purpose | Input fixture | Expected result | Negative condition | Source |
|---|---|---|---|---|---|
| `P1-HANDOFF-01` | 驗證 handoff 必填欄位 | `TEST_HANDOFF_REQUIRED_FIELDS.json` | 所有 D08 欄位完整 | 缺欄位仍通過 | D08 |
| `P1-HANDOFF-02` | 驗證 Gate／Dependency 阻塞 | `TEST_HANDOFF_BLOCKED_DEPENDENCY.json` | 未 PASS 即阻塞 | 未通過仍交接 | D05、D08、D12 REC-05 |
| `P1-HANDOFF-03` | 排除 Rejected | `TEST_HANDOFF_REJECTED_INPUT.json` | Rejected 被拒絕 | Rejected 進入 handoff | D08、D12 AST-01 |
| `P1-HANDOFF-04` | 限制 Exact Asset 引用 | `TEST_HANDOFF_EXACT_ASSET.json` | 只允許受控原檔引用 | 接受生成或替代資產 | D08、D09、D12 AST-02 |
| `P1-HANDOFF-05` | 禁止執行 Flow | `TEST_HANDOFF_FLOW_EXECUTION_ATTEMPT.json` | `STOP_AND_REPORT`，無外部呼叫 | 執行 Flow 或消耗點數 | D08、D11 P1-06 |

## 8. Common Regression and Acceptance

- P0 全部 62 項測試必須持續通過。
- Repository path traversal／allowlist 回歸必須通過。
- Protected Artifact changes：`0`
- Legacy／Formal Tree changes：`0`
- Media changes：`0`
- P1 新增測試：全部通過。
- `compileall`：`PASS`
- `git diff --check`：`PASS`

## 9. External Integration Boundary

所有 Drive、Flow、CapCut 或媒體相關情境只能使用
`tests/p1/fixtures/TEST_*` 的離線 fixture 或模擬輸入。測試不得登入、
授權、讀寫或呼叫 Google Drive、Flow、CapCut，也不得使用付費 API。

## 10. Mapping Status

P1-01～P1-06 均已建立一對一 Test ID，父授權中的 P1 專用 test
mapping gate 可改為 `AUTHORIZED`。若實作無法對應本文件的 purpose、
fixture、expected result、negative condition、source 與 work item，
必須 `STOP_AND_REPORT`。
