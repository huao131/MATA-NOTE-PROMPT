# CODEX P1 IMPLEMENTATION AUTHORIZATION V1.0

## 1. Authorization Identity

| Field | Value |
|---|---|
| Authorization ID | `CODEX-P1-AUTH-V1.0-20260727-001` |
| Version | `V1.0` |
| Status | `AUTHORIZED_WITH_PHASE_GATES` |
| Authorized by | Mata老師 |
| Effective date | `2026-07-27` |
| Repository | `huao131/MATA-AI-VIDEO-STUDIO` |
| P0 accepted baseline | `296a70fd87e4bde4b3bcc064e9aa6612531a4cb1` |
| System Specification Lock ID | `SYS-SPEC-LOCK-V2.0-20260726-001` |
| Current Effective Manifest | `docs/work/v2_drafts/20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.2_DRAFT.md` |
| Remediation reference | `CODEX-P1-WRITE-SCOPE-ADDENDUM-V1.0-20260727-001`; `CODEX-P1-TEST-MAPPING-ADDENDUM-V1.0-20260727-001` |

本文件只建立 P1 實作授權與 phase gates。本次治理作業不建立 P1
實作分支、不建立 P1 程式、不修改 P0，亦不授權 P2 或 P3。

## 2. Preconditions

- P0 Foundation Implementation：`PASS`
- P0 Acceptance Review：`PASS`
- P0 Accepted Commit 固定為
  `296a70fd87e4bde4b3bcc064e9aa6612531a4cb1`
- P0 的 Schema、Evidence、Lifecycle、QC、Dependency Recheck、
  Version／Lock 與 Repository Governance 保護機制必須持續生效。
- P0 程式、Schema、測試與報告不得被破壞、刪除、覆寫或繞過。
- P1 開始前，實作分支必須由上述 P0 Accepted Commit 建立，並確認
  remote history 一致。
- P1 精確實作路徑由 Write Scope Addendum 核准；P1 一對一測試 ID
  由 Test Mapping Addendum 核准。兩份 Addendum 必須與本授權一起
  通過 P1 Authorization Review。

## 3. Exact P1 Scope

P1 僅包含 D11 `10_CODEX_BACKLOG_V2.1_DRAFT.md` 中標為 P1 的六個
工作項目。目的、輸入、輸出、依賴、邊界與驗收均來自 D04、D05、
D08、D09、D10、D11、D12，不得擴充。

### P1-01 — New Episode initialization plan

- 目的：建立新 Episode 初始化計畫，並確保新 Episode 與 `TEST_`
  scope 隔離。
- 輸入：D04 Workflow Schema、D10 Portable Installation Guide。
- 輸出：New Episode initialization plan。
- 依賴：P0 已接受；Repository Publication Gate 已解除。
- 實作邊界：只處理新 V2 Episode／測試範圍的初始化規劃；精確寫入
  路徑已由 Write Scope Addendum 正式核准，實作只能使用核准路徑與
  `P1-EPI-01`～`P1-EPI-03`，超出 Addendum 範圍即 `STOP_AND_REPORT`。
- 驗收測試：`P1-EPI-01`～`P1-EPI-03`；P0 path governance 回歸另列
  於共用 mandatory tests。
- 不包含：Legacy 遷移、正式 Episode 資料修改、Drive 資料夾建立、
  P2／P3。

### P1-02 — Production State update workflow

- 目的：以可稽核流程更新 Episode／Segment／Asset Production State。
- 輸入：D05 Production State and Gate Model。
- 輸出：Production State update workflow。
- 依賴：P0-01 Schema validation、P0-05 Evidence validator。
- 實作邊界：只允許符合 D05 Schema、Evidence 與 Gate 順序的狀態候選；
  不得推定 Canonical State。精確路徑已由 Write Scope Addendum 核准，
  實作只能使用核准路徑與 `P1-STATE-01`～`P1-STATE-04`，超出範圍即
  `STOP_AND_REPORT`。
- 驗收測試：`P1-STATE-01`～`P1-STATE-04`。
- 不包含：Segment READY 自動推升 Episode READY、人工核准取代、
  正式 Production State 寫入。

### P1-03 — Gate Register operations

