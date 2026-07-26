# 第一批跨文件一致性修正基準 V1.0｜草案

**狀態：DRAFT／NOT LOCKED**  
**審閱基準宣告：指定 Commit `fd5d011a980251514ff405973c36158556bdf9c9` 目前不在本機 Git 物件庫；本文件只記錄可讀工作樹與可解析 Commit `a44fbaae0f356172d9f4160782b8a2a5e9656ea7` 的修正需求。**

## 1. 效力與使用方式

本文件不是對任何舊 Draft 的原地覆寫，也不是 Lock／Final。它只列出下一版 Draft 必須採用的共同規則；在六份來源文件均以新檔名重出且完成同一份 Commit 的內容驗證前，第一批不得宣告 PASS、不得進入第二批審閱、不得建立、搬移、刪除或寫入 Google Drive 資產。

## 2. 統一用語與責任邊界

| 主題 | 強制共同規則 |
|---|---|
| GitHub | GitHub 保存可版本化的規格、程式、Register schema、可讀 Legacy 證據索引；其內容只有在來源路徑、Commit SHA 與內容雜湊可驗證時，才可作為 `VERIFIED` 證據。 |
| Google Drive | Google Drive 保存實體資料夾、媒體與交付物；資料夾以 `google_drive_folder_id` 定位，名稱不能取代 ID。 |
| 狀態證據 | `VERIFIED`＝可回讀正式來源且 ID／Commit／雜湊完整；`INFERRED`＝有旁證但未完成正式登錄；`UNVERIFIED`＝無可驗證來源；`CONFLICTED`＝來源互相矛盾或索引與實物不一致。只有 `VERIFIED` 可提出 Canonical State 候選；仍須 Gate／Register 決策，才可成為正式 Production State。 |
| 資產生命週期 | `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED` 為唯一受控值。不得以 `QC_PENDING`、`IN_REVIEW`、`CANDIDATE` 混入同一 lifecycle 欄位；候選性應放入 `evidence_status` 或外部 Register。 |
| Legacy | EP01、EP02 均只可作 Legacy／來源候選處理；不移動、不改名、不覆寫。`LOCK`／`FINAL`／`MASTER`／`APPROVED` 原檔永不回寫，`CURRENT_EFFECTIVE` 與 `SUPERSEDED` 僅寫外部 Register。 |

