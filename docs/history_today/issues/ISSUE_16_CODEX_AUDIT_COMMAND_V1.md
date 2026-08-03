# Issue #16｜Codex 單張 9:16 生圖 Golden Path 技術稽核與可執行化指令

## 目的

不要重新設計生圖流程，不要憑推測另做一套。請直接從 2026-08-02 `0802_BARTOLDI` 曾經成功生成五張獨立 9:16 圖片的實際執行證據反查，確認真實機制後，整理成可由 ChatGPT → GitHub → Windows Watcher → Runner 自動呼叫的模組。

## 已知成功證據

### Episode

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI
```

### 實際 Runner

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\_SYSTEM\GOLDEN_PATH_RUNTIME_V1\scripts\RUN_END_TO_END_GOLDEN_PATH.ps1
```

### Baseline Manifest

```text
C:\Users\huao3\OneDrive\文件\AI影音生成\MATA-AI-VIDEO-STUDIO-local-watcher\golden\history_today\jk_rowling_v6_2\GOLDEN_BASELINE_MANIFEST.json
```

### 已成功輸出

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI\03_視覺素材\Scene_01.png
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI\03_視覺素材\Scene_02.png
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI\03_視覺素材\Scene_03.png
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI\03_視覺素材\Scene_04.png
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI\03_視覺素材\Scene_05.png
```

五張皆曾確認：獨立 9:16、非拼貼。

### 當次執行狀態

```text
Preflight = PASS
Scene Images = PASS
Voice = FAIL
Timing / Motion / Audio / Subtitle / Ending / MASTER_PREVIEW = FAIL
OneDrive Archive = PARTIAL PASS
```

這證明圖片生成發生在 Voice Gate 之前，且不依賴後續配音與合成。

---

## 最高執行規則

1. 先做稽核，再做程式。
2. 不得重新生成新圖片來代替查證。
3. 不得修改 Golden Runtime、Golden Package、0802 正式資產。
4. 不得宣稱找到方法，除非能指出實際檔案、函式、命令、工具與證據。
5. 若圖片其實不是 Runner 生成，而是 Codex 工作階段直接生成後寫入，也必須明確證明。
6. 若找不到完整 Log，不得停止；必須用檔案時間戳、SHA256、PNG metadata、PowerShell 呼叫鏈、Git history、shell history、任務記錄與鄰近檔案反向重建。

---

# 第一階段｜本機證據稽核

## A. 列出 Episode 全部檔案

請遞迴列出：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0802\0802_BARTOLDI
```

每筆至少輸出：

- FullName
- Length
- CreationTimeUtc
- LastWriteTimeUtc
- SHA256
- 副檔名

依時間排序，建立「圖片生成前後事件時間線」。

## B. 分析五張 PNG

逐張檢查：

- 實際寬高
- PNG metadata / textual chunks
- software / generator 欄位
- ICC / EXIF / XMP
- 檔案 SHA256
- 建立與修改時間
- 是否存在相同 hash 的來源檔、暫存檔或下載檔