- 目的：建立六個固定 Gate 的完整、可稽核 Register 操作。
- 輸入：D05 Production State and Gate Model、D11 Backlog。
- 輸出：Gate Register operations。
- 依賴：P1-02。
- 實作邊界：Gate entry 必須保存 D05 規定欄位；不得以布林值取代
  Gate record，亦不得由 Codex 宣告人工 Gate PASS。精確路徑已由
  Write Scope Addendum 核准，實作只能使用核准路徑與
  `P1-GATE-01`～`P1-GATE-04`，超出範圍即 `STOP_AND_REPORT`。
- 驗收測試：`P1-GATE-01`～`P1-GATE-04`。
- 不包含：人工核准、P2／P3 Gate 自動化、正式 Gate PASS 寫入。

### P1-04 — Segment／Asset status handling

- 目的：依正式狀態模型處理 Segment 與 Asset 狀態，隔離 Rejected。
- 輸入：D08 Tool Handoff／Asset contract rules。
- 輸出：Segment／Asset status handling。
- 依賴：P0-03 Asset Index contract。
- 實作邊界：Segment、Asset、Lifecycle 與 QC 狀態維持分離；
  `REJECTED` 只保留為歷史或隔離證據。精確路徑已由 Write Scope
  Addendum 核准，實作只能使用核准路徑與
  `P1-STATUS-01`～`P1-STATUS-05`，超出範圍即 `STOP_AND_REPORT`。
- 驗收測試：`P1-STATUS-01`～`P1-STATUS-05`。
- 不包含：把 Rejected 納入 Reference／Dependency／Final Asset List、
  Exact Asset 生成、重繪或替代。

### P1-05 — Prompt Library metadata model

- 目的：定義可追溯至 approved inputs 的 Prompt Library metadata。
- 輸入：D04 Workflow Schema、D08 Tool Handoff Specification。
- 輸出：Prompt Library metadata model。
- 依賴：D04 GAP 已由 Current Effective Workflow Schema 解除。
- 實作邊界：僅處理 metadata 與來源追溯；精確 write paths 已由 Write
  Scope Addendum 正式核准，一對一 test mapping 已由 Test Mapping
  Addendum 正式核准。實作只能使用核准路徑與
  `P1-PROMPT-01`～`P1-PROMPT-04`，超出 Addendum 範圍即
  `STOP_AND_REPORT`。
- 驗收測試：`P1-PROMPT-01`～`P1-PROMPT-04`。
- 不包含：Prompt 內容生成、Flow 控制、外部 API 呼叫、正式資產處理。

### P1-06 — Storyboard／Flow handoff manifest

- 目的：建立人工可交接的 Storyboard／Flow handoff manifest，並揭露
  驗證缺口。
- 輸入：D08 Tool Handoff Specification、D09 QC and Recovery
  Specification。
- 輸出：Storyboard／Flow handoff manifest。
- 依賴：D08 GAP 已由 Current Effective Tool Handoff Specification
  解除。
- 實作邊界：只產出檔案化交接資料與驗證缺口；精確 write paths 已由
  Write Scope Addendum 正式核准，一對一 test mapping 已由 Test
  Mapping Addendum 正式核准。實作只能使用核准路徑與
  `P1-HANDOFF-01`～`P1-HANDOFF-05`，超出 Addendum 範圍即
  `STOP_AND_REPORT`。
- 驗收測試：`P1-HANDOFF-01`～`P1-HANDOFF-05`。
- 不包含：Flow 自動呼叫、點數消耗、媒體生成、CapCut 操作或發布。

## 4. Authorized Implementation Branch

- Branch：`implementation/v2-p1-orchestration`
- Required base commit：
  `296a70fd87e4bde4b3bcc064e9aa6612531a4cb1`

本文件僅指定該分支；建立或使用該分支不屬於本次治理作業。在 P1
Authorization Review 完成前不得建立該分支或開始實作。

## 5. Authorized Read Scope

P1 Codex 只可讀取：

