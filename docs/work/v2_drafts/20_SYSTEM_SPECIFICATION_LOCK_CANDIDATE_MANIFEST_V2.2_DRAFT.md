# 20｜System Specification Lock Candidate Manifest V2.2 Draft

**狀態：DRAFT／LOCKED BY PARENT LOCK + ADDENDUM**  
**Repository：** `huao131/MATA-AI-VIDEO-STUDIO`  
**Branch：** `review/v2-system-specification-publication-v2`  
**Parent Lock：** `SYS-SPEC-LOCK-V2.0-20260726-001`  
**Addendum：** `SYS-SPEC-LOCK-V2.0-ADDENDUM-20260727-001`

## 1. 強制讀取規則

Codex只能讀取本Manifest列為`CURRENT_EFFECTIVE`且`codex_read_allowed=true`的文件。D01–D12維持原責任；S01、S02為P0 Supporting Contracts，不新增正式Deliverable編號。

## 2. Current Effective Deliverables

| ID | 文件 | 版本 | effective_status | lifecycle_status | evidence_status | codex_read_allowed |
|---|---|---|---|---|---|---:|
| D01 | `docs/work/v2_drafts/13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D02 | `docs/work/v2_drafts/14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D03 | `docs/work/v2_drafts/19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D04 | `docs/work/v2_drafts/15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D05 | `docs/work/v2_drafts/04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | V2.1 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D06 | `docs/work/v2_drafts/16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D07 | `docs/work/v2_drafts/DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | V2.1 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D08 | `docs/work/v2_drafts/17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D09 | `docs/work/v2_drafts/18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D10 | `docs/work/v2_drafts/09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | V2.1 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D11 | `docs/work/v2_drafts/10_CODEX_BACKLOG_V2.1_DRAFT.md` | V2.1 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| D12 | `docs/work/v2_drafts/11_TEST_PLAN_V2.1_DRAFT.md` | V2.1 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |

## 3. P0 Supporting Contracts

| ID | 文件 | 版本 | responsibility | effective_status | lifecycle_status | evidence_status | codex_read_allowed |
|---|---|---|---|---|---|---|---:|
| S01 | `docs/work/v2_drafts/07_FOLDER_REGISTRY_V2.1_DRAFT.md` | V2.1 | Folder Registry唯一正式定義與七筆Folder契約 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |
| S02 | `docs/work/v2_drafts/08_ASSET_INDEX_AND_IDENTITY_SCHEMA_V2.1_DRAFT.md` | V2.1 | Asset Index、Identity、Exact Asset、Rejected與Dependency契約 | CURRENT_EFFECTIVE | LOCKED | VERIFIED | true |

## 4. Codex限制

1. P0實作必須同時依D01–D12與S01–S02。
2. S01、S02只解除Folder Registry與Asset Index白名單缺口，不擴大P0功能邊界。
3. 不得讀取其他歷史Draft作為實作依據。
4. 不得進入P1、P2、P3。
5. 不得修改main、Legacy、媒體、Exact Asset，亦不得操作Drive、Flow或CapCut。
