# MATA AI VIDEO STUDIO｜本機網站操作指南 V1.0

## Windows 啟動

1. 安裝 Python 3.11 或更新版本。
2. 在 Repository 根目錄執行 `powershell -ExecutionPolicy Bypass -File scripts/start_local_studio.ps1`。
3. 瀏覽器開啟 `http://127.0.0.1:8765`。
4. 本機索引預設位於 `.local/mata-studio/studio.db`；可用 `MATA_STUDIO_DATA_DIR` 改至 Windows Local AppData。

本版本只使用 Python 標準函式庫，不需安裝第三方套件，也不需 Docker。

## 日常流程

1. New Episode 建立 Brief，系統只建立 `AWAITING_CREATIVE_INPUT`。
2. 在 ChatGPT 完成創意後，將結構化 JSON 貼入 Creative Studio。
3. 先驗證、儲存 Candidate，再提交人工 Gate。
4. Mata老師以獨立人工按鈕批准或退回；Payload 不能偽造批准。
5. Story、Visual Bible、Storyboard、Keyframe 依相同 Artifact 版本流程匯入。
6. Drive 連線後依已驗證 Folder ID 瀏覽與登記資產。
7. Production Handoff 只匯出 Flow／Editing 候選包，不會自動執行外部工具。

## Google Drive OAuth

- OAuth Client 設定檔只能放在本機安全路徑，透過 `MATA_DRIVE_CLIENT_CONFIG` 指向。
- 不得把 Client Secret、Refresh Token、Access Token 或個人 Drive ID 寫入 Git。
- 未完成 OAuth 時網站仍可啟動，Drive 狀態明確顯示 `NOT_CONNECTED`。
- 本版未執行真實 Drive E2E；不得將 Mock 結果視為真實上傳證據。

## 資料與 Cache

- SQLite：索引、狀態、Drive ID、事件；不是正式媒體來源。
- `.local/mata-studio/cache`：可刪除預覽 Cache。
- Google Drive：確認後文字成果及正式圖片、影片、音訊、字幕與 Final Output。
- 備份：停止程式後複製 `studio.db`；還原時保留損壞檔案，再使用備份或 GitHub Manifest＋Drive ID 重建。

## JSON 匯入

Artifact Submission 必須符合 `schemas/local_studio/artifact_submission.schema.json`。批准事件只能走 Gate API，不得放在一般 Artifact Payload。

## 常見錯誤

- `DRIVE_NOT_CONNECTED`：完成本機 OAuth 設定。
- `DRIVE_ROOT_FORBIDDEN`：指定已驗證 Folder ID，禁止 Drive 首頁。
- `ARTIFACT_VERSION_CONFLICT`：建立新版本，不得覆寫。
- `NON_HUMAN_APPROVER`：只有 Mata老師人工事件可批准。
- `REJECTED_ASSET_DEPENDENCY`：移除 Rejected Asset 下游引用。
