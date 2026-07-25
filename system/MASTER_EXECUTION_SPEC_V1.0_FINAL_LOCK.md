# MATA AI VIDEO STUDIO｜MASTER EXECUTION SPEC V1.0

**Status：FINAL／LOCKED**  
**Owner：Mata老師**  
**Canonical Source：Git Repository**  
**Formal Archive：Google Drive／MATA AI VIDEO STUDIO OS／02_System Specification**  
**Rule：本文件不得直接覆寫；任何正式修訂必須建立 V1.1、V1.2 或 V2.0。**

---

## 1. 系統目的

MATA AI VIDEO STUDIO 是 AI 影片製片系統，不是單純聊天流程。系統必須在不依賴模型自行回憶的情況下，穩定完成：影片策略、Hook、劇情、旁白、視覺規劃、角色與場景母版、Storyboard、Keyframe、AI 影片生成、剪映交接、Final QC、歸檔與知識沉澱。

最高成果標準：完成可公開、可代表 Mata、可作為教學案例的高品質 AI 影片作品。

---

## 2. 唯一真實來源架構

### 2.1 三層資料責任

1. **Git Repository：規則、文字母版、狀態與索引的唯一真實來源。**
2. **Google Drive：正式大型資產、核准圖片、影片片段、交付檔與備份。**
3. **ChatGPT Project：創意討論、人工 Gate、圖像生成與製片操作介面。**

ChatGPT 的聊天記憶不得被視為正式資料庫。任何工作開始前，必須重新讀取 Repository 內的規格與 Episode 狀態。

### 2.2 共用規則與單集資料隔離

- 共用規則存於 `system/`。
- 每支影片存於獨立 `episodes/<EPISODE_ID_名稱>/`。
- 一支影片＝一個獨立 Chat。
- Episode 設定不得污染其他影片。
- Series 共用角色或場景只能透過明確的 Series Master 引用，不得自行推測。

---

## 3. 強制啟動程序（PRE-FLIGHT）

任何影片工作開始前，AI 必須依序載入並驗證：

1. `AGENTS.md`
2. `system/MASTER_EXECUTION_SPEC_V1.0_FINAL_LOCK.md`
3. 目前 Episode 的 `EPISODE_MASTER.md`
4. `PRODUCTION_STATE.json`
5. `ASSET_INDEX.json`
6. `STORYBOARD_MASTER.md`
7. 本次工作所需的 Character／Scene／Prop／Logo Master
8. Previous Approved Frame（若非第一張）

只要任何必要項目缺失、版本不一致、狀態不合法或資產不存在，必須停止，不得生成、不得自行補腦。

PRE-FLIGHT 必須輸出機器可讀結果：

```text
PRE-FLIGHT
Episode: <ID>
Runtime State: <STATE>
Story Lock: PASS/FAIL
Character Master: PASS/FAIL
Scene Master: PASS/FAIL
Prop Master: PASS/FAIL
Exact Asset: PASS/FAIL
Previous Approved Frame: PASS/FAIL/N/A
Next Legal Action: <ACTION>
```

---

## 4. 版本與鎖定規則

### 4.1 正式狀態

`DRAFT → REVIEW → LOCKED → APPROVED → FINAL APPROVED → CLOSED`

### 4.2 不可違反規則

- 已標示 `LOCKED／MASTER／APPROVED／FINAL` 的內容不得直接修改。
- 修改已鎖定內容必須建立新版本。
- 視覺生成失敗不等於故事失敗。
- 圖片重生只修改指定視覺問題，不得擅自修改 Story、Character、Scene 或 Ending。
- Rejected 版本不得成為後續 Reference。
- 最新正式 LOCK 版本高於聊天舊內容與 Draft。

---

## 5. New Episode Workflow

### 5.1 NEW EPISODE BRIEF

必須建立：Episode ID、主題、目的、核心受眾、秒數、平台、比例、希望觀眾行動、特殊要求、系列、既有角色／場景引用。

已知資訊直接帶入，只詢問真正影響製作的重要缺口。

### 5.2 Audience Insight

輸出：表層痛點、深層痛點、核心渴望、錯誤認知、觀看動機、行動阻力、最值得攻擊的核心認知。

### 5.3 Hook Strategy

支援 AI 推薦、使用者複選、半指定＋AI 搭配。建立 Primary Hook、Supporting Hooks、Hook Psychological Path，並提出高停留、高共鳴、高轉化三案。

確認後建立 `CREATIVE LOCK V1.0`。

### 5.4 Story Development

