# 20｜System Specification Lock Candidate Manifest V2.0 Draft

**狀態：DRAFT／NOT LOCKED**  
**Repository：`huao131/MATA-AI-VIDEO-STUDIO`；Branch：`review/v2-system-specification-publication-v2`；PR #2。**

## 1. 強制讀取規則

Codex 只能讀取本 Manifest 列為 `CURRENT_EFFECTIVE` 且 `codex_read_allowed=true` 的文件。任何歷史 Draft、未列入 Manifest 的文件或 `codex_read_allowed=false` 文件，均不得作為實作依據。舊文件不回寫 `SUPERSEDED`；取代關係僅記錄於本 Manifest 與 Version／Lock Register。

## 2. Lock Candidate 清單

| deliverable_id | responsibility | current_effective_filename | document_version | remote_path | remote_commit | lifecycle_status | evidence_status | superseded_documents | codex_read_allowed | lock_candidate |
|---|---|---|---|---|---|---|---|---|---:|---:|
| D01 | ChatGPT 製片中樞 | `13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D02 | Gemini 視覺／prompt | `14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D03 | Global MASTER SOP | `19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | `PENDING_THIS_COMMIT` | CURRENT_EFFECTIVE | VERIFIED | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` (D03 role only) | true | true |
| D04 | Workflow Schema | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D05 | State／Gate | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D06 | GitHub 結構 | `16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D07 | Drive Asset System | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | `DRIVE_ASSET_SYSTEM_V2.0_DRAFT.md` | true | true |
| D08 | Tool Handoff | `17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D09 | QC／Recovery | `18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | — | true | true |
| D10 | Portable Installation | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | `09_PORTABLE_INSTALLATION_GUIDE_V2_DRAFT.md` | true | true |
| D11 | Codex Backlog | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/10_CODEX_BACKLOG_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | `10_CODEX_BACKLOG_V2_DRAFT.md` | true | true |
| D12 | Test Plan | `11_TEST_PLAN_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/11_TEST_PLAN_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | VERIFIED | `11_TEST_PLAN_V2_DRAFT.md` | true | true |

## 3. Review 限制

`lock_candidate=true` 表示可接受 Lock Review，不表示已 Lock。只有審查明確通過後，才可由新 Register event 將對應版本設為 LOCKED；本 Manifest 及所有文件在此之前保持 Draft。提交本 Manifest 的 commit SHA 必須回填所有 `PENDING_THIS_COMMIT` 欄位，並同步更新 V1.4 Crosswalk 與 V1.1 Integration Review 的 remote head。
