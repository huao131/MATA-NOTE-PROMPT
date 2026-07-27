# 07｜Folder Registry V2 Draft

**文件狀態：DRAFT／NOT LOCKED**
**定位原則：Drive ID 優先；stable code 與中文顯示名稱分離**
**驗證基準：03_V2_GOOGLE_DRIVE_CANONICAL_MAPPING_DRAFT.md**

## 1. 目的與強制規則

Folder Registry 是 V2 對 Google Drive 資料夾唯一且可稽核的定位表。任何人、夥伴帳號、SOP 或未來自動化，都必須先以 `google_drive_folder_id` 定位，再以 `stable_folder_code` 驗證語意；不得以資料夾名稱、模糊路徑或聊天記憶定位。

中文名稱是正式使用者介面，stable code 是不可變的系統語意，Drive ID 是實體主鍵。三者必須同時存在，但不可互相替代。

## 2. Registry 最小資料模型

| 欄位 | 必填 | 說明 |
|---|---:|---|
| `stable_folder_code` | 是 | 全域唯一且不可任意改變的邏輯代碼。 |
| `display_name_zh_TW` | 是 | Drive 正式繁體中文名稱；不可用作唯一定位。 |
| `google_drive_folder_id` | 是 | 實體定位主鍵；不可為空、TBD 或由名稱推測。 |
| `parent_stable_folder_code` | 根目錄除外 | 父層穩定代碼。 |
| `parent_folder_id` | 根目錄除外 | 已讀取驗證的父資料夾 ID。 |
| `logical_layer` | 是 | `SYSTEM_ROOT`、`GLOBAL`、`SERIES`、`EPISODE`、`SHARED_ASSET`、`DATABASE`、`ARCHIVE` 或 `LEGACY_AUDIT`。 |
| `folder_purpose` | 是 | 該資料夾唯一職責。 |
| `allowed_content`／`prohibited_content` | 是 | 可寫入與禁止寫入邊界。 |
| `verification_status` | 是 | `VERIFIED_CANONICAL`、`PENDING_VERIFICATION`、`RECONCILIATION_REQUIRED`、`ARCHIVED`。 |
| `verified_at` | 是 | ISO 8601 含時區時間。 |
| `child_folder_count` | 是 | 本輪直接子資料夾數；用於變更檢測。 |
| `evidence_ref` | 是 | 可重現的 Drive 讀取證據描述。 |

