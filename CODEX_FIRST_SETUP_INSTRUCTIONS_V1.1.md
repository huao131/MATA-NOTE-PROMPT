# MATA AI VIDEO STUDIO｜Codex 首次建置指令 V1.1

## 0. 任務定位

你是本系統的「首次建置與技術維護執行者」，不是日常製片操作員。

本次任務完成後，日常 Episode 工作由：

`Mata老師＋ChatGPT＋GitHub Connector＋Google Drive Connector`

直接完成。不得設計成每張圖片、每次 Lock 或每集建檔都必須再次交給 Codex。

---

## 1. 任務目標

在私人 Repository：

`https://github.com/huao131/MATA-AI-VIDEO-STUDIO`

完成：

1. 將 `MATA-AI-VIDEO-STUDIO_V1.0_FINAL_LOCK_REGISTERED.zip` 內的專案內容匯入 `main`。
2. 保留 V1.0 全部內容與位元組，不得修改。
3. 新增 V1.1 架構、保護機制、Episode Template 與驗證工具。
4. 建立讓 ChatGPT 可直接維護 GitHub 文字狀態、並以 Drive File ID 管理大型資產的結構。
5. 完成後輸出建置報告與驗證證據。

---

## 2. 最高保護規則

### 2.1 禁止事項

- 不得修改、格式化、重新儲存、改名或搬移任何既有 V1.0 檔案。
- 不得修改名稱或內容含有：
  - `FINAL`
  - `LOCKED`
  - `MASTER`
  - `APPROVED`
  - `EXACT`
- 不得重新壓縮、重新輸出或轉換 PNG。
- 不得將 ZIP 本身放入 Repository。
- 不得把 ZIP 內的 `.git/` 目錄上傳到遠端。
- 不得建立公開 Repository。
- 不得加入 License。
- 不得以「整理格式」為由重寫 V1.0。
- 不得把 Codex 設計成日常 Episode 的必要中繼站。

### 2.2 特別保護

至少包含：

- `system/MASTER_EXECUTION_SPEC_V1.0_FINAL_LOCK.md`
- `episodes/EP02_美容業/masters/CHARACTER_MASTER_林沐晴.png`
- `episodes/EP02_美容業/masters/SCENE_MASTER_日光美學館.png`
- `episodes/EP02_美容業/masters/PROP_MASTER_日光美學館.png`
- `episodes/EP02_美容業/masters/LOGO_MASTER_EXACT.png`

匯入前後必須計算 SHA-256；任何一筆不同立即停止。

---

## 3. 建置流程

### STEP 1｜安全解壓與來源檢查

1. 解壓至新的暫存工作目錄。
2. 確認解壓根目錄為 `MATA-AI-VIDEO-STUDIO/`。
3. 排除 ZIP 內的 `.git/`，不得把巢狀 Git 歷史匯入遠端。
4. 列出所有 V1.0 檔案並建立 SHA-256 基準。
5. 確認遠端 Repository 是 `private`，預設分支為 `main`。

### STEP 2｜匯入 V1.0 原始內容

1. 將專案內容複製至乾淨 checkout。
2. 不修改任何來源檔案。
3. 先執行：

```bash
python scripts/validate_episode.py episodes/EP02_美容業
```

4. 若驗證失敗，只回報；不得自行修復 V1.0 LOCK。
5. 提交訊息：

```text
chore: import V1.0 FINAL LOCKED baseline without modification
```

### STEP 3｜建立不可變更保護

只新增下列保護機制：

```text
system/protection/
├── V1.0_PROTECTED_FILES.sha256
└── PROTECTION_POLICY_V1.1.md

scripts/
└── verify_v1_0_protection.py

.github/workflows/
└── protect-v1-0.yml
```

要求：

- `V1.0_PROTECTED_FILES.sha256` 記錄所有 V1.0 FINAL／LOCKED／MASTER／APPROVED／EXACT 檔案。
- 驗證器只讀取與比對，不改寫任何來源。
- GitHub Actions 在 push／pull request 時執行驗證。
- 驗證失敗必須阻止合併並列出變更檔案。

### STEP 4｜新增 V1.1 架構

保留並提交：

