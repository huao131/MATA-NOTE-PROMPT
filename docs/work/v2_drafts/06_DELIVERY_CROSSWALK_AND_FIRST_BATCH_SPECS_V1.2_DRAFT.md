# Delivery Crosswalk and 12 Deliverables V1.2｜第三批草案

**狀態：DRAFT／NOT LOCKED**  
**第三批基準：`c1ef8d0f3dfa54570b93e77e112ead7cb96232b5`（Local-only）**  
**限制：本文件不解除 Repository Publication Gate，不授權 SYSTEM SPECIFICATION LOCK V2.0、Codex Implementation、Flow 操作或任何 Legacy／正式資產異動。**

## 1. 共通判定規則

- `current_status`：`DRAFT_AVAILABLE`、`LEGACY_BASELINE_ONLY` 或 `GAP`；`GAP` 表示尚無符合 V2 的獨立交付，不得以「已涵蓋」取代。
- `evidence_status` 僅用 `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`。非 `VERIFIED` 不能寫入 Canonical Production State；本 Crosswalk 對文件存在性的證據為 Git Local Commit，並非遠端發布證據。
- GitHub 保存規格、Schema、State、Gate、Register、Index 與稽核證據；Google Drive 保存大型實體資產，File／Folder ID 與 metadata 回寫 GitHub Index。Drive 名稱不是主鍵。
- `implementation_required=YES` 只代表未來實作前置需求，絕不授權現在開始寫程式。

## 2. 十二項正式交付 Crosswalk

