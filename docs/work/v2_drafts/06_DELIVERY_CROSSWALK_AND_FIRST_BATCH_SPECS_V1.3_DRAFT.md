# Delivery Crosswalk and 12 Deliverables V1.3｜整合後草案

**狀態：DRAFT／NOT LOCKED**  
**整合基準：`d1aa27ef77933c11683e06b7bc0af333782a99dc`；本版 Commit 於提交前為 `PENDING_LOCAL_COMMIT`。**  
**限制：所有交付僅為 Local Review Draft；Repository Publication Gate 仍為 `BLOCKED`。**

## 12 項正式 V2 交付

| ID | 正式 V2 Draft | Commit 追溯 | 狀態 | V2 對應與驗收摘要 |
|---|---|---|---|---|
| D01 | `13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | AI 製片中樞、獨立 Chat、Gate／Lock／Evidence 邊界。 |
| D02 | `14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | 視覺／prompt／Flow 前置、continuity、metadata 回寫。 |
| D03 | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | V2 流程正式對應；V1 MASTER SOP 只讀基線，不再是 GAP。 |
| D04 | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | Stage 0 至 Final、欄位、Gate、阻塞、Recovery。 |
| D05 | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | `c1ef8d0f…` | `DRAFT_AVAILABLE` | State、Evidence、六 Gate 與 Ready 隔離。 |
| D06 | `16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | specs／schemas／registries／episodes／templates／tests 及 Legacy 唯讀。 |
| D07 | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | `4e1182f3…` | `DRAFT_AVAILABLE` | ID 為主、Exact、Rejected、Drive 物理資產。 |
| D08 | `17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | 所有工具交接、人工 Gate、無自動控制。 |
| D09 | `18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | 本共同 Local Commit | `DRAFT_AVAILABLE` | QC、disposition、衝突、rollback／recovery。 |
| D10 | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | `d1aa27ef…` | `DRAFT_AVAILABLE` | 可攜安裝、獨立帳號 Mapping、停止規則。 |
| D11 | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | `d1aa27ef…` | `DRAFT_AVAILABLE` | 未來 Backlog；不啟動實作、不控 Flow／CapCut。 |
| D12 | `11_TEST_PLAN_V2.1_DRAFT.md` | `d1aa27ef…` | `DRAFT_AVAILABLE` | 結構、狀態、版本、資產與 Recovery 驗收。 |

## 追溯與完整性

- 所有 D01–D12 都有至少一份獨立或明確對應的正式 V2 Draft，`GAP=0`。
- D03 與 D04 共用 Workflow Schema，但責任不同：D03 是 V2 全域流程／V1 基線替代，D04 是機器可驗證的 workflow schema 契約；同一文件以明確章節承擔兩個可追溯交付。
- 共同約束：Evidence 四值、Lifecycle 七值、六 Gate、Version／Lock Register、Dependency Recheck、Exact Asset、Rejected isolation、Legacy 唯讀與 GitHub／Drive 邊界均引用前批已通過規則。
- `DRAFT_AVAILABLE` 不等同 published、locked、implemented 或可控制外部工具。發布完成前，Commit 只能稱 `LOCAL_ONLY`。

**整合後 Crosswalk 結論：12 項均為 `DRAFT_AVAILABLE`，無交付 GAP；可進入 Repository Publication Gate 修復評估。**