## 3. 共同 Canonical Folder Registry（七筆）

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | folder_purpose | allowed_content | prohibited_content | verification_status | verified_at |
|---|---|---|---|---|---|---|---|---|
| `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `MATA AI 原創影片製片系統 V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `ROOT_PARENT_NOT_IN_V2_SCOPE` | V2 唯一系統容器。 | 僅五大已登錄根目錄。 | 頂層檔案、Episode 直放、任何平行根。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |
| `GLOBAL_OS` | `01_全域系統規範` | `1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 全域規格與治理。 | 規格、SOP、治理、測試與安裝文件。 | Episode 原始媒體、Flow 輸出、平行 Global 目錄。 | `VERIFIED` | `2026-07-26T12:36:31+08:00` |
| `ORIGINAL_VIDEO_LIBRARY` | `02_原創影片資料庫` | `14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Series／Episode 資產容器。 | 已登錄 Series、Episode 與受控資產樹。 | 根層 `01_SERIES`、`02_EPISODES`、未審核共用副本。 | `VERIFIED` | `2026-07-26T12:36:32+08:00` |
| `SHARED_ASSET_LIBRARY` | `03_共用素材資料庫` | `1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 已核准跨集共用資產。 | Approved／Locked 共用資產與 Exact Asset 原檔。 | Episode 專屬資產、Rejected 資產、生成重繪 Exact Asset。 | `VERIFIED` | `2026-07-26T12:36:33+08:00` |
| `PRODUCTION_DATABASE` | `04_製片控制與索引` | `1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | State、Gate、Index、Register 與 QC 證據。 | 結構化登錄、不可覆寫事件、依賴與校驗。 | 原始大型媒體、聊天摘要、未驗證 ID 自動化輸出。 | `VERIFIED` | `2026-07-26T12:36:34+08:00` |
| `ARCHIVE` | `05_封存資料庫` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Legacy 與 Superseded 證據。 | 歷史快照、已取代版本、舊系統稽核。 | 新製片工作檔、對受保護檔的直接變更。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |
| `LEGACY_SYSTEM_AUDIT` | `01_舊系統稽核` | `1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | Legacy 只讀稽核證據。 | 只讀盤點、歷史路徑與交接資料。 | 新 V2 資產、移動、改名、覆寫或刪除 Legacy。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |

僅允許五大根目錄：`01_全域系統規範`、`02_原創影片資料庫`、`03_共用素材資料庫`、`04_製片控制與索引`、`05_封存資料庫`。禁止 `00_GLOBAL_OS`、`01_SERIES`、`02_EPISODES` 與任何中文／英文平行架構。

## 4. 證據歸屬修正

| 對象 | evidence_status | 可寫入 Canonical State？ | 強制處置 |
|---|---|---:|---|
| EP01 | `UNVERIFIED` | 否 | 不得賦予 Legacy、Ready 或 Revision Required 狀態；待提供正式路徑、Commit 與 Index。 |
| EP02 | `VERIFIED`（僅既有 Git 路徑／索引所載事實） | 僅該可回讀事實 | 不得以旁證覆寫既有 Git State。 |
| A2_V1.1 | `INFERRED` | 否 | 僅可建立外部 reconciliation candidate；須來源、雜湊、Drive ID、人工核對與依賴檢查。 |
| S1 Flow Package | `INFERRED` | 否 | 僅可作 Segment 候選；不得推定 Episode Ready 或 Flow Approved。 |
| B1_V2.0 | `UNVERIFIED` | 否 | 不歸屬 EP01 或 EP02。 |
| REVISION_REQUIRED | `UNVERIFIED`（作為既有 Legacy state） | 否 | 僅可於 V2 健康狀態 schema 定義，不能回填既有 Canonical State。 |

## 5. 依賴、Exact Asset 與 Rejected

`BRIEF → STORY → (VISUAL_BIBLE + STORYBOARD) → KEYFRAME → FLOW_MEDIA → EDIT → QC_EVIDENCE → FINAL_DELIVERY`；`STORY → AUDIO → EDIT` 為平行支線。只有直接上游 `APPROVED`／`LOCKED` 且 `dependency_check_status=PASSED` 才能流入下游；上游被 `REJECTED`／`SUPERSEDED` 或 MAJOR 升版，所有下游改為 `RECHECK_REQUIRED`。

Exact Asset 必須保留原始檔、來源、權利、Drive file ID 與 SHA-256；禁止生成式重繪、風格化、補畫與相似替代，輸出僅可後製置入或受控引用。Rejected 必須保有 ID、雜湊、理由與拒絕事件，隔離於已登錄 `REJECTED_QUARANTINE` 或 Archive 隔離區，不可進入 Approved、Shared、Exact、模型參考、剪輯預設或發布候選清單。

## 6. 必須新建的替代 Draft 檔

1. `01_WORK_SYSTEM_AUDIT_V1.2_DRAFT.md` 與 `02_EPISODE_EVIDENCE_STATE_TABLE_V1.1_DRAFT.md`：改用本文件第 2、4 節 evidence vocabulary，移除「高信心旁證」作為可用狀態的語意。
2. `03_V2_GOOGLE_DRIVE_CANONICAL_MAPPING_V1.1_DRAFT.md`、`07_FOLDER_REGISTRY_V2.1_DRAFT.md`、`DRIVE_ASSET_SYSTEM_V2.1_DRAFT.md`：完整採本文件第 3 節九欄與 `VERIFIED` vocabulary，不得使用 `VERIFIED_CANONICAL` 作為 evidence_status。
3. `08_ASSET_INDEX_AND_IDENTITY_SCHEMA_V2.1_DRAFT.md`：補足九欄 Folder Registry 引用、`evidence_status`、七個 lifecycle 受控值、`REJECTED`、Exact Asset、dependency 與 Legacy mapping 規則。

新 Draft 必須在同一可解析 Git Commit 中提交後，才可重做第一批審閱；本修正草案本身不改變任何 Production State、Drive 結構或受保護資產。