先建立 Story Treatment：Opening、Conflict、Escalation、Turning Point、Solution、Result、Ending；同步規劃情緒曲線、Retention 節點與 CTA 銜接。故事方向未確認前，不大量生成圖片。

### 5.5 Story & Visual Lock

建立完整劇情、旁白／對白、時間軸、Character Bible、Scene Bible、Prop Continuity、Lighting Progression、Exact Asset List、Segment Structure、Keyframe Structure、Storyboard Master Sheet。

確認後建立 `STORY LOCK` 與 `VISUAL LOCK`。

---

## 6. Segment 與 Keyframe 規格

- 每個影片 Segment 依故事需求配置，不套用其他影片固定編號。
- **每個 Segment 至少 2 張 Keyframe（首＋尾）。**
- 動作、情緒或空間變化較大時使用 3 張（首＋中＋尾）。
- 每個 Keyframe 必須定義：ID、Segment、時間、故事功能、人物、動作、場景、情緒、光線、Continuity、Exact Asset、Generation Dependency。
- 圖片數量由 Segment 與動作需求決定，不得簡化為一句旁白一張圖。

---

## 7. 母版與資產規則

### 7.1 資產分類

- `LOCKED`：不可改動的正式設定。
- `REFERENCE`：必須引用但可有合理構圖變化。
- `FLEXIBLE`：允許依鏡頭調整。
- `EXACT`：必須使用原始檔，不得生成式重繪。

### 7.2 母版必要項目

每集依需求建立：Logo Master、Character Master、Scene Master、Prop Master、Previous Approved Frame。

### 7.3 Exact Asset

官方 Logo、QR Code、品牌文字、正式產品包裝與指定原始素材皆屬 EXACT ASSET。生成畫面時原則上不生成 Logo 或精確品牌文字；於後製使用原始檔置入。不得將 AI 生成的近似 Logo 當成正式版本。

---

## 8. Keyframe Production Runtime

### 8.1 生成前強制檢查

每次生成只允許改變 Storyboard 指定的動作、表情、鏡位或故事狀態。以下項目必須固定：

- Story Lock
- Character identity 與服裝
- Scene geometry、材質、光線與固定道具
- Prop Continuity
- Aspect ratio
- Previous Approved Frame continuity
- Exact Asset policy

### 8.2 批次原則

依 Generation Dependency 每批生成 2～3 張；但每張生成完成後必須個別進入 QC Gate，不得自動略過人工核准。

### 8.3 圖片生成後強制狀態

圖片生成完成後，系統必須立刻進入 `QC_WAITING`，停止其他分析與建議，只顯示下列指令：

1. `確認`：方向正確但需修改；依指定問題重生，不儲存正式版本。
2. `OK`：核准使用；更新 Asset Library 與 Production Log，但停留目前節點。
3. `PASS／通過`：正式鎖定、實際上傳 Google Drive、寫入 Drive File ID。
4. `APPROVED`：本張流程完成，進入下一個合法 Keyframe。
5. `3+4`：先執行 PASS；確認 Drive 上傳成功與狀態寫入成功後，再執行 APPROVED。

在 `QC_WAITING` 狀態，AI 禁止：自行生成下一張、重新規劃故事、增加新 SOP、將數字當成圖片編號、聲稱未實際完成的上傳已成功。

---

## 9. Runtime State Machine

合法狀態：

- `NEW_EPISODE`
- `BRIEF_REVIEW`
- `CREATIVE_GATE`
- `STORY_DEVELOPMENT`
- `STORY_VISUAL_GATE`
- `KEYFRAME_READY`
- `KEYFRAME_GENERATING`
- `QC_WAITING`
- `ASSET_UPLOADING`
- `NEXT_KEYFRAME`
- `KEYFRAME_LOCKED`
- `FLOW_PACKAGE_READY`
- `FLOW_GENERATION`
- `FLOW_QC`
- `PRODUCTION_LOCKED`
- `EDITING_PACKAGE_READY`
- `FINAL_QC`
- `FINAL_APPROVED`
- `EPISODE_CLOSED`

狀態只能依 `system/RUNTIME_STATE_MACHINE_V1.0.md` 的合法轉移進行。每次狀態改變必須寫入 `PRODUCTION_STATE.json` 與 `PRODUCTION_LOG.md`。

---

## 10. Google Drive 儲存規格

共用 OS：

```text
MATA AI VIDEO STUDIO OS/
├── 00_MASTER SOP V1.0（LOCK）/
├── 01_MASTER SOP V2.0 Draft/
├── 02_System Specification/
├── 03_Change Log/
├── 04_AI Decision Log/
├── 05_Series Masters/
├── 06_GitHub Repository Scaffold/
└── 09_SAB｜Standard Asset Blueprint/
```

