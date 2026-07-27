# Drive Asset System V2.0 Draft

**文件狀態：DRAFT／NOT LOCKED**
**適用範圍：所有 V2 Series、Episode、Shared Asset 與 Archive 資產**
**Folder 定位依據：03 Canonical Mapping 與 07 Folder Registry**

## 1. 目的與核心原則

本文件定義 V2 在 Google Drive 中對製片資產的分類、命名、版本、狀態、校驗與依賴管理方式。它不建立任何新資料夾，不批准任何資產，不改寫 Legacy `LOCK`／`FINAL`／`MASTER`／`APPROVED` 檔，也不構成 `SYSTEM SPECIFICATION LOCK V2.0`。

所有資產必須具備可追溯的 `asset_id`、`episode_id`（共用資產除外）、`google_drive_file_id`、`folder_id`、版本、狀態與校驗資訊。名稱利於人讀；ID 與校驗資訊才是可稽核的定位依據。

## 2. Canonical Drive 定位

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | 用途 |
|---|---|---|---|---|
| `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `MATA AI 原創影片製片系統 V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `ROOT_PARENT_NOT_IN_V2_SCOPE` | V2 唯一根容器。 |
| `GLOBAL_OS` | `01_全域系統規範` | `1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 全域規格與治理。 |
| `ORIGINAL_VIDEO_LIBRARY` | `02_原創影片資料庫` | `14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Series／Episode 內容資產。 |
| `SHARED_ASSET_LIBRARY` | `03_共用素材資料庫` | `1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Approved 跨集共用資產。 |
| `PRODUCTION_DATABASE` | `04_製片控制與索引` | `1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Asset Index、Gate、State、Version／Lock 與 QC 記錄。 |
| `ARCHIVE` | `05_封存資料庫` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 封存與 Legacy 證據。 |
| `LEGACY_SYSTEM_AUDIT` | `01_舊系統稽核` | `1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | 只讀舊系統稽核區。 |

以上七筆皆為 `VERIFIED_CANONICAL`；五大根目錄驗證時間為 `2026-07-26T12:36:31+08:00` 至 `2026-07-26T12:36:35+08:00`，舊系統稽核區為 `2026-07-26T12:36:35+08:00`。任何 Episode 子層於核准建立前，不得假定其 folder ID 或書寫為 Canonical。

## 3. Episode 完整資產分類

每個 Episode 只能位於 `ORIGINAL_VIDEO_LIBRARY` 下的已登錄 Series 容器。下列是 Episode 邏輯分類；實體子資料夾必須另經 Folder Registry 建立與驗證，不能因分類表而自動建立。

| asset_class | 內容 | 上游依賴 | 下游消費者 | 不可混入 |
|---|---|---|---|---|
| `BRIEF` | 目標、受眾、平台、時長、CTA、限制。 | Series 定位。 | Script、Production Plan。 | 未確認需求、他集 Brief。 |
| `STORY` | Hook、故事、旁白、腳本、對白、時間對位。 | Approved Brief。 | Storyboard、Voice、Edit。 | 未核准改寫、視覺生成檔。 |
| `VISUAL_BIBLE` | 角色、場景、服裝、光線、道具、連續性與 Exact Asset 引用。 | Approved Story。 | Storyboard、Keyframe、Flow。 | 未授權共用資產、重繪 Exact Asset。 |
| `STORYBOARD` | Shot／Segment、鏡頭、畫面功能、轉場與連續性。 | Approved Story、Visual Bible。 | Keyframe、Flow、Edit。 | 未對應 Story 的鏡頭。 |
| `KEYFRAME` | 起迄影格、關鍵畫面、角色／場景連續性圖。 | Approved Storyboard、Visual Bible。 | Flow、Edit、QC。 | 無來源的單張圖、Rejected 混放。 |
| `FLOW_MEDIA` | 圖生影片、模型輸出、Prompt、生成參數與輸出片段。 | Approved Keyframe、Storyboard。 | Edit、QC。 | 無 Keyframe／Prompt 記錄的媒體。 |
| `AUDIO` | 配音、音樂、音效、字幕來源、授權資訊。 | Approved Story。 | Edit、Final。 | 未授權音訊、未對位旁白。 |
| `EDIT` | 剪輯工程、字幕檔、色彩／音訊處理、輸出候選。 | Flow Media、Audio、Storyboard。 | QC、Final。 | 唯一原始母檔、未登錄外部素材。 |
| `QC_EVIDENCE` | 檢查表、問題單、修正證據、Gate 結果。 | 各階段輸出。 | Approval／Lock 決策。 | 用口頭或聊天結論取代證據。 |
| `FINAL_DELIVERY` | 已核准交付檔、封面、平台版本、交付 manifest。 | Approved QC、版本登錄。 | 發布、Archive。 | 未核准候選檔、唯一可編輯專案。 |
| `REJECTED_QUARANTINE` | 被拒絕的媒體與理由；僅可稽核。 | Rejection event。 | 僅供比對與追溯。 | Approved、Current、Exact Asset。 |

## 4. Asset Index 最小欄位

| 欄位 | 說明 |
|---|---|
| `asset_id` | 不可變唯一 ID，例如 `EP02-S03-KEYFRAME-001`。 |
| `asset_class` | 第 3 節受控分類之一。 |
| `series_id`／`episode_id`／`segment_id` | 所屬範圍；共享資產使用 `shared_asset_id`，不得假裝屬於 Episode。 |
| `stable_folder_code`／`folder_id` | 實體位置；folder ID 必須存在於 Folder Registry。 |
| `google_drive_file_id` | 檔案唯一定位；不得只存 URL 或檔名。 |
| `display_filename` | 依第 5 節命名。 |
| `version`／`approval_status`／`lock_status` | 版本與生命周期狀態。 |
| `source_asset_ids` | 直接上游資產 ID 清單。 |
| `dependency_check_status` | `NOT_RUN`、`PASSED`、`FAILED`、`RECHECK_REQUIRED`。 |
| `sha256`／`file_size_bytes`／`mime_type` | 完整性與格式校驗。 |
| `created_at`／`verified_at`／`verified_by` | 建立與核對時間、人員。 |
| `exact_asset_flag`／`rights_ref` | 是否 Exact Asset 與授權／來源證據。 |
| `rejection_reason`／`supersedes_asset_id` | 被拒原因與版本關係（適用時）。 |

## 5. 檔名與版本規則

### 5.1 格式

`<SERIES_ID>_<EPISODE_ID>_<SEGMENT_ID-or-GLOBAL>_<ASSET_CLASS>_<ASSET_SLUG>_v<MAJOR>.<MINOR>_<STATUS>.<ext>`

範例：

- `IFAI_EP02_S03_STORYBOARD_CAFE_MEETING_v1.0_APPROVED.md`
- `IFAI_EP02_S03_KEYFRAME_CAFE_START_v1.1_APPROVED.png`
- `IFAI_EP02_S03_FLOW_CAFE_LISTEN_v1.0_REJECTED.mp4`
- `GLOBAL_BRAND_LOGO_SUNLIGHT_v1.0_EXACT.png`

檔名使用 ASCII stable token；中文名稱可在 Asset Index 的 `display_name_zh_TW` 維護。不得以檔名作為唯一識別，亦不得覆寫相同 ID 的既有版本。

### 5.2 版本

| 變更類型 | 版本規則 | 例子 |
|---|---|---|
| 初始可審閱版本 | `v1.0` | 首次送審。 |
| 不改變已核准故事／語意的修正 | MINOR +1 | `v1.0 → v1.1`。 |
| 改變故事、鏡頭、權利、角色連續性或交付語意 | MAJOR +1，MINOR 歸零 | `v1.1 → v2.0`。 |
| 已 Lock／Approved 的後續修改 | 新 asset ID 或新版本檔；舊檔不覆寫 | Register 記錄 supersession。 |

## 6. Approval、Lock 與 Rejected 狀態

| 狀態 | 可否做為下游輸入 | 可否修改原檔 | 必要紀錄 |
|---|---|---|---|
| `DRAFT` | 否，僅內部準備。 | 是，依版本規則另存。 | 基本 Asset Index 欄位。 |
| `IN_REVIEW` | 否。 | 否；意見產生新版本。 | 審閱者、提交時間、檢核項。 |
| `APPROVED` | 是，限指定用途。 | 否；修改必產生新版本。 | 批准人、批准時間、依賴檢查。 |
| `LOCKED` | 是，作為正式基準。 | 絕對不可原地修改。 | Lock event、SHA-256、核准版本、理由。 |
| `REJECTED` | 否。 | 不得重用或混入 Approved 資產。 | 拒絕原因、拒絕人、時間、替代資產（如有）。 |
| `SUPERSEDED` | 僅為歷史追溯，不得作為新下游預設輸入。 | 不得覆寫。 | 被哪個 asset／版本取代。 |
| `ARCHIVED` | 否，除非人工指定稽核。 | 不得覆寫。 | 封存時間與 Archive 位置。 |

`APPROVED` 不等於 `LOCKED`；Approved 是可用審核結論，Locked 是不可回寫的正式基準。`REJECTED` 不等於刪除，必須隔離保存其 ID、校驗與原因。

## 7. Drive ID 與校驗規則

1. 每項 Folder 引用必須能回溯到 Folder Registry 的 `folder_id`；未登錄或不存在的 ID，Asset Index 不得寫入 `APPROVED` 或 `LOCKED`。
2. 每項檔案必須記錄 `google_drive_file_id`、MIME type、檔案大小與 SHA-256。無法取得雜湊時，標示 `HASH_PENDING`，不得 Lock。
3. 上傳、移動、rename、批准、Lock、封存後均需回讀 Drive ID 與父 folder ID，並更新 `verified_at`、`verified_by` 與證據連結。
4. ID 無法讀取、父層不符、檔名與 Index 不符、雜湊不符或發現重複 ID／名稱時，狀態立即為 `RECONCILIATION_REQUIRED`；停止發布與下游傳遞。
5. 目前已驗證的只有第 2 節七個資料夾。Episode 子資料夾與任何檔案在個別驗證前均不得標示為 `VERIFIED_CANONICAL`。

## 8. 上下游 Dependency 管理

資產只能在直接上游為 `APPROVED` 或 `LOCKED`，且 `dependency_check_status=PASSED` 時進入下游製作。預設關係如下：

`BRIEF → STORY → VISUAL_BIBLE + STORYBOARD → KEYFRAME → FLOW_MEDIA → EDIT → QC_EVIDENCE → FINAL_DELIVERY`

`STORY → AUDIO → EDIT` 為平行支線；`SHARED_ASSET_LIBRARY` 的 Approved／Locked 資產可供 `VISUAL_BIBLE` 引用，但必須列入 `source_asset_ids`。

若任一上游被改為 `REJECTED`、`SUPERSEDED` 或出現 MAJOR 版本升級，所有直接與間接下游標記 `RECHECK_REQUIRED`。Segment Ready 只代表該 Segment 的依賴通過，不得推定整個 Episode Ready；Episode 狀態須由 Episode 層的全部必要依賴與 Gate 另行判定。

## 9. Exact Asset 與 Rejected 隔離

### 9.1 Exact Asset

Exact Asset（官方 Logo、正式品牌元素、授權人物或其他要求一比一保留之檔案）只能保存原始檔與可追溯版本，不得交由生成式模型重繪、風格化、補畫或以相似圖替代。Asset Index 必須設 `exact_asset_flag=true`，保存來源、授權、原始 Drive file ID、SHA-256 與允許用途。輸出使用 Exact Asset 時以後製置入或受控引用處理，不能從生成結果擷取假冒版本。

### 9.2 Rejected 隔離

Rejected 檔案必須有 `approval_status=REJECTED`、拒絕原因與原始 ID，並放在 Episode 的 `REJECTED_QUARANTINE` 邏輯區或已登錄的 Archive 隔離區。它們不得與 Approved、Locked、Shared 或 Exact Asset 同一可用清單；不得作為模型參考圖、素材庫搜尋預設結果、剪輯預設輸入或對外發布候選。

## 10. 一致性與停止條件

本文件中七筆 Drive Folder ID、父 ID、stable code、中文名稱與驗證狀態，與 `03_V2_GOOGLE_DRIVE_CANONICAL_MAPPING_DRAFT.md` 及 `07_FOLDER_REGISTRY_V2_DRAFT.md` 相同。發現任一差異時，Asset System、Canonical Mapping 與 Folder Registry 一律退回 `RECONCILIATION_REQUIRED`，不得啟動自動化、不得進入 Lock、不得把任何資產升為 Approved／Locked。

本文件僅為第一批內容審閱稿；在書面核准前，仍不得進入 `SYSTEM SPECIFICATION LOCK V2.0` 或 Codex Implementation。
