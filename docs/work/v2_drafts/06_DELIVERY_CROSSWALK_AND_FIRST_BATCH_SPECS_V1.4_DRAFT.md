# Delivery Crosswalk and 12 Deliverables V1.4｜發布後追溯草案

**狀態：DRAFT／NOT LOCKED**  
**Remote Repository：`huao131/MATA-AI-VIDEO-STUDIO`**  
**Publication Branch：`review/v2-system-specification-publication-v2`；PR：#2；發布基準 Remote Head：`4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b`。**  
**Repository Publication Gate：`PASS`。本文件不授權 SYSTEM SPECIFICATION LOCK V2.0 或 Codex Implementation。**

| ID | 唯一正式 V2 對應 | 職責 | 發布／驗證結果 |
|---|---|---|---|
| D01 | `13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | ChatGPT 製片中樞與 Chat 邊界 | `DRAFT_AVAILABLE` |
| D02 | `14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | 視覺／prompt 與 Flow 前置交接 | `DRAFT_AVAILABLE` |
| D03 | `19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | 唯一全域 MASTER SOP | `DRAFT_AVAILABLE` |
| D04 | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | 僅機器可驗證 workflow schema 附屬規格 | `DRAFT_AVAILABLE` |
| D05 | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | State、Evidence、六 Gate | `DRAFT_AVAILABLE` |
| D06 | `16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | GitHub 結構與 Legacy 唯讀 | `DRAFT_AVAILABLE` |
| D07 | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | Drive 資產、Exact 與 Rejected | `DRAFT_AVAILABLE` |
| D08 | `17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | 工具人工交接邊界 | `DRAFT_AVAILABLE` |
| D09 | `18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | QC、Recovery、Disposition | `DRAFT_AVAILABLE` |
| D10 | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | 可攜安裝與帳號隔離 | `DRAFT_AVAILABLE` |
| D11 | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | 未來實作 Backlog 與禁止範圍 | `DRAFT_AVAILABLE` |
| D12 | `11_TEST_PLAN_V2.1_DRAFT.md` | 驗收測試計畫 | `DRAFT_AVAILABLE` |

## 重新驗證結論

1. D03 僅由 `19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` 承擔；`15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` 不再同時取代或承擔 Global MASTER SOP。
2. D04 僅由 `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` 承擔，作為 MASTER SOP 的機器可驗證附屬規格。
3. 十二項交付均已有單一責任對應、遠端發布追溯與 Lock Candidate Manifest 對照，重新驗證 `GAP=0`。
4. `DRAFT_AVAILABLE`、Repository Publication Gate PASS 均不等同 Lock、實作、Flow／CapCut 操作或 main 合併。
