# Portable Installation Guide V2.1｜第三批草案

**狀態：DRAFT／NOT LOCKED；不執行任何實體安裝。**

## 1. 安裝原則與帳號責任

每位使用者複製自己的 Repository，並在自己的 Google Drive 建立獨立工作區。`stable_folder_code` 必須維持 V2 規格一致；`display_name_zh_TW` 使用正式繁中顯示名稱；Mata老師帳號的 Folder／File ID 絕不可複製或填入新使用者 Mapping。

預設安裝不要求額外付費 API。ChatGPT、Gemini、Flow、Canva、CapCut 均由使用者自行建立、付費、授權、登入與遵守平台條款；系統只定義交接資料，不能保證或控制這些服務的操作、點數、輸出或可用性。

## 2. 系統規格安裝

1. clone／fork 已正式發布且可解析的 GitHub Repository；目前 Publication Gate 為 `BLOCKED`，因此本步驟只能作為未來指引，不能以 Local Commit 代替正式來源。
2. 建立使用者分支與本地工作區；保留 Legacy 目錄只讀，不搬移、不刪除、不覆寫 `LOCK`／`FINAL`／`MASTER`／`APPROVED`。
3. 驗證所需 V2 Draft、Schema 與範本存在；若 D01、D02、D04、D06、D08、D09 仍為 Crosswalk `GAP`，停止宣告完整系統安裝，改列安裝前缺口。

## 3. Google Drive 映射

1. 在使用者的 `drive_account_context` 新建一個 V2 根容器與五大根目錄，顯示名稱依 `07_FOLDER_REGISTRY_V2.1_DRAFT.md`；不得建立 `00_GLOBAL_OS`、`01_SERIES`、`02_EPISODES` 平行 root。
2. 建立前先以目標父 ID 列出直接子項，檢查 stable code、名稱、用途與既有 ID；任一重複或同用途不同 ID，即 `STOP_AND_REPORT`，不得自動 create-copy-move-delete 修正。
3. 建立後讀回每個 folder 的 ID、父 ID、名稱、MIME type 與 child count，寫入使用者專屬 Folder ID Mapping。Mapping 必須保留同一 stable code，但全部使用新帳號實際 ID。
4. 任一 ID 不存在、父層不符、名稱不符、權限不足或平行目錄存在時，停止後續寫入；回報預期／實際 ID、父 ID、子項清單、時間與無修改讀取證據。

## 4. 使用者工具設定與 EXACT ASSET

- ChatGPT／Gemini：使用者自行匯入已核准 Instructions；在 D01、D02 完成前不得聲稱有正式 V2 Instructions。
- Flow：僅由使用者在其帳號中執行；不得消耗點數作為安裝或測試。Flow 輸出需手動登錄 Drive File ID、checksum、來源與 Asset Index。
- Canva／CapCut：使用者帳號自行負責；僅接受受控 manifest／素材交接，系統不直接控制它們。
- EXACT ASSET：匯入原始檔，登錄 `exact_asset_id`、原始 Drive File ID、checksum、權利證據與允許用途。只能受控引用或後製置入；禁止生成式 AI 重繪、仿製或替代。

## 5. Episode 初始化

1. 僅在使用者 Mapping 已 `VERIFIED` 且目標 Series／Episode 容器已受控登錄時初始化。
2. 使用獨立 Episode ID 與受控範本；Legacy Episode 僅作唯讀參考，不可被複製覆寫為新 Episode。
3. 初始資料的 `evidence_status` 為 `UNVERIFIED`，Canonical Production State 保持空白／`NOT_EVALUATED`，直到存在可解析證據。
4. 測試 Episode、測試資產與測試 Gate 必須使用明確 `TEST_` scope，並與正式 Production State／Final Asset List 完全隔離；不得把測試資料寫入正式紀錄。

## 6. 驗證、停止與復原

驗證順序：Repository remote SHA → Folder Mapping → Asset Index 欄位 → Gate／Evidence → Dependency Check。任何 `CONFLICTED`、非 `VERIFIED` Canonical 寫入、缺 Drive ID／checksum、Lock 改寫、重複版號或未完成 Dependency Recheck 均停止。

復原只允許：停止、保存讀取證據、將失敗項目標為待處理、由 Register 建立新版本或外部 supersession 關係。不得以刪除、搬移、覆寫、重建平行資料夾或回填測試資料作為復原。安裝完成不等於 SYSTEM SPECIFICATION LOCK 或 Codex Implementation 核准。