單集：

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

Drive 上傳成功的最低證據：File ID、檔名、父資料夾 ID、上傳時間、狀態。沒有工具成功回應，不得宣稱完成。

---

## 11. Flow Production

Keyframe Lock 後，每個 Segment 建立 Flow Production Package：Segment ID、故事任務、輸入圖片、生成模式、建議模型、人物鎖定、場景鎖定、道具、主要／次要動作、鏡頭運動、光線進程、Continuity Risk、Negative Constraints、Ending State、完整 Prompt。

依需求選擇單圖、首尾影格或多圖參考；圖片不是越多越好。

Flow 生成結果分類：`APPROVED／APPROVED_WITH_EDIT／REGENERATE／REBUILD_SEGMENT`。

若 Flow 無正式可用 API，系統執行半自動：自動建立素材包、提示詞與操作清單，由 Mata老師在 Flow 完成最終生成按鍵；結果回存 Drive 並更新狀態。

---

## 12. 剪映 Editing Handoff

Production Lock 後自動建立：核准片段順序、每段時間、旁白、字幕／SRT、Ending、官方 Logo、CTA、BGM、音效節點、轉場、Editing Timeline、Editing Manifest、Final Asset List。

ChatGPT／系統負責剪輯決策與交接規劃；剪映負責實際後製。若無正式 API，不得假設可直接控制剪映；採半自動交接包。

---

## 13. Final QC 與結案

檢查：內容、視覺、聲音、節奏、技術、品牌。Logo、品牌名稱、字幕與 CTA 為高風險項目。確認後建立 `FINAL APPROVED`。

結案建立：Episode Summary、Production Log、Final Asset List、生成經驗、問題、成功 Prompt、可重用素材、Series 歸屬。

學習分級：Episode Learning、Series Learning、Global Learning。單集特殊規則不得直接升級成 Global Rule。

---

## 14. Codex／GitHub 執行規範

- Repository 是規則、狀態與索引的唯一真實來源。
- `AGENTS.md` 是每次 Codex 工作的入口。
- Codex 必須先讀取系統規格與 Episode State，通過驗證後才可執行。
- 所有狀態轉移由腳本驗證，不允許任意跳階段。
- Git commit 必須描述：Episode、階段、資產、版本、Gate 結果。
- 大型媒體檔存 Drive；Repository 僅存必要母版副本、索引與 Drive File ID，避免儲存大量影片。
- GitHub 建立後，ChatGPT 不會天然自動讀取；必須由連接器、Codex 工作區或製作控制台在每次執行前強制載入。

---

## 15. 自動化邊界

可高可靠自動化：資料夾、命名、Master／State 讀取、合法狀態驗證、Prompt Package、QC 選項、Drive 歸檔、Flow Package、剪映交接包、Production Log。

無 API 時採半自動：Flow 網頁生成、剪映實際剪輯。

生成式模型無法保證人物與場景每次像素級完全一致；系統以多母版引用、Previous Approved Frame、圖像編輯、嚴格 QC 與拒絕不合格版本降低漂移。不得承諾未經 QC 的生成結果百分之百正確。

---

## 16. 失敗處理

- 缺 Master：停止並列出缺項。
- Story 與 Visual 衝突：以最新 LOCK 為準，禁止生成。
- 生成失敗：保留故事，只修指定視覺問題。
- Drive 上傳失敗：停在 `ASSET_UPLOADING`，不得進入下一張。
- 狀態檔與實際資產不一致：執行驗證與修復，不得猜測。
- 發現流程問題：先記錄至 Episode／Series／Global Learning；不在製作途中無限擴張 SOP。

---

## 17. 三大人工 Gate

- GATE 01｜CREATIVE LOCK：確認做什麼故事。
- GATE 02｜STORY & VISUAL LOCK：確認故事如何被看見。
- GATE 03｜PRODUCTION LOCK：確認 AI 影片素材完成，進入後製。

除三大 Gate、QC Gate 與真正需要 Mata老師決策的問題外，AI 應主動推進，不要求反覆輸入「下一步」。

---

## 18. 最終執行原則

1. 不依賴聊天記憶；每次重新載入正式資料。
2. 不自行修改 LOCK。
3. 不自行重畫 Exact Asset。
4. 不在 QC_WAITING 狀態做其他事。
5. 不聲稱未實際成功的儲存、上傳或自動化。
6. 能局部修正不整體重生；能剪不重生。
7. 作品優先於系統擴張；現有規範足以執行時，不因追求完美系統停止作品。

**END OF MASTER EXECUTION SPEC V1.0｜FINAL／LOCKED**
