# MATA AI ORIGINAL VIDEO STUDIO OS V2.0｜WORK HANDOFF

**Phase:** Work Specification  
**Depends on:** `docs/product/MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2.0_PRODUCT_DEFINITION_FINAL.md`  
**Source of truth:** GitHub latest MASTER / SOP / LOCK / APPROVED  

## Work Role

你是 MATA AI ORIGINAL VIDEO STUDIO OS 的系統架構、流程設計與產品規格顧問。

你的任務不是重新發明產品，也不是直接寫程式，而是將已鎖定的產品定義與現有 GitHub 資料，整理成 Codex 可直接實作的完整系統規格。

## Mandatory Reading Order

1. PRODUCT DEFINITION FINAL V2.0
2. 最新 MASTER SOP
3. New Episode Workflow / Templates
4. Global QC 與版本規則
5. EP01 / EP02 的 LOCK、Production State、Asset Index
6. EP02 圖片與連戲失敗案例
7. Google Drive V2 資料治理與 Legacy Audit 規則

若舊資料與 PRODUCT DEFINITION LOCK 衝突：

- 不得自行改產品方向。
- 列出衝突、影響與建議。
- 等待 Mata老師決策。

## Product Constraints

- 原創優先，不得改成模板選擇器。
- 必須支援跨行業、跨系列。
- 一支影片一個獨立 Episode / Chat / State。
- GitHub 是正式規範與狀態來源。
- Google Drive 是媒體與資產資料庫。
- V1 使用現有訂閱工具，不以額外付費 API 為必要條件。
- ChatGPT / Gemini 為操作介面。
- Flow 由使用者使用自己的點數確認生成。
- 剪映採標準交接包，不假設可完全自動控制。
- LOCK / FINAL / MASTER / APPROVED 不得覆寫。
- 單集特殊規則不得升級成 Global Rule。

## Required Deliverables

### 1. `SYSTEM_ARCHITECTURE_V2.0.md`

定義：

- Global OS / Series / Episode 三層架構
- ChatGPT / Gemini 前端操作模式
- GitHub / Google Drive 雙資料層
- Stage 0–9 模組
- Human Gates
- 各模組依賴與資料流
- V1 與未來 API Adapter 邊界

### 2. `CHATGPT_PROJECT_INSTRUCTIONS_V2.0.md`

必須可直接安裝於 ChatGPT Project，包含：

- AI 製片中樞角色
- 原創優先規則
- 啟動命令
- Stage 0–9 狀態判定
- 何時讀 GitHub
- 何時讀 Production State
- 何時寫入 Drive / GitHub
- Gate 行為
- 重生、局部修改與版本行為
- 錯誤恢復
- 不可自行修改 LOCK 的限制

### 3. `GEMINI_GEM_INSTRUCTIONS_V2.0.md`

提供 Gemini Gem 可安裝版本，與 ChatGPT 共用同一狀態與資料規範，但需標示 Gemini / Flow 特有操作差異。

### 4. `WORKFLOW_SCHEMA_V2.0.md`

為每個 Stage 定義：

- 觸發條件
- 必要輸入
- 系統輸出
- 文件名稱
- Drive 路徑
- GitHub 路徑
- 狀態更新
- Human Gate
- 失敗與恢復

### 5. `PRODUCTION_STATE_MACHINE_V2.0.md`

定義完整合法狀態與轉移：

- INIT
- BRIEF_READY
- INSIGHT_READY
- CREATIVE_REVIEW
- CREATIVE_LOCKED
- STORY_REVIEW
- STORY_LOCKED
- VISUAL_REVIEW
- STORY_VISUAL_LOCKED
- KEYFRAME_PRODUCTION
- KEYFRAME_LOCKED
- FLOW_PRODUCTION
- PRODUCTION_LOCKED
- EDITING_HANDOFF
- FINAL_QC
- FINAL_APPROVED
- ARCHIVED
- BLOCKED / REVISION_REQUIRED / REGENERATE