| deliverable_id | stable_filename | document_title_zh_TW | responsibility_scope | input_sources | output_definition | dependencies | acceptance_criteria | current_status | evidence_status | canonical_owner | implementation_required |
|---|---|---|---|---|---|---|---|---|---|---|---:|
| D01 | `CHATGPT_PROJECT_INSTRUCTIONS_V2_DRAFT.md` | ChatGPT Project Instructions | ChatGPT 專案行為、輸入輸出與 Lock 邊界。 | Product Definition、MASTER SOP、V2治理規格。 | 可獨立匯入的 V2 Instructions。 | D03、D04、D05、D07。 | 獨立文件、V2 Gate／Evidence／Lock 一致、無未授權工具控制。 | `GAP` | `UNVERIFIED` | GitHub／Global OS | YES |
| D02 | `GEMINI_GEM_INSTRUCTIONS_V2_DRAFT.md` | Gemini Gem Instructions | Gemini Gem 的提示、交接與限制。 | D03、D04、D08、D09。 | 可獨立匯入的 Gem Instructions。 | D03、D04、D08、D09。 | 獨立文件、不得假設控制 Flow、Exact Asset 與 Rejected 規則一致。 | `GAP` | `UNVERIFIED` | GitHub／Global OS | YES |
| D03 | `MASTER_EXECUTION_SPEC_V1.0_FINAL_LOCK.md` | 全域 MASTER SOP | V1 全域製片流程基礎。 | 既有系統文件。 | 已鎖定 V1 SOP。 | 既有 Legacy 系統。 | 只讀引用；不得宣稱為已升級 V2。 | `LEGACY_BASELINE_ONLY` | `VERIFIED` | GitHub／Legacy read-only | YES |
| D04 | `WORKFLOW_SCHEMA_V2_DRAFT.md` | 工作流程 Schema | V2 端到端資料與交接 Schema。 | D03、D05、D07、D08。 | 受控 V2 Workflow Schema。 | D05、D07、D08。 | 獨立文件、可驗證欄位與交接邊界。 | `GAP` | `UNVERIFIED` | GitHub／Global OS | YES |
| D05 | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | Production State Machine | Episode／Segment／Asset 狀態與六個 Gate。 | 01、02、05、08、Drive Asset System。 | Canonical State 與 Gate Register schema。 | Evidence、Version／Lock、Dependency。 | 六 Gate 名稱固定；非 VERIFIED 不得寫入；Segment Ready 不推升 Episode。 | `DRAFT_AVAILABLE` | `VERIFIED` | GitHub／Production Database | YES |
| D06 | `GITHUB_REPOSITORY_STRUCTURE_V2_DRAFT.md` | GitHub Repository Structure | V2 repo 目錄、治理資料位置與保護策略。 | 現有 repo、D05、D10、D11。 | 可遷移的 V2 結構規格。 | Publication Gate、D04、D10。 | 獨立文件；不搬移 Legacy；定義受保護檔與 register 位置。 | `GAP` | `UNVERIFIED` | GitHub／Global OS | YES |
| D07 | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | Google Drive Asset System | Folder Registry、資產分類、ID、Exact Asset、Rejected 隔離。 | 03、07、08、DRIVE_ASSET_SYSTEM。 | V2 Drive 資產治理規格。 | Folder Registry、Asset Index。 | 以 ID 定位；七筆 Mapping 一致；無平行架構；Legacy 唯讀。 | `DRAFT_AVAILABLE` | `VERIFIED` | GitHub spec + Google Drive physical assets | YES |
| D08 | `TOOL_HANDOFF_SPECIFICATION_V2_DRAFT.md` | Tool Handoff Specification | ChatGPT、Gemini、Flow、Canva、CapCut 的交接契約。 | D03、D04、D07、既有 `FLOW_EDITING_HANDOFF_SPEC_V1.0.md`。 | V2 工具輸入／輸出／責任界線。 | D01、D02、D04、D07。 | 獨立文件；不得假設 Codex 可控制 Flow 或 CapCut；帳號責任清楚。 | `GAP` | `UNVERIFIED` | GitHub／Global OS | YES |
| D09 | `QC_AND_RECOVERY_SPECIFICATION_V2_DRAFT.md` | QC and Recovery Specification | QC、阻塞、Rollback、Recovery 規格。 | D05、D07、D11、既有 `QC_GATE_SPEC_V1.0.md`。 | V2 可執行復原規格。 | D05、D07、D11。 | 獨立文件；涵蓋衝突、缺 ID、Lock、Dependency Recovery。 | `GAP` | `UNVERIFIED` | GitHub／Production Database | YES |
| D10 | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | Portable Installation Guide | 新使用者獨立安裝與安全停止。 | D07、D08、D11。 | 可攜安裝／映射／驗證流程。 | Folder Registry、工具帳號。 | 不沿用 Mata Drive ID；不自動重複建立；測試不可寫正式 State。 | `DRAFT_AVAILABLE` | `VERIFIED` | GitHub／Global OS | YES |
| D11 | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | Codex Implementation Backlog | 未來階段化實作需求。 | D04、D05、D07、D09、D10。 | P0–P3 的非程式 Backlog。 | Publication Gate、Lock、D04、D09。 | 每項含輸入、輸出、依賴、驗收、禁止、API、風險。 | `DRAFT_AVAILABLE` | `VERIFIED` | GitHub／Global OS | YES |
| D12 | `11_TEST_PLAN_V2.1_DRAFT.md` | Test and Acceptance Plan | 結構、狀態、版本、資產、Recovery 驗收。 | D05、D07、D10、D11。 | 可重複執行的測試案例。 | Schema、Registry、Index、Register。 | 每例具八個必填欄位；覆蓋指定阻塞情境。 | `DRAFT_AVAILABLE` | `VERIFIED` | GitHub／Production Database | YES |

## 3. 完整性結果與引用矩陣

| 批次／文件群 | 對第三批提供的規則 | 第三批引用文件 |
|---|---|---|
| 第一批：01、02、03、07、08、Drive Asset System | Evidence 四值、Folder Registry／七筆 Mapping、Asset ID／Exact Asset／Rejected／Legacy 邊界。 | 06、09、10、11 |
| 第二批：04、05 | 六 Gate、Canonical State、Lifecycle、Version／Lock、Supersession、Dependency Recheck。 | 06、09、10、11 |
| 第三批：06、09、10、11 | 12項交付缺口、可攜安裝、未來實作分期、驗收測試。 | 全系統整合審查輸入 |

**完整性判定：12 項中 5 項 `DRAFT_AVAILABLE`、1 項 `LEGACY_BASELINE_ONLY`、6 項 `GAP`。** 因此第三批文件內容可供審閱，但「全系統12項交付已完整」不可宣稱 PASS；缺口須在 FULL SYSTEM INTEGRATION REVIEW 建立處置決策。
