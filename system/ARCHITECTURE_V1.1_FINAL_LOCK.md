# MATA AI VIDEO STUDIO｜ARCHITECTURE V1.1

**Status：FINAL／LOCKED**  
**Owner：Mata老師**  
**Base Version：V1.0 FINAL／LOCKED**  
**Revision Type：Additive Architecture／新增式架構**  
**Effective Date：2026-07-25**  
**Lock Confirmation：Mata老師已於 2026-07-25 22:50（Asia/Taipei）確認鎖定**  
**Immutable Rule：本文件不得直接覆寫；後續修訂必須建立 V1.2 或更高版本。**  

---

## 1. 版本治理聲明

1. V1.0 FINAL／LOCKED 是不可變更的基準版本。
2. V1.1 不得覆寫、重新格式化、重新儲存、改名或搬移任何 V1.0 FINAL／LOCKED／MASTER／APPROVED／EXACT 文件與資產。
3. V1.1 只以新增檔案、附加規格與新自動化流程實作。
4. V1.1 已由 Mata老師核准並正式生效。
5. 若與 V1.0 的「日常工具責任」衝突，以 V1.1 為準；故事鎖定、QC、Exact Asset、版本控制及人工 Gate 等品質規則仍完整繼承 V1.0。

---

## 2. V1.1 改版目的

V1.0 已建立完整製片標準，但日常操作仍可能形成：

`ChatGPT 產出 → 人工交給 Codex → Codex 上傳 GitHub／Drive → 回到 ChatGPT`

V1.1 將流程改為：

`Mata老師＋ChatGPT 製片 → ChatGPT 直接同步 GitHub／Drive → Codex 僅處理首次建置與系統維護`

目標是減少重複交接、手動下載、重新上傳與多平台往返，同時保留可稽核的版本與資產紀錄。

---

## 3. 權責架構

### 3.1 ChatGPT｜日常製片中樞與同步執行者

ChatGPT 負責：

- 每集的 Brief、策略、Hook、故事、旁白、視覺規劃、Storyboard、Prompt 與 QC。
- 在每個合法事件發生時，直接操作已連接的 GitHub 與 Google Drive。
- 建立每集 GitHub 文字狀態檔與 Drive 資產資料夾。
- 每次重大 Lock 後立即同步，不等整支影片完成才補整理。
- 圖片 PASS 後上傳 Drive、取得真實 File ID，再更新 GitHub 索引與狀態。
- 驗證工具回傳成功後才宣告完成。
- 發現漏步驟時主動補齊版本號、Production Log、Asset Index 與狀態紀錄。

ChatGPT 不得：

- 依賴聊天記憶取代正式檔案。
- 在沒有工具成功回應時聲稱已上傳、已同步或已提交。
- 修改任何既有 LOCKED／FINAL／MASTER／APPROVED／EXACT 檔案。
- 在人工 Gate 或 QC 尚未核准時自行推進。

### 3.2 GitHub｜文字規格、狀態與索引的權威來源

GitHub 保存：

- System Specs、SOP Addendum、Runtime Rules。
- Episode Master、Storyboard Master、Production State、Production Log。
- Asset Index：Drive File ID、SHA-256、狀態、版本與父資料夾 ID。
- Prompt、Flow Package、Editing Manifest 等可文字化成果。

GitHub 原則：

- 私人 Repository：`huao131/MATA-AI-VIDEO-STUDIO`。
- 正式分支：`main`。
- V1.0 保持原檔；V1.1 使用新檔名或新目錄。
- 大型圖片與影片原始檔不以 GitHub 作主要儲存。

### 3.3 Google Drive｜大型資產與正式交付檔的權威來源

Google Drive 保存：

- Character／Scene／Prop／Logo Master 原始資產。
- Approved Keyframes、Flow Video、剪輯工程交接、Final 成品。
- 正式 Lock 文件的可閱讀／交付版本。
- 大型檔案與永久歸檔。

Drive 根目錄：

