# 03｜V2 Google Drive Canonical Mapping Draft

**文件狀態：DRAFT／NOT LOCKED**
**驗證基準日：2026-07-26**
**驗證時區：Asia/Taipei（UTC+08:00）**
**適用範圍：MATA AI 原創影片製片系統 V2 的 Google Drive 實體資料夾**

## 1. 本文件的效力與邊界

本文件記錄已存在之 V2 根目錄、五大根目錄與舊系統稽核區的唯一 Canonical Mapping。它是資料夾定位與命名的草案規格，不是 `SYSTEM SPECIFICATION LOCK V2.0`，也不授權建立、搬移、刪除、合併或清理任何 Drive 項目。

本輪僅確認下列事實：根目錄與五大根目錄均以既有 Drive ID 原地改為正式繁體中文顯示名稱；五大根目錄同屬同一根目錄；未發現同層的中文／英文平行根目錄。驗證時所有五大根目錄均為空，僅 `05_封存資料庫` 包含一個 `01_舊系統稽核` 子資料夾。

## 2. 不可變識別與命名原則

| 欄位 | 定義 | 規則 |
|---|---|---|
| `stable_folder_code` | 系統穩定邏輯代碼 | 全域唯一；不得因改名、語系或搬移而改變。 |
| `display_name_zh_TW` | Drive 對人顯示的正式繁體中文名稱 | 本系統唯一正式介面名稱；需經變更控制才可原地改名。 |
| `google_drive_folder_id` | Google Drive 唯一資料夾 ID | Canonical 定位主鍵；不得以名稱、路徑或聊天內容取代。 |
| `parent_folder_id` | 已驗證父資料夾的 Drive ID | 必須與實體父層相符；不相符即停止後續作業。 |

不得使用純英文資料夾名作為正式 V2 介面、不得建立中文或英文平行資料夾、不得以同名資料夾替代既有 ID。任何處理都必須先以 `google_drive_folder_id` 讀取，再以 `stable_folder_code` 交叉核對；顯示名稱僅用於人工作業確認。

## 3. 已驗證 Canonical Mapping

