# HISTORY TODAY PROJECT CHAT STARTUP PROTOCOL V1.0

Status: CURRENT_EFFECTIVE
Effective date: 2026-08-03
Scope: ChatGPT Project、Work、Codex、Renderer Orchestrator

## 1. 通關密語

### A. 新的一天／新 Episode

使用者輸入：

`[歷史上的今天]`

系統必須自動：

1. 讀取 `docs/history_today/HISTORY_TODAY_MASTER_DATABASE_CURRENT.json`。
2. 依 CURRENT 讀取所有 `required_startup_reads`。
3. 取得使用者當地日期，建立當日 Episode；若日期或主題不明確，才詢問一次。
4. 檢查當日是否已有 Production Input Lock、Production State、Asset Index。
5. 新 Episode 不得繼承前一日的主題、人物、Scene Prompt 或資產；只繼承 Global／Series 規格。
6. 先回報：

```text
STARTUP_MODE = NEW_EPISODE
CURRENT_SPEC =
ACTIVE_DATE =
ACTIVE_EPISODE =
PRODUCTION_INPUT_LOCK =
PRODUCTION_STATE =
NEXT_ACTION =
```

7. 依 Master Database 執行企劃、旁白、分鏡、Voice-first 與後續流程。
8. 視覺生成強制使用 Single Frame Golden Path：One Frame = One Image Generation Invocation；START 與 END 分開；每次只傳入當前 Scene 的純畫面描述。

### B. 同一 Episode 做到一半後繼續

使用者輸入：

`[繼續歷史上的今天]`

系統必須自動：

1. 讀取 `HISTORY_TODAY_MASTER_DATABASE_CURRENT.json` 與全部 `required_startup_reads`。
2. 搜尋本專案中最近一個尚未完成的《歷史上的今天》Episode。
3. 讀取該 Episode 的 Production Input Lock、Production State、Asset Index、QC 與最後完成資產。
4. 不得重做已 PASS、APPROVED 或 LOCKED 的步驟。
5. 不得重新詢問已存在於正式文件中的旁白、分鏡、Scene 數、品牌規格或生圖規則。
6. 若有多個未完成 Episode，必須列出候選並只詢問要接續哪一集。
7. 先回報：

```text
STARTUP_MODE = RESUME_EPISODE
ACTIVE_EPISODE =
LAST_COMPLETED_ACTION =
ACTIVE_SCENE =
ACTIVE_FRAME_ROLE =
BLOCKER =
NEXT_ACTION =
```

8. 從 `NEXT_ACTION` 繼續，不得從頭重啟。

## 2. 單張生圖永久規則

每一張圖都必須是獨立 image generation invocation。

允許送入 Renderer 的內容只有：

- Episode ID
- 當前 Scene ID
- Frame role：START 或 END
- 當前單張純畫面描述
- 9:16
- 禁止文字、字幕、Logo、表格、拼貼的負面限制

禁止送入：

- 完整 Storyboard
- 其他 Scene
- START 與 END 同時生成
- 完整旁白
- Markdown 表格
- 工作流程說明
- 品牌、字幕或片尾規則

執行順序：

```text
Scene N START
→ QC
→ Scene N END
→ QC
→ Flow／Meta Prompt
→ Scene N+1 START
```

## 3. 角色分工

- ChatGPT：每日製片控制中心、讀取狀態、逐張生圖、Flow／Meta Prompt、回報進度。
- Work：規格治理、版本審查、CURRENT／LOCK／SUPERSEDED 管理，不負責日常生圖。
- Codex：Runner、Watcher、QC、保存、索引與工程修復，不作為每日人工必經操作介面。
- GitHub：永久規格與版本記憶。
- OneDrive：正式 Episode 資產。
- Production State：跨 Chat 接續位置的唯一依據。

## 4. Fail-Closed

若 CURRENT、Startup Protocol、Single Frame Golden Path 或 Episode Production State 無法讀取：

- 不得猜測。
- 不得沿用前一日 Episode。
- 不得開始生圖。
- 必須回報缺失檔案、讀取失敗原因與唯一需要使用者確認的事項。

## 5. 使用者最低操作

新的一天只需輸入：

`[歷史上的今天]`

中斷後繼續只需輸入：

`[繼續歷史上的今天]`

不得要求使用者每天重新敘述既有規格。