- `system/ARCHITECTURE_V1.1_DRAFT.md`
- `CODEX_FIRST_SETUP_INSTRUCTIONS_V1.1.md`

新增：

```text
system/v1.1/
├── SYNC_EVENT_SPEC_V1.1.md
├── OWNERSHIP_MATRIX_V1.1.md
└── schemas/
    └── asset_sync_record.schema.json

templates/episode_v1.1/
├── EPISODE_MASTER.md
├── PRODUCTION_STATE.json
├── PRODUCTION_LOG.md
├── STORYBOARD_MASTER.md
└── ASSET_INDEX.json
```

V1.1 必須是新增式內容，不得取代或移動 `templates/episode/`。

### STEP 5｜建立 ChatGPT 日常同步介面

新增文字化、可由 ChatGPT Connector 更新的欄位：

```json
{
  "episode_id": "",
  "drive_episode_folder_id": "",
  "runtime_state": "NEW_EPISODE",
  "sync_status": {
    "github": "PENDING",
    "drive": "PENDING"
  },
  "last_verified_at": ""
}
```

`ASSET_INDEX.json` 每筆資產至少包含：

```json
{
  "asset_id": "",
  "file_name": "",
  "version": "",
  "status": "",
  "drive_file_id": "",
  "drive_parent_folder_id": "",
  "sha256": "",
  "timestamp": "",
  "reference_eligible": false
}
```

不得把大型圖片或影片直接塞進狀態 JSON。

### STEP 6｜建立 Episode 初始化工具

新增 `scripts/create_episode_v1_1.py`，功能：

1. 接收 Episode ID、產業與影片名稱。
2. 只建立 GitHub／本地文字結構，不操作使用者憑證。
3. 產出 Drive 資料夾建立清單與預期欄位。
4. 不建立重複 Episode。
5. 不允許覆寫既有 Episode。

此腳本是維護與備援工具；日常情況由 ChatGPT 透過 GitHub／Drive Connector 直接建立。

### STEP 7｜驗證

至少執行：

```bash
python scripts/verify_v1_0_protection.py
python scripts/validate_episode.py episodes/EP02_美容業
python -m json.tool templates/episode_v1.1/PRODUCTION_STATE.json
python -m json.tool templates/episode_v1.1/ASSET_INDEX.json
```

另做一次不提交的 dry run：

```bash
python scripts/create_episode_v1_1.py EP999 測試業 測試影片 --dry-run
```

驗證：

- 不修改任何 V1.0。
- 不產生未追蹤的大型檔案。
- 不建立實際 EP999。
- 所有 JSON 合法。
- 保護工作流程可執行。

### STEP 8｜提交與推送

V1.1 使用獨立提交：

```text
feat: add V1.1 ChatGPT GitHub Drive operating architecture
```

推送至：

```text
origin/main
```

不得 force push。

---

## 4. 完成報告格式

Codex 完成後只需回報：

```text
SETUP RESULT
Repository: huao131/MATA-AI-VIDEO-STUDIO
Visibility: PRIVATE
Branch: main
V1.0 Import Commit: <SHA>
V1.1 Setup Commit: <SHA>
Protected Files Check: PASS/FAIL
EP02 Validation: PASS/FAIL
V1.1 JSON Validation: PASS/FAIL
Dry Run: PASS/FAIL
Modified V1.0 Files: 0
Remaining Manual Action: <NONE or exact blocker>
```

若任何保護檢查失敗，不得推送 V1.1，必須停止並列出差異。

---

## 5. 建置後責任邊界

建置完成後：

- ChatGPT：每集日常製片、GitHub 狀態更新、Drive 資產歸檔與同步驗證。
- GitHub：文字規格、State、Log、Index 的權威來源。
- Google Drive：大型資產與 Final 的權威來源。
- Codex：系統維護、批次修復、Schema Migration 與技術除錯。
- Mata老師：人工 Gate、QC 決策、Flow／剪映無 API 時的實際操作。

不得要求 Mata老師為每張圖重複下載、開 Codex、上傳、再返回 ChatGPT。

**END OF CODEX FIRST SETUP INSTRUCTIONS V1.1**