1. `docs/work/v2_locks/SYSTEM_SPECIFICATION_LOCK_V2.0_RECORD.md`
2. `docs/work/v2_locks/SYSTEM_SPECIFICATION_LOCK_V2.0_ADDENDUM_V1.0.md`
3. `docs/work/v2_registers/SYSTEM_SPECIFICATION_LOCK_REGISTER_V2.0.json`
4. `docs/work/v2_authorizations/CODEX_IMPLEMENTATION_AUTHORIZATION_V1.1.md`
5. `docs/work/v2_drafts/20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.2_DRAFT.md`
6. Manifest V2.2 中 `CURRENT_EFFECTIVE`、`LOCKED`、`VERIFIED` 且
   `codex_read_allowed=true` 的 D01–D12 與 S01–S02。
7. P0 Accepted Commit 中的 `src/mata_p0/`、`schemas/p0/`、
   `tests/p0/` 與兩份 P0 報告。
8. 經本授權及後續 P1 Authorization Review 核准後，由 P1 自行建立、
   且位於已核准精確 write scope 的檔案。

不得讀取未列入 Manifest V2.2 的歷史 Draft、Legacy 內容或聊天推論
作為實作依據。

## 6. Authorized Write Scope

Write Scope Addendum
`CODEX-P1-WRITE-SCOPE-ADDENDUM-V1.0-20260727-001` 核准下列最小、
隔離、可回復的 P1 專用路徑：

