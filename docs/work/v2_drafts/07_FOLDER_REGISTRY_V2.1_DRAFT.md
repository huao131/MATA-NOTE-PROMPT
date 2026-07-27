# Folder Registry V2.1｜第一批正式定義草案

**狀態：DRAFT／NOT LOCKED**  
**本文件是所有第一批 Draft 的唯一 Folder Registry 定義。Drive ID 為主鍵；stable code 與繁中顯示名稱不可互相替代。**

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | folder_purpose | allowed_content | prohibited_content | verification_status | verified_at |
|---|---|---|---|---|---|---|---|---|
| `MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2` | `MATA AI 原創影片製片系統 V2` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | `ROOT_PARENT_NOT_IN_V2_SCOPE` | V2 唯一系統容器。 | 僅五大已登錄根目錄。 | 頂層檔案、Episode 直放、平行根。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |
| `GLOBAL_OS` | `01_全域系統規範` | `1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 全域規格與治理。 | 規格、SOP、治理、測試、安裝文件。 | Episode 原始媒體、Flow 輸出、平行 Global。 | `VERIFIED` | `2026-07-26T12:36:31+08:00` |
| `ORIGINAL_VIDEO_LIBRARY` | `02_原創影片資料庫` | `14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Series／Episode 資產容器。 | 已登錄 Series、Episode 與受控資產樹。 | `01_SERIES`、`02_EPISODES` 平行根、未審核共用副本。 | `VERIFIED` | `2026-07-26T12:36:32+08:00` |
| `SHARED_ASSET_LIBRARY` | `03_共用素材資料庫` | `1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | 跨集共用資產。 | Approved／Locked 共用資產與 Exact Asset 原檔。 | Episode 專屬、Rejected、生成重繪 Exact Asset。 | `VERIFIED` | `2026-07-26T12:36:33+08:00` |
| `PRODUCTION_DATABASE` | `04_製片控制與索引` | `1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | State、Gate、Index、Register、QC 證據。 | 結構化登錄、依賴與校驗。 | 原始大型媒體、聊天摘要、未驗證輸出。 | `VERIFIED` | `2026-07-26T12:36:34+08:00` |
| `ARCHIVE` | `05_封存資料庫` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | `18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT` | Legacy 與 Superseded 證據。 | 歷史快照、已取代版本、舊系統稽核。 | 新製片工作檔、受保護檔直接變更。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |
| `LEGACY_SYSTEM_AUDIT` | `01_舊系統稽核` | `1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6` | `1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz` | Legacy 唯讀稽核證據。 | 只讀盤點、歷史路徑、交接資料。 | 新 V2 資產、移動、改名、覆寫、刪除 Legacy。 | `VERIFIED` | `2026-07-26T12:36:35+08:00` |

## 防重複與夥伴帳號

操作前必須讀取已登錄 ID；ID 不存在、名稱或父 ID 不符、發現同名／平行資料夾時，立即 `STOP_AND_REPORT`。不得 create-copy-move-delete 修正。夥伴帳號為獨立 `drive_account_context`：沿用 stable code，不得沿用 Mata 帳號的 Drive ID；跨帳號引用須同時記錄 `account_context_id`、stable code、folder ID。