搜尋本機相同 SHA256，範圍至少包含：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天
C:\Users\huao3\OneDrive\文件\AI影音生成
C:\Users\huao3\Downloads
C:\Users\huao3\AppData\Local\Temp
```

## C. 追蹤 Runner 呼叫鏈

完整讀取：

```text
RUN_END_TO_END_GOLDEN_PATH.ps1
GOLDEN_BASELINE_MANIFEST.json
```

並遞迴追蹤所有：

- dot-source PowerShell
- `&` 呼叫
- `Start-Process`
- Python 呼叫
- Node / npm / npx 呼叫
- curl / Invoke-WebRequest / Invoke-RestMethod
- OpenAI / Bing / DALL-E / image generation 關鍵字
- browser automation
- clipboard / download / file copy
- `Scene_01.png`～`Scene_05.png`
- `03_視覺素材`
- prompt / renderer / image / visual / generation

輸出完整 Call Graph：

```text
RUN_END_TO_END_GOLDEN_PATH.ps1
→ script A
→ function B
→ command C
→ output Scene_01.png
```

## D. 查閱 Log 與歷史紀錄

搜尋：

- Episode 內 `*.log`, `*.json`, `*.md`, `*.txt`, `*.ps1`, `*.py`
- Golden Runtime logs
- `_VALIDATION_RUNS`
- PowerShell history
- Codex session artifacts / task logs（若本機存在）
- Git commits / untracked backup / stash
- Windows Task Scheduler history（若相關）

搜尋詞：

```text
BARTOLDI
Scene_01.png
Scene_05.png
03_視覺素材
image generation
generate image
renderer
1024x1792
1080x1920
9:16
```

## E. 判定真實來源

只能從以下類型擇一或多個，附證據：

```text
1. Golden Path Runner 自動生成
2. Codex 內建影像能力直接生成並保存
3. ChatGPT / OpenAI Image 工具生成後下載或複製
4. Python / API 生成
5. Browser automation 生成
6. 既有素材複製或重新命名
7. 其他（必須說明）
```

---

# 第二階段｜輸出稽核報告

必須建立：

```text
docs/history_today/CODEX_SINGLE_IMAGE_GOLDEN_PATH_AUDIT_V1.md
```

固定格式：

```text
IMAGE_GENERATION_METHOD =
TOOL_OR_MODEL =
ACTUAL_EXECUTION_ENTRYPOINT =
ACTUAL_CALL_CHAIN =
ISOLATED_CONTEXT =
PROMPT_SOURCE =
EXACT_PROMPT_EVIDENCE =
NEGATIVE_PROMPT_SOURCE =
ASPECT_RATIO_CONTROL =
OUTPUT_SAVE_METHOD =
OUTPUT_FILE_ORIGIN =
API_KEY_REQUIRED =
PAID_SERVICE_REQUIRED =
RELATED_FILES =
RELATED_LOGS =
TIMELINE_EVIDENCE =
HASH_EVIDENCE =
KNOWN_LIMITATIONS =
CODEX_SINGLE_IMAGE_GOLDEN_PATH = CONFIRMED / PARTIALLY_CONFIRMED / NOT_CONFIRMED
```

不得只寫摘要。每個判定要附實際路徑、行號、命令輸出或 SHA256。

---

# 第三階段｜做成可執行系統

只有 `CONFIRMED` 或具充分證據的 `PARTIALLY_CONFIRMED` 才能開始。

建立或升級：

```text
control/render_single_frame_request.schema.json
runners/modules/history_today_single_frame_renderer.py
control/windows/run_single_frame_renderer.ps1
```

介面至少支援：

```python
render_single_frame(
    episode_id,
    scene_id,
    frame_role,
    visual_prompt,
    negative_prompt,
    output_path,
    width=1080,
    height=1920,
)
```

若真實 Golden Path 不是 Python，介面可調整，但外部 Request Contract 不可缺少：

```json
{
  "request_type": "render_frame",
  "episode_id": "HISTORY_TODAY_2026_0803_COLUMBUS_DEPARTURE",
  "scene_id": "SCENE_01",
  "frame_role": "START",
  "visual_prompt": "純畫面描述",
  "negative_prompt": "禁止文字、拼貼、資訊圖表",
  "output_path": "...\\20260803_SCENE_01_START_V1.png",
  "width": 1080,
  "height": 1920
}
```

硬性要求：

- 一個 Request 只生成一張圖。
- START 與 END 為兩個獨立 Request、兩個獨立 PNG。
- 不傳完整 Storyboard、Markdown、Scene Package、表格或工作流說明。
- 每次執行必須是乾淨隔離 Context。
- 9:16 硬驗證，不合格自動拒絕。
- OCR／視覺 QC 檢查文字、拼貼、表格、Logo、UI。
- 最多重試三次。
- QC PASS 後才寫入正式 Episode 路徑。
- 更新 Asset Index、Production State、SHA256。
- START 與 END 皆 PASS 後，自動生成 Flow／Meta Prompt。

---

# 第四階段｜最小重現測試

先建立隔離測試資料夾，不得覆寫 0802：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\_VALIDATION_RUNS\issue_16_single_frame_renderer
```

測試一：單張 START

```text
輸入：純畫面 Prompt
輸出：TEST_SCENE_01_START.png
要求：獨立 9:16、無文字、無拼貼
```

測試二：START + END

```text
TEST_SCENE_01_START.png
TEST_SCENE_01_END.png
```

測試三：兩張 PASS 後自動生成：

```text
TEST_SCENE_01_FLOW_PROMPT.md
```

測試四：接入 Watcher Request / Callback。

不得消耗 Flow 點數；只驗證靜態首尾幀 Renderer 與 Prompt 產生鏈。

---

# 第五階段｜交付

必須回報：

```text
AUDIT_REPORT_PATH =
IMPLEMENTATION_FILES =
TEST_OUTPUT_PATHS =
TEST_LOG_PATH =
SHA256_MANIFEST =
COMMIT_SHA =
WATCHER_REQUEST_TEST = PASS / FAIL
START_FRAME_TEST = PASS / FAIL
END_FRAME_TEST = PASS / FAIL
FLOW_PROMPT_TEST = PASS / FAIL
AUTOMATION_READY = TRUE / FALSE
BLOCK_REASON =
NEXT_ACTION =
```

完成後將結果回覆到 GitHub Issue #16。