| Work item | Exact authorized paths | Status |
|---|---|---|
| P1-01 | `src/mata_p1/episode_initialization.py`; `schemas/p1/episode_initialization.schema.json`; `tests/p1/test_episode_initialization.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| P1-02 | `src/mata_p1/production_state.py`; `schemas/p1/production_state.schema.json`; `tests/p1/test_production_state.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| P1-03 | `src/mata_p1/gate_register.py`; `schemas/p1/gate_register.schema.json`; `tests/p1/test_gate_register.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| P1-04 | `src/mata_p1/status_handling.py`; `schemas/p1/segment_asset_status.schema.json`; `tests/p1/test_status_handling.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| P1-05 | `src/mata_p1/prompt_metadata.py`; `schemas/p1/prompt_library_metadata.schema.json`; `tests/p1/test_prompt_metadata.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| P1-06 | `src/mata_p1/handoff_manifest.py`; `schemas/p1/storyboard_flow_handoff.schema.json`; `tests/p1/test_handoff_manifest.py`; `tests/p1/fixtures/TEST_*` | `AUTHORIZED` |
| Shared | `src/mata_p1/__init__.py`; `src/mata_p1/constants.py`; `src/mata_p1/errors.py`; `tests/p1/__init__.py`; `tests/p1/_support.py` | `AUTHORIZED` |
| P1 delivery | `docs/work/v2_reports/P1_IMPLEMENTATION_VALIDATION_REPORT_V1.0.md` | `AUTHORIZED` |

本授權不授權整個 `src/`、`schemas/`、`tests/` 或 `docs/`。除上表
精確路徑與 `TEST_*` fixture pattern 外，任何寫入均須
`STOP_AND_REPORT`。不得修改 P0、Legacy、媒體、正式 Episode／
Production State 或受保護檔案。

## 7. P1 Mandatory Controls

- P0 Evidence、Lifecycle 與 QC 分離規則持續有效。
- 非 `VERIFIED` 不得支撐 Canonical Production State。
- Dependency Recheck 未 `PASS`，受影響 Gate 不得推進。
- Segment `READY` 不得自動推升 Episode `READY`。
- `REJECTED` 不得成為 Reference、Dependency 或 Final Asset。
- Exact Asset 不得生成、重繪、模仿或替代。
- `LOCK`／`FINAL`／`MASTER`／`APPROVED` 不得原地修改、改名、
  移動或刪除。
- 不得以檔名作為 Asset identity。
- 所有狀態變更必須保存版本、操作者、時間、證據與依賴，可被稽核。
- 所有 P1 操作必須能 `STOP_AND_REPORT`。
- 不得繞過或弱化 P0 Repository Governance。

## 8. P1 Test and Acceptance Requirements

P1 測試必須包含：

- 單元測試、整合測試與負向測試。
- EVD-01 至 EVD-04 Evidence／State／Gate 阻塞測試。
- VLK-01 至 VLK-04 Protected Artifact、版本與 Dependency Recheck
  測試。
- AST-01 至 AST-04 Rejected、Exact Asset、Drive metadata 與 Final
  Asset List 測試；涉及 Drive 的部分只能使用離線 fixture。
- REC-01 至 REC-05 Stop／Recovery／Conflict／Gate blocking 測試；
  不得操作 Drive。
- Gate 順序與六 Gate 完整稽核欄位測試。
- Test Mapping Addendum 中 P1-01～P1-06 的 25 個正式一對一 Test ID：
  - P1-01：`P1-EPI-01`、`P1-EPI-02`、`P1-EPI-03`
  - P1-02：`P1-STATE-01`、`P1-STATE-02`、`P1-STATE-03`、
    `P1-STATE-04`
  - P1-03：`P1-GATE-01`、`P1-GATE-02`、`P1-GATE-03`、
    `P1-GATE-04`
  - P1-04：`P1-STATUS-01`、`P1-STATUS-02`、`P1-STATUS-03`、
    `P1-STATUS-04`、`P1-STATUS-05`
  - P1-05：`P1-PROMPT-01`、`P1-PROMPT-02`、`P1-PROMPT-03`、
    `P1-PROMPT-04`
  - P1-06：`P1-HANDOFF-01`、`P1-HANDOFF-02`、`P1-HANDOFF-03`、
    `P1-HANDOFF-04`、`P1-HANDOFF-05`
- P1-01～P1-06 的 test mapping status 全部為 `AUTHORIZED`。
- Repository path traversal／allowlist 回歸測試。
- P0 全部 `62` 項測試持續通過。
- P1 新增測試全部通過。
- `compileall`：`PASS`。
- `git diff --check`：`PASS`。
- `ProtectedChanges=0`。
- `LegacyOrFormalTreeChanges=0`。
- `MediaChanges=0`。

## 9. P1 Delivery Requirements

P1 完成後必須交付：

1. Commit SHA。
2. 完整變更檔案清單。
3. P1-01 至 P1-06 完成狀態。
4. 測試命令。
5. P0 62 項回歸測試結果。
6. P1 新增測試結果。
7. 未通過項目。
8. Recovery／Rollback 方式。
9. 受保護文件零修改證據。
10. Legacy／媒體／正式資產零接觸證據。
11. 外部 API、第三方套件與費用狀態。
12. P1 驗證報告。
13. P1 結論：`PASS`、`PASS_WITH_CONDITIONS` 或 `FAIL`。
14. 是否具備 P1 Acceptance Review 條件。

## 10. Explicit Prohibitions

- 執行 P2 或 P3。
- 修改或合併 `main`。
- `force push`、`force-with-lease`、`rebase`、`reset --hard`。
- amend 已發布 Commit。
- 修改、刪除、覆寫或繞過 P0 歷史、程式、Schema、測試或報告。
- 修改 Legacy、正式 Episode 資料或正式 Production State。
- 修改圖片、影片、音訊、Exact Asset，或生成／重繪替代品。
- 操作 Google Drive、Flow 或 CapCut。
- 使用付費 API。
- 安裝未核准第三方套件。
- 自行擴張規格或以未授權路徑寫入。
- 規格、路徑、測試或遠端歷史發生衝突時自行猜測。

## 11. Phase Gates

| Phase | Status |
|---|---|
| P1 | `AUTHORIZED`；精確路徑與一對一測試映射由兩份 remediation Addendum 核准，仍須 P1 Authorization Review PASS |
| P2 | `BLOCKED` |
| P3 | `BLOCKED` |

P2 只有在 P1 Acceptance Review 為 `PASS`，且新的正式 P2 授權生效後
才可開始。P3 仍須通過後續獨立 gate 與正式授權。

## 12. Stop Conditions

發生下列任一情況，必須立即停止且不得提交或 Push 未核准實作：

- Current Effective 規格之間存在衝突。
- Manifest 缺口或讀取白名單不完整。
- 缺少工作項目所需正式 Schema。
- 缺少 Test Plan 一對一對照或驗收標準。
- 嘗試寫入 Write Scope Addendum 核准範圍以外的路徑。
- P0 任一回歸測試失敗。
- Repository path governance 失敗或被繞過。
- Protected Artifact 發生異動。
- Legacy、媒體、Exact Asset、正式 Episode 或 Production State 發生異動。
- 實作需要付費 API、Drive／Flow／CapCut 操作。
- 實作需要未授權第三方套件。
- 遠端分支歷史、P0 Accepted Commit 或 branch base 不一致。