列出每個狀態的進入條件、退出條件、允許動作、禁止動作與更新欄位。

### 6. `GITHUB_STRUCTURE_V2.0.md`

定義：

- Global OS 路徑
- Series 路徑
- Episode 路徑
- schemas / templates / scripts / docs / examples / tests
- LOCK 文件保護
- 命名規則
- 版本策略
- Release / Change Log

### 7. `DRIVE_ASSET_SYSTEM_V2.0.md`

定義：

- V2 根目錄
- 第一層五大資料夾
- 產業 → 系列 → Episode 三級分類
- 每個 Episode 的固定資料夾
- 每種資產存放位置
- Draft / Passed / Approved / Locked / Rejected / Archived 規則
- Asset Registry / Episode Registry / Prompt Database / Error Database
- Drive ID 與 GitHub 索引同步
- Legacy KEEP / MIGRATE / ARCHIVE / DELETE CANDIDATE

### 8. `TOOL_HANDOFF_SPEC_V2.0.md`

定義：

- ChatGPT → Gemini
- ChatGPT / Gemini → Drive
- Keyframe → Flow
- Flow Output → Drive
- Drive → Editing Package
- Editing Package → 剪映 / 其他剪輯軟體

每次交接需明確列出檔案、格式、命名、使用者動作與狀態回寫。

### 9. `QC_AND_RECOVERY_V2.0.md`

包括：

- Creative QC
- Story QC
- Visual Bible QC
- Keyframe QC
- Character / Scene / Prop / Lighting / Exact Asset / Ergonomics QC
- Flow Continuity QC
- Audio / Subtitle / Editing QC
- Final QC
- Rejected / Retry / Escalation
- Human Override
- 不可無限重生

### 10. `PORTABLE_INSTALLATION_GUIDE_V2.0.md`

定義夥伴安裝流程：

- 使用自己的 ChatGPT 或 Gemini
- 建立自己的 Drive V2 根目錄
- 複製 OS 指令與模板
- 初始化自己的 IDs / credentials / registries
- 不共用 Mata老師帳號與資產 ID
- 第一支示範影片啟動流程
- 升級與更新流程

### 11. `CODEX_IMPLEMENTATION_BACKLOG_V2.0.md`

按 P0 / P1 / P2 排序。

每項包含：

- 目的
- 影響檔案
- 新增 / 修改
- 輸入 / 輸出
- 依賴
- 測試方法
- 完成定義
- Commit 拆分建議
- 是否需要 Mata老師決策

P0：流程、狀態、模板、Lock、GitHub 結構。  
P1：Drive 分類、索引、交接包、SRT / Timeline。  
P2：Hard Gate、技術 QC、夥伴安裝包、範例與回歸測試。

### 12. `TEST_AND_ACCEPTANCE_PLAN_V2.0.md`

至少測試：

- 全新行業完整流程
- Hook 重生與混合
- Story 局部重生
- LOCK 保護
- 單集不污染其他 Episode
- Drive 正確分類
- Rejected 不進 Approved
- 工具能力不符時阻擋
- Flow Package
- SRT / Editing Package
- Legacy 資產不被誤刪
- ChatGPT / Gemini 雙環境安裝
- 無額外 API 的 V1 操作

## Work Output Gate

完成後，先提供：

1. 規格摘要
2. 產出文件清單
3. 現有系統衝突
4. 尚待 Mata老師決策的重大項目
5. Codex 可開始實作的 P0 清單

不得直接修改正式程式或覆寫 LOCK 文件。

## Acceptance Gate

Work 規格只有在以下條件全部通過後，才建立 `SYSTEM SPECIFICATION LOCK V2.0`：

- 忠實保留原創優先定位。
- 完整涵蓋 Stage 0–9。
- 每個階段有輸入、輸出、狀態、Drive 路徑與 Gate。
- 沒有把 V1 改成額外付費 API 平台。
- 沒有把 EP02 單集規則誤升為 Global Rule。
- Codex 可以不重新猜需求，直接按照 Backlog 實作。