## 3. 已驗證 Registry Records

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_stable_folder_code | parent_folder_id | logical_layer | folder_purpose | allowed_content | prohibited_content | child_folder_count | verification_status | verified_at | evidence_ref |
|---|---|---|---|---|---|---|---|---|---:|---|---|---|
| `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `MATA AI 原創影片製片系統 V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | — | `ROOT_PARENT_NOT_IN_V2_SCOPE` | `SYSTEM_ROOT` | V2 唯一根容器。 | 僅五大已登錄根目錄。 | 頂層檔案、未登錄根目錄、中文／英文平行 root。 | 5 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` | 讀取根目錄直接子項，取得五個已驗證資料夾。 |
| `GLOBAL_OS` | `01_全域系統規範` | `1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5` | `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `GLOBAL` | 全域規格與治理。 | V2 規格、治理、SOP、安裝與測試文件。 | Episode 原始媒體、未登錄平行 Global 目錄。 | 0 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:31+08:00` | 根目錄直接子項＋本身直接子項讀取。 |
| `ORIGINAL_VIDEO_LIBRARY` | `02_原創影片資料庫` | `14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC` | `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `SERIES` | 原創 Series 與 Episode 製片資產容器。 | 已登錄 Series、Episode 與其完整資產樹。 | `01_SERIES`／`02_EPISODES` 平行根、未審核共用資產。 | 0 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:32+08:00` | 根目錄直接子項＋本身直接子項讀取。 |
| `SHARED_ASSET_LIBRARY` | `03_共用素材資料庫` | `1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV` | `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `SHARED_ASSET` | 已核准跨集共用資產庫。 | Approved 角色、場景、道具、聲音、品牌 Exact Asset。 | Episode 專屬資產、Rejected、重繪 Exact Asset。 | 0 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:33+08:00` | 根目錄直接子項＋本身直接子項讀取。 |
| `PRODUCTION_DATABASE` | `04_製片控制與索引` | `1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG` | `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `DATABASE` | 製片控制、索引與稽核資料。 | Folder Registry、Asset Index、Gate、State、Lock／Version Register、QC log。 | 原始影片／圖片母檔、聊天摘要替代紀錄。 | 0 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:34+08:00` | 根目錄直接子項＋本身直接子項讀取。 |
| `ARCHIVE` | `05_封存資料庫` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `ARCHIVE` | Legacy 與 Superseded 證據保存。 | 歷史快照、舊系統稽核、已取代版本。 | 新製片工作檔、對鎖定檔直接改寫。 | 1 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` | 根目錄直接子項＋本身直接子項讀取。 |
| `LEGACY_SYSTEM_AUDIT` | `01_舊系統稽核` | `1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6` | `ARCHIVE` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `LEGACY_AUDIT` | 保存既有系統盤點證據。 | 只讀 Legacy 稽核資料。 | 新 V2 工作檔、移動／改名／覆寫舊 Lock 檔。 | `NOT_CAPTURED_IN_THIS_PASS` | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` | 由 `ARCHIVE` 直接子項讀取驗證。 |

## 4. 重複建立防護

1. **先讀 ID。** 操作前輸入必須是已登錄的 `google_drive_folder_id`；ID 不存在、無法讀取或回傳 MIME type 非 folder，立即停止並回報。
2. **再核對三欄。** 讀取結果必須同時符合登錄的 ID、stable code 所代表的邏輯層與 `display_name_zh_TW`。名稱不符不是可自動修正的 rename 指令，而是 `RECONCILIATION_REQUIRED`。
3. **建立前雙重查重。** 僅在已核准建立子層時，先以目標父 ID 列出直接子項，檢查：(a) 同一 stable code 是否已登錄；(b) 同一 display name 是否已存在；(c) 是否有不同 ID 但相同用途的資料夾。任一成立即不得建立。
4. **建立後立即登錄與回讀。** 新資料夾必須先取得 Drive ID，再寫入本 Registry，回讀確認父 ID、名稱與子項數；未完成前不得寫入資產。
5. **不可用 create-copy-move 修正。** ID 遺失、誤建、同名或平行樹僅能標記異常並報告；不得自行複製、搬移、合併或刪除。

## 5. ID 不存在或不一致時的停止規則

以下任一情況，作業狀態必須切換為 `STOP_AND_REPORT`：

- Registry 找不到指定 `google_drive_folder_id`；
- Drive 讀取失敗、權限不足、或讀回 ID 不同；
- 讀回名稱與 `display_name_zh_TW` 不同；
- 父 ID 與 `parent_folder_id` 不同；
- 直接子項數與本 Registry 基準不同，且沒有已核准的變更紀錄；
- 發現中文／英文平行資料夾或相同 stable code 指向兩個 ID。

停止報告至少包含：操作人、時間、stable code、預期 ID、實際 ID／錯誤、預期父 ID、實際父 ID、直接子項清單及無修改的讀取證據。未有人工決策前，不得繼續該樹的任何寫入操作。

## 6. 夥伴帳號的獨立映射規則

1. 每一個夥伴 Google 帳號、共用雲端硬碟或學員工作區，都是獨立的 `drive_account_context`，不得沿用 Mata 老師帳號的 Drive ID。
2. 夥伴建立自己的 V2 工作區時，必須建立一份獨立 Folder Registry，使用相同 stable code 與命名規範，但填入該帳號實際產生的 `google_drive_folder_id`、`parent_folder_id` 與驗證時間。
3. 跨帳號引用一律使用 `account_context_id + stable_folder_code + google_drive_folder_id`；不可只提供名稱或只提供 stable code。
4. 共用素材的「參照」與「複製」必須明確標記。若授權使用中心資產，Asset Index 記錄來源帳號、原始 Drive file ID、授權範圍與本帳號引用方式；不得將夥伴副本誤登錄為中心 Exact Asset。
5. 任何自動化在未收到明確 `drive_account_context` 時預設停止。禁止把夥伴檔案寫入 Mata 老師 V2 根目錄，或把 Mata 老師的 ID 套入夥伴帳號。

## 7. 稽核、保留與一致性

每次 rename、建立、移動或封存，都應新增一筆不可覆寫的事件紀錄，至少保留 before／after 名稱、folder ID、父 ID、直接子項數、操作人、時間與證據。`LOCK`、`FINAL`、`MASTER`、`APPROVED` 不得在原地變更；有效版本與取代關係由外部 Register 管理。

本 Registry 的七筆已驗證資料，與 `03_V2_GOOGLE_DRIVE_CANONICAL_MAPPING_DRAFT.md` 及 `DRIVE_ASSET_SYSTEM_V2.0_DRAFT.md` 完全一致。若後續驗證改變任何 ID、父 ID、名稱或狀態，三份文件須同一變更單同步更新，否則維持 `DRAFT／NOT LOCKED`。