驗證方法：讀取根目錄直接子項，再逐一讀取五大根目錄直接子項。`parent_folder_id` 的父子關係由根目錄直接子項結果交叉確認。驗證時間採最後一次原地改名完成後的 UTC 時間換算為 Asia/Taipei。

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | folder_purpose | allowed_content | prohibited_content | verification_status | verified_at |
|---|---|---|---|---|---|---|---|---|
| `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `MATA AI 原創影片製片系統 V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `ROOT_PARENT_NOT_IN_V2_SCOPE` | V2 唯一系統容器；承載五大根目錄。 | 僅五大已登錄根目錄。 | 任一平行中文／英文根目錄、未登錄頂層資料夾、Episode 或檔案直接置入。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` |
| `GLOBAL_OS` | `01_全域系統規範` | `1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 管理跨 Episode 的系統規格、治理、SOP 與正式登錄規則。 | 已核准或草案中的 Global 規格、治理紀錄、安裝手冊、測試計畫。 | Episode 專屬原始素材、Flow 生成檔、未登錄的平行 Global 目錄。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:31+08:00` |
| `ORIGINAL_VIDEO_LIBRARY` | `02_原創影片資料庫` | `14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 承載 Series 與 Episode 的正式原創製片資產。 | 已登錄 Series／Episode 容器及其 Brief、Script、Visual、Storyboard、Keyframe、Flow、Edit、Final 資產。 | 根目錄層級的 `01_SERIES`／`02_EPISODES` 平行架構、跨集共享資產的未審核副本。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:32+08:00` |
| `SHARED_ASSET_LIBRARY` | `03_共用素材資料庫` | `1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 存放經核准可跨 Episode 使用的共用資產。 | Approved 的角色、場景、道具、聲音、字型、品牌 Exact Asset 與其 manifest。 | Episode 專屬資產直接升格、Rejected 資產、生成式重繪的 Exact Asset。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:33+08:00` |
| `PRODUCTION_DATABASE` | `04_製片控制與索引` | `1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 存放 Folder Registry、Asset Index、Production State、Gate、Version／Lock Register 與 QC 證據。 | 結構化登錄、不可覆寫稽核事件、校驗資訊、依賴關係。 | 原始大型媒體、以聊天摘要取代登錄、未驗證 ID 的自動化輸出。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:34+08:00` |
| `ARCHIVE` | `05_封存資料庫` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 保存 Legacy Snapshot、已取代版本與舊系統稽核證據。 | 已封存的歷史證據、Superseded snapshot、不可覆寫的舊系統稽核區。 | 對 `LOCK`／`FINAL`／`MASTER`／`APPROVED` 原檔直接改名、搬移、覆寫或刪除。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` |
| `LEGACY_SYSTEM_AUDIT` | `01_舊系統稽核` | `1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | 保存舊系統盤點與稽核證據，作為 Legacy 參照。 | 只讀盤點證據、Legacy 路徑記錄、歷史交接。 | 新 V2 生產資產、Lock 後文件的直接修改、當作目前系統的寫入區。 | `VERIFIED_CANONICAL` | `2026-07-26T12:36:35+08:00` |

## 4. 實體結構驗證結果

| 檢核項目 | 結果 | 證據／判定 |
|---|---|---|
| 根目錄名稱 | 通過 | ID `18k…PbT` 顯示為 `MATA AI 原創影片製片系統 V2`。 |
| 五大根目錄名稱 | 通過 | 五個直接子項顯示為 `01_全域系統規範` 至 `05_封存資料庫`。 |
| 五大根目錄父層 | 通過 | 五項均由 V2 根目錄直接列出，父層固定為 `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT`。 |
| 子項數 | 通過 | `01`、`02`、`03`、`04` 各 0；`05` 為 1（`01_舊系統稽核`）。 |
| 舊系統稽核區 | 通過 | ID `1Hxc…qu6`，位於 `05_封存資料庫` 下，名稱為 `01_舊系統稽核`。 |
| 平行中文／英文目錄 | 通過 | 根目錄直接子項僅五個已登錄繁中名稱；未發現 `01_GLOBAL_OS`、`02_ORIGINAL_VIDEO_LIBRARY`、`03_SHARED_ASSET_LIBRARY`、`04_PRODUCTION_DATABASE`、`05_ARCHIVE` 或同名平行 root。 |

## 5. 三層邏輯映射與建立限制

| 邏輯層 | 唯一實體位置 | 允許的後續細分 | 禁止的平行結構 |
|---|---|---|---|
| Global OS | `01_全域系統規範` | 依已核准 Folder Registry 建立的規格類別子層。 | 在 V2 根目錄另建 `00_GLOBAL_OS`。 |
| Series | `02_原創影片資料庫/<SERIES_ID>` | Series Master 與 Episode 容器。 | 在 V2 根目錄另建 `01_SERIES`。 |
| Episode | `02_原創影片資料庫/<SERIES_ID>/Episodes/<EPISODE_ID>` | 依 Asset System V2 建立的資產類別。 | 在 V2 根目錄另建 `02_EPISODES` 或以名稱猜測既有 Episode。 |

任何尚未存在的子資料夾，不因本 Mapping 自動獲准建立。必須先在 Folder Registry 取得唯一 stable code 與目標父層 ID，確認無重複後才可進入獨立的建置審核。

## 6. 異常處理與變更控制

1. 讀取 ID 失敗、回傳名稱不符、父層不符、子項數意外變更，或發現平行目錄時，狀態改為 `RECONCILIATION_REQUIRED`。
2. 異常時立即停止該分支的 rename、建立、移動、上傳與自動化；僅可做讀取與稽核紀錄。
3. 不得以建立新資料夾、複製內容或刪除項目來「修正」不一致；需提交 ID、父 ID、名稱、子項清單與時間戳供人工決策。
4. `LOCK`、`FINAL`、`MASTER`、`APPROVED` 的舊檔保留原狀。有效版本、取代關係與目前可用狀態將由外部 Register 表示，而非回寫歷史檔。

## 7. 與第一批文件的一致性聲明

本 Mapping 是 `07_FOLDER_REGISTRY_V2_DRAFT.md` 的根目錄與稽核區唯一來源，亦是 `DRIVE_ASSET_SYSTEM_V2.0_DRAFT.md` 的 `folder_id`、父層定位與隔離規則基準。三份文件均使用相同七筆 stable code、顯示名稱、Drive ID、父層 ID、驗證狀態與驗證時間；若任一欄位發生差異，三份文件一律退回 `RECONCILIATION_REQUIRED`，不得進入 Lock。
