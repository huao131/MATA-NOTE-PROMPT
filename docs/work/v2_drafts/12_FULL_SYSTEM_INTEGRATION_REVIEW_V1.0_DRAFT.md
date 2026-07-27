# Full System Integration Review V1.0｜整合審查草案

**狀態：DRAFT／NOT LOCKED**  
**整合基準 Commit：`d1aa27ef77933c11683e06b7bc0af333782a99dc`（LOCAL_ONLY）**  
**限制：Repository Publication Gate 仍為 `BLOCKED`；本審查不授權 Lock、Codex 實作、Flow／CapCut 操作或 Legacy／正式資產異動。**

## 1. 納入審查文件與來源

| 批次 | 文件 | 版本 | Commit 來源 |
|---|---|---|---|
| 第一批 | `00_FIRST_BATCH_REMEDIATION_V1.0_DRAFT.md`、`01_WORK_SYSTEM_AUDIT_V1.2_DRAFT.md`、`02_EPISODE_EVIDENCE_STATE_TABLE_V1.1_DRAFT.md` | V1.0／V1.2／V1.1 | `4e1182f3…` |
| 第一批 | `03_V2_GOOGLE_DRIVE_CANONICAL_MAPPING_V1.1_DRAFT.md`、`07_FOLDER_REGISTRY_V2.1_DRAFT.md`、`08_ASSET_INDEX_AND_IDENTITY_SCHEMA_V2.1_DRAFT.md`、`DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md` | V1.1／V2.1 | `4e1182f3…` |
| 第二批 | `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md`、`05_VERSION_AND_LOCK_REGISTER_V2.1_DRAFT.md` | V2.1 | `c1ef8d0f…` |
| 第三批 | `06_DELIVERY_CROSSWALK_AND_FIRST_BATCH_SPECS_V1.2_DRAFT.md`、`09_PORTABLE_INSTALLATION_GUIDE_V2.1_DRAFT.md`、`10_CODEX_BACKLOG_V2.1_DRAFT.md`、`11_TEST_PLAN_V2.1_DRAFT.md` | V1.2／V2.1 | `d1aa27ef…` |
| 只讀基線 | Product Definition、MASTER SOP、既有 Legacy／LOCK／FINAL／MASTER／APPROVED | 現存版本 | 只讀引用；不可由本審查改寫 |

## 2. 跨文件一致性矩陣

| 審查面向 | 統一結果 | 主要依據 | 影響 |
|---|---|---|---|
| Product Definition 核心定位 | 原創優先、跨行業、使用者自有資源、無額外付費 API 優先，無衝突。 | 01、06、09、10 | 無 |
| Global／Series／Episode | Global 在 `GLOBAL_OS`；Series／Episode 在 `ORIGINAL_VIDEO_LIBRARY`，Legacy 不升格。 | 03、07、04、09 | 無 |
| GitHub／Drive 邊界 | GitHub 保存版本化規格、State、Register、Index；Drive 保存實體媒體及 ID 回寫。 | 01、04、05、08、09 | 無 |
| Drive 五大根目錄 | 五個繁中正式名稱、stable code 與 Drive ID 分離，無平行 root。 | 03 V1.1、07 V2.1 | 無 |
| Evidence／Lifecycle／Production State | 三者分欄；Evidence 四值、Lifecycle 七值、State 依 scope 分開。 | 01、02、04、05、08 | 無 |
| 六個 Gate | 固定順序：creative、story、story_visual、keyframe、production、final。 | 04、05、11 | 無 |
| Version／Lock | 保護原檔不覆寫；以新版本及外部 Register 建立 supersession。 | 05、08、09、11 | 無 |
| Asset Identity／Exact／Rejected | ID＋Drive File ID＋checksum；Exact 不重繪；Rejected 隔離且不可作 reference。 | 07、08、11 | 無 |
| Dependency／Ready | 上游變更觸發 recheck；Segment Ready 不推升 Episode Ready。 | 04、05、10、11 | 無 |
| Legacy／Portable Installation | Legacy 唯讀；新帳號不可沿用 Mata Drive ID；測試隔離。 | 01、07、09 | 無 |
| Codex／工具邊界 | 無額外 API 為預設；Codex 不直接控制 Flow 或 CapCut。 | 09、10、11 | 無 |
| 12 項交付 | V1.2 有 D01、D02、D04、D06、D08、D09 GAP；本批 13–18 對應補齊。 | 06 V1.2 | 需新 V1.3 Crosswalk |

## 3. 名詞與枚舉值統一表

| 類別 | 受控值／定義 |
|---|---|
| `evidence_status` | `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`；僅 VERIFIED 可支撐 Canonical 事實。 |
| `lifecycle_status` | `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED`。 |
| Gate status | `NOT_STARTED`、`PENDING`、`PASS`、`FAIL`、`BLOCKED`、`SUPERSEDED`。 |
| Dependency | `NOT_EVALUATED`、`PASS`、`FAIL`、`DEPENDENCY_RECHECK_REQUIRED`、`BLOCKED_BY_UPSTREAM`。 |
| Episode status | `NOT_STARTED`、`IN_PROGRESS`、`REVISION_REQUIRED`、`READY`、`APPROVED`、`CLOSED`、`NOT_EVALUATED`。 |
| Segment status | `NOT_STARTED`、`IN_PROGRESS`、`REVISION_REQUIRED`、`READY`、`APPROVED`、`NOT_EVALUATED`。 |
| QC disposition | `APPROVED`、`APPROVED_WITH_EDIT`、`REGENERATE`、`REBUILD_SEGMENT`；不是 lifecycle 值。 |

## 4. 發現、缺口與修正建議

| ID | 發現／缺口 | 上下游影響 | 修正 |
|---|---|---|---|
| I-01 | D03 在 V1.2 僅列為 Legacy MASTER SOP，未有 V2 正式對應。 | 影響 D01、D04、D08 的流程來源。 | 以 `15_WORKFLOW_SCHEMA_V2.0_DRAFT.md` 作 D03 的 V2 可執行對應；V1 僅做只讀基線。 |
| I-02 | 六項 GAP 尚無獨立文件。 | 阻塞 Crosswalk 完整性，亦阻塞未來實作。 | 建立 13–18；不改動前批文件。 |
| I-03 | 部分舊版 Draft 使用 `VERIFIED_CANONICAL`。 | 僅舊版本；若被誤引用會混淆 Evidence。 | 僅引用 V1.1／V2.1 文件；不覆寫舊版。 |
| I-04 | Publication Gate 仍 BLOCKED。 | 所有 Local Commit 不能宣稱遠端發布。 | 另行做 Publication Gate 修復；不屬本批寫入範圍。 |

## 5. 整合結論

新增 13–18 與 06 V1.3 後，規格語意為 **PASS**：12 項交付均有明確 V2 Draft 與 Local Commit 可追溯，且無未解決的規格衝突。系統治理狀態仍為 **PASS_WITH_CONDITIONS**：所有文件仍為 Draft／LOCAL_ONLY，Repository Publication Gate 未解除。因此可進入「Repository Publication Gate 修復評估」，但不得進入 SYSTEM SPECIFICATION LOCK V2.0 或 Codex Implementation。
