# 20｜System Specification Lock Candidate Manifest V2.1 Draft

**狀態：DRAFT／NOT LOCKED**  
**Repository：`huao131/MATA-AI-VIDEO-STUDIO`；Branch：`review/v2-system-specification-publication-v2`；PR #2。**  
**取代關係：本版取代 `20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.0_DRAFT.md` 作為 Lock Review 的 Current Effective Manifest；舊檔保持不變。**

## 1. 強制讀取規則

Codex 只能讀取本 Manifest 列為 `effective_status=CURRENT_EFFECTIVE`、`codex_read_allowed=true` 且完成 SYSTEM SPECIFICATION LOCK V2.0 後的文件。歷史 Draft、未列入 Manifest 的文件，或 `codex_read_allowed=false` 的文件，不得作為實作依據。`CURRENT_EFFECTIVE` 是外部治理狀態，不是 Asset Lifecycle Status；本清單內文件在 Lock 前仍維持 `lifecycle_status=DRAFT`。

## 2. Lock Candidate 清單

| deliverable_id | responsibility | current_effective_filename | document_version | remote_path | source_content_commit | effective_status | lifecycle_status | evidence_status | superseded_documents | codex_read_allowed | lock_candidate |
|---|---|---|---|---|---|---|---|---|---|---:|---:|
| D01 | ChatGPT 製片中樞 | `13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D02 | Gemini 視覺／prompt | `14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D03 | Global MASTER SOP | `19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | `1dadff44448da8caf1e38c940c01a7f62ca6b752` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md`（僅取消其 D03 角色） | true | true |
| D04 | Workflow Schema | `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D05 | State／Gate | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D06 | GitHub 結構 | `16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D07 | Drive Asset System | `DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | `DRIVE_ASSET_SYSTEM_V2.0_DRAFT.md` | true | true |
| D08 | Tool Handoff | `17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D09 | QC／Recovery | `18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `docs/work/v2_drafts/18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | — | true | true |
| D10 | Portable Installation | `09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | `09_PORTABLE_INSTALLATION_GUIDE_V2_DRAFT.md` | true | true |
| D11 | Codex Backlog | `10_CODEX_BACKLOG_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/10_CODEX_BACKLOG_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | `10_CODEX_BACKLOG_V2_DRAFT.md` | true | true |
| D12 | Test Plan | `11_TEST_PLAN_V2.1_DRAFT.md` | V2.1 | `docs/work/v2_drafts/11_TEST_PLAN_V2.1_DRAFT.md` | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` | CURRENT_EFFECTIVE | DRAFT | VERIFIED | `11_TEST_PLAN_V2_DRAFT.md` | true | true |

## 3. Lock Review限制

`lock_candidate=true`只表示該文件具備 Lock Review資格，不表示已鎖定。SYSTEM SPECIFICATION LOCK V2.0明確通過前，全部文件保持DRAFT，PR維持Draft，不得合併`main`，也不得啟動Codex Implementation、Flow／CapCut操作或Legacy／正式資產異動。
