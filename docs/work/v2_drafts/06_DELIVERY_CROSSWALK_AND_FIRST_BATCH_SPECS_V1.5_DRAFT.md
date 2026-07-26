# Delivery Crosswalk and 12 Deliverables V1.5｜Lock Review追溯草案

**狀態：DRAFT／NOT LOCKED**  
**Remote Repository：`huao131/MATA-AI-VIDEO-STUDIO`**  
**Publication Branch：`review/v2-system-specification-publication-v2`；PR：#2。**  
**Repository Publication Gate：PASS。Lock Candidate Manifest：`20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.1_DRAFT.md`。**

| ID | 唯一正式V2對應 | 職責 | Lock Review狀態 |
|---|---|---|---|
| D01 | `13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | ChatGPT製片中樞與Chat邊界 | LOCK_CANDIDATE |
| D02 | `14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | 視覺／prompt與Flow前置交接 | LOCK_CANDIDATE |
| D03 | `19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | 唯一Global MASTER SOP | LOCK_CANDIDATE |
| D04 | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | 機器可驗證Workflow Schema | LOCK_CANDIDATE |
| D05 | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | State、Evidence與六Gate | LOCK_CANDIDATE |
| D06 | `16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | GitHub結構與Legacy唯讀 | LOCK_CANDIDATE |
| D07 | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | Drive資產、Exact與Rejected | LOCK_CANDIDATE |
| D08 | `17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | 工具人工交接邊界 | LOCK_CANDIDATE |
| D09 | `18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | QC、Recovery與Disposition | LOCK_CANDIDATE |
| D10 | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | 可攜安裝與帳號隔離 | LOCK_CANDIDATE |
| D11 | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | Codex實作Backlog與禁止範圍 | LOCK_CANDIDATE |
| D12 | `11_TEST_PLAN_V2.1_DRAFT.md` | 驗收測試計畫 | LOCK_CANDIDATE |

## 再驗證結論

1. D03只由`19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md`承擔；D04只由`15_WORKFLOW_SCHEMA_V2.0_DRAFT.md`承擔。
2. 12項交付均有唯一Current Effective對應，`GAP=0`。
3. Current Effective與Lifecycle已分欄：Lock前文件Lifecycle仍為DRAFT。
4. Codex只有在SYSTEM SPECIFICATION LOCK V2.0明確通過後，才能依Manifest V2.1中`codex_read_allowed=true`的清單讀取；歷史Draft不得作為實作依據。
5. 本文件不授權合併`main`、Codex Implementation、Flow／CapCut操作或Legacy／正式資產異動。