`MATA AI VIDEO STUDIO OS/`

Episode 根目錄：

`MATA AI VIDEO STUDIO OS/07_Episodes/EPxxx_影片名稱/`

### 3.4 Codex｜首次建置、修復與批次維護

Codex 只負責：

- Repository 首次匯入與初始化。
- 建立資料夾模板、驗證腳本、保護規則與必要的 GitHub Actions。
- 系統級結構調整、Schema Migration、批次修復與技術除錯。
- ChatGPT 連接器無法完成的特殊維護工作。

Codex 不負責：

- 每張圖片的日常上傳。
- 每個 Episode 的例行建檔、搬檔或提交。
- 每次 Lock 後的人工轉交。
- 取代 ChatGPT 的製片、故事或 QC 決策。

---

## 4. 分層真實來源

| 資料類型 | 權威來源 | ChatGPT 的責任 |
|---|---|---|
| 規格、SOP、狀態、Log、索引 | GitHub | 讀取、更新、驗證提交結果 |
| 圖片、影片、品牌原檔、Final | Google Drive | 上傳、歸位、驗證 File ID |
| 討論、提案、Gate 決策 | 當前 Episode Chat | 確認後立即同步正式來源 |
| 系統程式、驗證器、Migration | GitHub／Codex | 日常僅呼叫；維護時交由 Codex |

ChatGPT 是操作中樞，不是永久資料庫；GitHub 與 Drive 各自對其資料類型負責。

---

## 5. Episode 標準結構

### 5.1 GitHub

```text
episodes/EPxxx_產業/
├── EPISODE_MASTER.md
├── PRODUCTION_STATE.json
├── PRODUCTION_LOG.md
├── STORYBOARD_MASTER.md
├── ASSET_INDEX.json
├── prompts/
├── flow_packages/
└── editing/
```

### 5.2 Google Drive

```text
EPxxx_影片名稱/
├── 00_BRIEF/
├── 01_STRATEGY/
├── 02_STORY_LOCK/
├── 03_VISUAL_BIBLE/
├── 04_STORYBOARD/
├── 05_KEYFRAMES/
│   ├── pending/
│   ├── approved/
│   └── rejected/
├── 06_FLOW_PROMPTS/
├── 07_FLOW_VIDEO/
├── 08_EDITING/
├── 09_FINAL/
└── 99_ARCHIVE/
```

每一集必須獨立；任何 Episode 的設定不得污染其他 Episode。

---

## 6. 事件驅動同步規格

### EVENT 01｜NEW EPISODE

ChatGPT 必須：

1. 確認 Episode ID 與名稱。
2. 在 Drive `07_Episodes` 建立標準資料夾。
3. 在 GitHub 由 Episode Template 建立文字狀態檔。
4. 寫入 Drive Episode Folder ID。
5. 驗證 GitHub 與 Drive 均成功後，才進入 `BRIEF_REVIEW`。

### EVENT 02｜MAJOR LOCK

適用：Creative Lock、Story Lock、Visual Lock、Keyframe Lock、Production Lock、Final Approved。

ChatGPT 必須：

1. 建立新版本，不覆寫既有 Lock。
2. 更新 GitHub Episode Master、State 與 Production Log。
3. 將正式可閱讀版本歸檔至對應 Drive 資料夾。
4. 寫入版本、時間、Gate 結果與 Drive File ID。
5. 完成雙端驗證後才宣告 Lock 生效。

### EVENT 03｜KEYFRAME QC

- `確認`：只重生指定問題，不建立正式資產。
- `OK`：更新紀錄，停留目前節點。
- `PASS／通過`：
  1. 上傳原始圖片至 Drive `05_KEYFRAMES/approved`。
  2. 取得真實 File ID、父資料夾 ID、檔名與上傳結果。
  3. 計算或記錄 SHA-256。
  4. 更新 GitHub `ASSET_INDEX.json`、`PRODUCTION_STATE.json`、`PRODUCTION_LOG.md`。
