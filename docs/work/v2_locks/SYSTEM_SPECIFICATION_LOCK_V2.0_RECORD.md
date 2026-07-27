# SYSTEM SPECIFICATION LOCK V2.0｜正式鎖定紀錄

**Lock ID：** `SYS-SPEC-LOCK-V2.0-20260726-001`  
**Scope：** `GLOBAL / MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2`  
**Status：** `LOCKED`  
**Evidence Status：** `VERIFIED`  
**Approved by：** Mata老師  
**Approved at：** `2026-07-26T23:03:10+08:00`  
**Repository：** `huao131/MATA-AI-VIDEO-STUDIO`  
**Publication Branch：** `review/v2-system-specification-publication-v2`  
**Pull Request：** `#2`  
**Locked Remote Head：** `b2215507075b9f90c02f4c6b992a7285a0956d99`

## 1. 鎖定決議

Mata老師已明確核准建立 `SYSTEM SPECIFICATION LOCK V2.0`。本紀錄將下列十二項 Current Effective 規格固定為 MATA AI ORIGINAL VIDEO STUDIO OS V2 的正式實作基準。

此 Lock 只固定規格；不等同合併 `main`、不自動授權 Codex Implementation，也不授權 Flow／CapCut 操作、Legacy 搬移、刪除或正式資產異動。

## 2. Current Effective 交付清單

| ID | Current Effective 文件 | 版本 | 內容來源 Commit |
|---|---|---|---|
| D01 | `docs/work/v2_drafts/13_CHATGPT_PROJECT_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D02 | `docs/work/v2_drafts/14_GEMINI_GEM_INSTRUCTIONS_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D03 | `docs/work/v2_drafts/19_GLOBAL_MASTER_SOP_V2.0_DRAFT.md` | V2.0 | `1dadff44448da8caf1e38c940c01a7f62ca6b752` |
| D04 | `docs/work/v2_drafts/15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D05 | `docs/work/v2_drafts/04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` | V2.1 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D06 | `docs/work/v2_drafts/16_GITHUB_REPOSITORY_STRUCTURE_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D07 | `docs/work/v2_drafts/DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | V2.1 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D08 | `docs/work/v2_drafts/17_TOOL_HANDOFF_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D09 | `docs/work/v2_drafts/18_QC_AND_RECOVERY_SPECIFICATION_V2.0_DRAFT.md` | V2.0 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D10 | `docs/work/v2_drafts/09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md` | V2.1 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D11 | `docs/work/v2_drafts/10_CODEX_BACKLOG_V2.1_DRAFT.md` | V2.1 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |
| D12 | `docs/work/v2_drafts/11_TEST_PLAN_V2.1_DRAFT.md` | V2.1 | `4cbd60675c1cfbb9cd141c58d9903cd2911b2c6b` |

## 3. 治理依據

- Current Effective Manifest：`docs/work/v2_drafts/20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.1_DRAFT.md`
- Current Effective Crosswalk：`docs/work/v2_drafts/06_DELIVERY_CROSSWALK_AND_FIRST_BATCH_SPECS_V1.5_DRAFT.md`
- Current Effective Integration Review：`docs/work/v2_drafts/12_FULL_SYSTEM_INTEGRATION_REVIEW_V1.2_DRAFT.md`
- Register Event：`docs/work/v2_registers/SYSTEM_SPECIFICATION_LOCK_REGISTER_V2.0.json`
- PR Review Evidence：PR #2 的 `SYSTEM SPECIFICATION LOCK V2.0 REVIEW — RECHECK`，結論 `PASS`

## 4. 鎖定後保護規則

1. 上述十二項文件的鎖定內容不得原地覆寫、改名、移動或刪除。
2. 後續修正必須建立新版本，例如 V2.1、V2.2 或 V3.0，並建立新的 Register Event。
3. 取代關係只寫入外部 Version／Lock Register，不回寫既有文件。
4. 任何上游規格改版均須觸發 `DEPENDENCY_RECHECK_REQUIRED`，重新檢查 Codex Backlog、Schema、Test Plan 與下游實作。
5. 歷史 Draft 不得被 Codex 作為實作依據；Codex僅可讀取 Manifest V2.1白名單中的 Current Effective 文件。
6. `Segment Ready`不得推升`Episode Ready`；非`VERIFIED`證據不得寫入Canonical Production State。
7. Exact Asset不得由生成式AI重繪或替代；Rejected資產不得成為任何正式Reference或下游依賴。

## 5. 尚未授權事項

- `CODEX IMPLEMENTATION`：未授權
- 合併PR #2至`main`：未授權
- Flow或CapCut操作：未授權
- Legacy搬移、刪除、覆寫：未授權
- 正式媒體與Exact Asset異動：未授權

## 6. 下一個必要Gate

下一步為建立獨立的 `CODEX IMPLEMENTATION AUTHORIZATION`，明確指定：

- Codex允許讀取的Manifest版本與Remote Head
- 實作Branch
- P0/P1/P2/P3執行範圍
- 禁止事項
- 測試與驗收條件
- 是否允許合併`main`

在該授權成立前，Codex不得開始任何實作。