- `APPROVED`：PASS 已成功時才可進入下一張。
- `3+4`：PASS 完成並驗證後，再執行 APPROVED。

Rejected 資產可移至 Drive `rejected` 保存，但必須標記 `REJECTED`，禁止作為後續 Reference。

### EVENT 04｜FLOW／EDITING／FINAL

ChatGPT 必須：

1. 將 Flow Prompt、Editing Manifest 等文字成果提交 GitHub。
2. 將影片片段、剪輯交接與 Final 成品上傳 Drive 對應資料夾。
3. 更新 Asset Index、State 與 Log。
4. Final QC 完成後建立 Episode Summary 與學習分級。

---

## 7. GitHub／Drive 同步紀錄最低欄位

每筆正式資產至少包含：

```json
{
  "episode_id": "EPxxx",
  "asset_id": "A1",
  "file_name": "A1.png",
  "version": "V1.0",
  "status": "APPROVED",
  "drive_file_id": "",
  "drive_parent_folder_id": "",
  "sha256": "",
  "timestamp": "",
  "source": "ChatGPT",
  "reference_eligible": true
}
```

欄位未取得時必須保留空值並標記同步失敗，不得猜測。

---

## 8. 自動化邊界

### 可由 ChatGPT 日常直接完成

- 建立 Episode Drive 資料夾。
- 建立／更新 GitHub 文字檔。
- 上傳圖片與文件至 Drive。
- 移動 pending／approved／rejected 資產。
- 寫入 File ID、版本、狀態與 Production Log。
- 讀回 GitHub／Drive 驗證同步結果。

### 仍需 Mata老師操作

- 人工 Gate 與 QC 決策。
- Flow 無正式 API 時的最終生成按鍵。
- 剪映無正式 API 時的實際剪輯。
- 外部服務要求重新登入或逐檔授權時的授權動作。

### 交由 Codex 的例外

- Repository 首次建置。
- 驗證腳本、GitHub Actions、Schema 或 Migration 的技術維護。
- 大量歷史資料修復。
- 連接器無法完成且需要本機 Git／程式處理的特殊任務。

---

## 9. 失敗與復原

- GitHub 成功、Drive 失敗：狀態標記 `DRIVE_SYNC_FAILED`，不得推進。
- Drive 成功、GitHub 失敗：狀態標記 `GITHUB_SYNC_FAILED`，保留 File ID 待補寫。
- 權限不足：停止該資產，不繞過權限；列出唯一需要 Mata老師處理的授權項目。
- 資產與索引不一致：以 Drive 真實 File ID 與 SHA 驗證，修復索引後再推進。
- 重試不得建立未標記的重複正式檔；必要時使用新版本號。

---

## 10. 日常啟動程序

每次開始 Episode 工作，ChatGPT 依序：

1. 讀取 GitHub V1.0 FINAL／LOCKED 與本 V1.1。
2. 讀取 Episode Master、Production State、Asset Index、Storyboard Master。
3. 從 Drive 驗證本次所需 Master 與 Previous Approved Frame。
4. 輸出 PRE-FLIGHT 與唯一合法下一步。
5. 執行製片工作。
6. 於事件發生時自動同步 GitHub＋Drive。

不再要求 Mata老師先下載檔案、另開 Codex、再回來繼續日常製片。

---

## 11. V1.1 鎖定驗收紀錄

V1.1 已依以下條件完成驗收並標記 LOCKED：

- V1.0 FINAL／LOCKED 檔案 SHA-256 全部不變。
- 私人 GitHub Repository 可讀寫。
- Google Drive Episode 根目錄可讀寫。
- NEW EPISODE 測試可同時建立 GitHub 與 Drive 結構。
- KEYFRAME PASS 測試可取得 Drive File ID 並寫回 Asset Index。
- 同步失敗時不會錯誤推進狀態。
- 日常流程不需要 Codex 人工接力。

**END OF ARCHITECTURE V1.1｜FINAL／LOCKED**
