# 《歷史上的今天》AI 自動化主控資料庫 V2.4

**文件代號：** `HISTORY_TODAY_MASTER_DATABASE_V2.4`  
**狀態：** `CURRENT_EFFECTIVE / READ_FIRST / SINGLE_SOURCE_OF_TRUTH`  
**建立日期：** 2026-08-03  
**適用時區：** Asia/Taipei  
**適用範圍：** ChatGPT、Codex、Local Watcher、Runner、首尾幀 Renderer、Flow／Meta、後製、QC、OneDrive 歸檔  
**Codex Prompt：** `docs/history_today/HISTORY_TODAY_CODEX_SYSTEM_PROMPT_V2.4.md`

---

# 0. READ FIRST｜最高優先權

所有執行端在處理《歷史上的今天》前，必須先讀取：

```text
docs/history_today/HISTORY_TODAY_MASTER_DATABASE_CURRENT.json
→ docs/history_today/HISTORY_TODAY_MASTER_DATABASE_V2.4.md
→ docs/history_today/HISTORY_TODAY_CODEX_SYSTEM_PROMPT_V2.4.md
```

文件優先權：

```text
1. HISTORY_TODAY_MASTER_DATABASE_V2.4.md
2. 已核准 Golden Package／Golden Runtime
3. 當集 PRODUCTION_INPUT_LOCK
4. HISTORY_TODAY_AUTOMATION_GOLDEN_WORKFLOW_V1.0.md
5. 增量擴充文件
6. 拾光貓 Brand Asset Master
7. 舊版工作流、舊提示詞、舊聊天與測試包
8. 模型自行推測
```

低優先權內容不得覆蓋高優先權規則。

---

# 1. 啟動與 Gate

當 Mata老師說「開始製作某日期《歷史上的今天》」，若未指定題目，只能進入：

```text
DATE_RESOLUTION
→ HISTORICAL_RESEARCH
→ TOPIC_CANDIDATE_GATE
→ AWAITING_MATA_TOPIC_SELECTION
```

不得自行選題、寫旁白、生成圖片、建立 5 Scene、鎖定 Creative 或啟動 Runner。

完整 Gate：

```text
STAGE_00 DATE_RESOLUTION
STAGE_01 HISTORICAL_RESEARCH
STAGE_02 TOPIC_CANDIDATE_GATE
STAGE_03 MATA_TOPIC_SELECTION
STAGE_04 STORY_DIRECTION_GATE
STAGE_05 HOOK_GATE
STAGE_06 NARRATION_GATE
STAGE_07 STORYBOARD_GATE
STAGE_08 PRODUCTION_INPUT_LOCK
STAGE_08A AUTO_CONTINUE_TRIGGER
STAGE_09 EPISODE_CREATION
STAGE_09A SCENE_STATE_DESIGN
STAGE_10 START_FRAME_RENDER
STAGE_10A START_FRAME_QC_AND_SAVE
STAGE_10B END_FRAME_RENDER
STAGE_10C END_FRAME_QC_AND_SAVE
STAGE_10D VIDEO_PROMPT_GENERATION
STAGE_10E FLOW_OR_META_EXECUTION
STAGE_11 VOICE_GENERATION
STAGE_12 VOICE_CHECKPOINT
STAGE_13 VOICE_FIRST_TIMING
STAGE_14 V6_CAMERA_MOTION
STAGE_15 AUDIO_DESIGN
STAGE_16 FIXED_ENDING
STAGE_17 GRAPHICS_AND_SUBTITLE_RECOMPOSITION
STAGE_18 CANONICAL_QC
STAGE_19 FIRST_DRAFT_MASTER
STAGE_20 MATA_REVIEW_GATE
STAGE_21 FLOW_UPGRADE_OPTIONAL
STAGE_22 EDIT_DELIVERY_OPTIONAL
STAGE_23 FINAL_QC
STAGE_24 ARCHIVE
```

狀態定義：`PENDING / AWAITING_MATA / APPROVED / PASS / LOCKED / BLOCKED_BY_* / FAIL / NOT_REQUESTED`。

---

# 2. 核准後自動續跑

當 Topic、Story Direction、Hook、Voice Script、Storyboard、Production Mode 均核准並建立 `PRODUCTION_INPUT_LOCK` 後：

```text
AUTO_CONTINUE = TRUE
NO_ADDITIONAL_CONFIRMATION_REQUIRED = TRUE
PRODUCTION_INPUT_LOCK = LOCKED
RUNNER_STATUS = STARTING
AUTO_SAVE = TRUE
SAVE_TRIGGER = ON_QC_PASS_OR_MATA_APPROVAL
VIDEO_MODE = FLOW_OR_META_FULL_DYNAMIC
STATIC_VIDEO_MODE = DISABLED
```

系統不得再次詢問是否繼續；必須自動跑到 `MASTER_PREVIEW` 或明確技術阻擋點。

合法停止條件：

- 缺少不可替代正式資產。
- 外部服務未連接或授權失效。
- Flow 點數未獲核准。
- 技術錯誤已達最大重試。
- 需要 Mata老師做內容或成片層級決策。

停止格式：

```text
AUTO_PIPELINE = BLOCKED
BLOCK_REASON = <具體原因>
COMPLETED_STAGES = <已完成項目>
NEXT_RECOVERY_ACTION = <下一個可執行修復>
```

---

# 3. 角色分工

## ChatGPT

負責日期、研究、候選題、故事方向、Hook、旁白、5 Scene Storyboard、Production Input Lock、Prompt Package、Runner 啟動、QC 結果與成片驗收。

## Codex

負責 Episode 目錄、Production Input 驗證、視覺素材接入、Edge TTS、Voice Checkpoint、Voice-first Timing、Camera Motion、Audio、固定片尾、雙語字幕、QC、Asset Index、Production State、Log、SHA256 與 OneDrive 歸檔。

Codex 不得改寫已核准內容、自行換聲線、使用機械音、廉價替代品或修改 Golden Package。

## Mata老師

負責 Topic、Story Direction、Hook、完整旁白、Storyboard、Production Mode、第一版成片與最終發布核准。

---

# 4. Storyboard Deliverable Boundary

製片分鏡是必要 Gate，但正式格式只能是 Markdown／JSON／YAML／資料庫欄位。

```text
STORYBOARD_PLAN = REQUIRED
STORYBOARD_APPROVAL = REQUIRED
STORYBOARD_VISUAL_SHEET = OPTIONAL_REFERENCE_ONLY
STORYBOARD_VISUAL_SHEET_TO_RENDERER = FORBIDDEN
```

16:9 分鏡總覽圖不是首尾幀必要資產，也不得送入 Renderer。

正確順序：

```text
TEXT_OR_JSON_STORYBOARD
→ MATA_APPROVAL
→ STORYBOARD_LOCK
→ SCENE_STATE_DESIGN
→ START_FRAME_PROMPT
→ START_FRAME_RENDER
→ END_FRAME_PROMPT
→ END_FRAME_RENDER
→ FLOW_OR_META_VIDEO_PROMPT
```

---

# 5. Renderer Isolation

```text
ONE_SCENE = ONE_ISOLATED_RENDER_CONTEXT
ONE_REQUEST = ONE_START_OR_END_FRAME
OUTPUT_ASPECT_RATIO = 9:16
OUTPUT_RESOLUTION = 1080x1920
OUTPUT_TYPE = SINGLE_FULL_FRAME_CINEMATIC_IMAGE
```

每次只允許當前 Scene。永久禁止：

- 16:9 分鏡板。
- 多格拼貼與資訊圖表。
- 字幕、標題、Logo、編號、UI、框線或任何文字。
- 五幕一起生成再裁切。
- 前一 Scene Context 污染下一 Scene。

每個 Scene 必須建立：

```yaml
scene_narration:
narrative_start_state:
narrative_end_state:
visible_change:
emotional_change:
composition_change:
scale_change:
lighting_change:
next_scene_handoff:
start_frame_prompt:
end_frame_prompt:
video_motion_prompt:
video_negative_prompt:
camera_path:
subject_motion:
object_motion:
environment_motion:
physics_constraints:
identity_constraints:
historical_constraints:
duration_target:
video_tool:
fallback_tool:
qc_checklist:
```

永久定義：

```text
DYNAMIC_SCENE = START_FRAME + END_FRAME + VIDEO_PROMPT
VIDEO_TOOL = FLOW_OR_META
STATIC_VIDEO_MODE = DISABLED
```

---

# 6. Renderer Fail Recovery｜錯圖必須自動修復並續跑

以下任一情況立即判定 `RENDER_FAIL`：

- 非 9:16。
- 分鏡表、資訊圖表、拼貼、多格版面。
- 字幕、標題、Logo、編號、UI、邊框或任何文字。
- Scene 內容與 Story State 不符。
- Start／End State 錯置。
- 前一幕人物、構圖或版面污染。

禁止只回覆「不對」「我錯了」後停止。必須執行：

```text
RENDER_FAIL
→ REJECT_AND_ARCHIVE_FAILED_ASSET
→ CLEAR_RENDER_CONTEXT
→ REBUILD_MINIMAL_SINGLE_SCENE_PROMPT
→ REGENERATE_SAME_TARGET
→ AI_QC
→ IF_PASS_AUTO_SAVE
→ AUTO_CONTINUE_TO_NEXT_FRAME
```

重試政策：

```yaml
max_attempts_per_asset: 3
attempt_1: original isolated prompt
attempt_2: stricter single-frame prompt + explicit forbidden layout list
attempt_3: fully reset renderer context + minimal prompt only
on_pass: auto_save_and_continue
on_final_fail: mark_scene_asset_blocked_but_continue_other_preparable_assets
```

同一張失敗先重做同一張；通過後立即進入下一張。三次失敗才可標記 `SCENE_ASSET_BLOCKED`，但其他可準備工作仍需續跑。

---

# 7. 全動態 Flow／Meta 模式

正式模式只允許：

```text
FLOW_FULL
META_FULL
FLOW_META_MIXED
```

停用：

```text
IMAGE_V6
STATIC_FIRST_DRAFT
HYBRID_WITH_STATIC_SCENES
KEN_BURNS_AS_FINAL_SCENE
```

五幕流程：

```text
CONTENT_LOCK
→ VIDEO_TOOL_MODE
→ 5_SCENE_STATE_DESIGN
→ 5_START_FRAMES
→ QC_AND_SAVE
→ 5_END_FRAMES
→ QC_AND_SAVE
→ 5_FLOW_OR_META_PROMPTS
→ SAVE
→ 5_DYNAMIC_CLIPS
→ VOICE_FIRST_POST
→ MASTER_PREVIEW
```

工具失敗時只重試該 Scene，必要時切換 Flow／Meta；不得改動旁白、首尾幀或 Story State。

---

# 8. Voice-first 與聲音

正式配音：

```text
Engine = Microsoft Edge TTS
Voice = zh-TW-HsiaoChenNeural
Rate = -4%
Pitch = -2Hz
Mode = 全篇旁白一次生成
```

順序：

```text
VOICE_SCRIPT_LOCK
→ GENERATE_FULL_VOICE
→ VOICE_CHECKPOINT
→ READ_ACTUAL_DURATION
→ RETIME_5_SCENES
→ CAMERA_MOTION
→ SUBTITLE
→ AUDIO_DESIGN
```

聲音必須包含：

```text
VOICE + MUSIC + SPACE / AMBIENCE / SFX
```

並執行 Ducking、Audio Master、Scene Transition、Emotional Curve 與片尾聲音收束。

固定片尾使用已核准《時光翻頁｜品牌片尾 V1.0》，禁止重新生成替代片尾。

---

# 9. 字幕與品牌

上方固定：

- `歷史上的今天`
- 暖金細線。
- 日期＋人物／事件英文小標。
- 暖金 Serif 質感。

下方固定：

- 薄型深色半透明橫幅。
- 繁體中文主字幕。
- 英文小字幕。
- 中文較大、英文較小。

左下固定：

```text
AI加速研究院・MATA
```

不得自行更名、換 Logo 或重新生成拾光貓。拾光貓必須遵守 Brand Asset Master：三腳橘白虎斑幼貓、左前腳缺失、右前腳完整、禁止第四腳、禁止水平鏡像、`SL` 固定。

---

# 10. Auto-save 與 OneDrive

```text
AUTO_SAVE = TRUE
MANUAL_DOWNLOAD_REQUIRED = FALSE
SAVE_TRIGGER = ON_QC_PASS_OR_MATA_APPROVAL
ARCHIVE_MODE = CONTINUOUS
```

每個素材：

```text
ASSET_CREATED
→ QC
→ PASS_OR_APPROVED
→ WRITE_TO_EPISODE_FOLDER
→ UPDATE_ASSET_INDEX
→ WRITE_SHA256
→ UPDATE_PRODUCTION_STATE
```

正式根目錄：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\
```

每日 Episode 結構至少包含：

```text
00_控制與狀態
01_研究與來源
02_腳本與分鏡
03_圖片/01_首幀
03_圖片/02_尾幀
03_圖片/03_未採用
04_影片提示詞/01_Flow
04_影片提示詞/02_Meta
05_動態影片/01_Flow
05_動態影片/02_Meta
06_配音
07_字幕
08_音樂與音效
09_半成品
10_成品
11_QC與Log
12_剪映交付包
13_Canva交付包
14_封存
```

不得要求 Mata老師逐張下載、改名或整理。Rejected 資產不得與正式資產混放。

---

# 11. Canonical QC

至少驗證：

- 日期、史實、主題、Hook、旁白與 Scene 順序正確。
- 9:16、1080×1920、無拼貼、無錯誤文字、無現代物件。
- 五幕鏡位、尺度、色溫與運動有差異。
- Edge TTS 聲線、Rate、Pitch 與全篇一次生成正確。
- BGM 不壓旁白，Ambience／SFX／Ducking／Audio Master 合格。
- Header、雙語字幕、品牌與固定片尾正確。
- MASTER_PREVIEW、無主字幕 Master、QC Montage、Production State、Asset Index、Execution Log、Manifest、SHA256 全部存在。
- OneDrive Archive Gate 通過。

未完成 QC 與歸檔不得宣告完成。

---

# 12. 永久禁止

1. 跳過 Topic Gate。
2. 把推薦當核准。
3. 主題未核准就寫旁白或生成圖片。
4. 一張五格圖裁成五幕。
5. 用 eSpeak／機械音替代 Edge TTS。
6. 逐 Scene 換聲線。
7. 每張圖片都要求 Mata老師中途確認。
8. 用普通黑框取代 Canonical Header。
9. 漏掉英文小字幕。
10. 因單一模組失敗重做全部 PASS 資產。
11. 缺少資產時用廉價替代品假裝完成。
12. 修改 Golden Package 或 APPROVED／LOCKED 資產。
13. 未獲核准消耗 Flow 點數。
14. Production Input Lock 後只交付 Markdown 而不啟動下游。
15. 要求 Mata老師手動下載或整理正式資產。
16. Flow Scene 缺少 Start Frame、End Frame 或 Motion Prompt。
17. 使用 Image V6 或單張靜態圖作為正式 Scene。
18. 把 Flow／Meta Prompt 寫成靜態畫面描述，而非首尾狀態轉換。
19. Renderer 出錯後只說「不對」就停止。
20. 將 Storyboard 表格直接送進生圖器。

---

# 13. V2.4 變更鎖定

1. 製片分鏡必須先以 Markdown／JSON／YAML 完成並經 Mata老師核准。
2. 16:9 分鏡總覽圖改為選配參考，禁止作為 Renderer 必要輸入。
3. Renderer 只能接收單一 Scene、單一首幀或尾幀、單一 9:16 滿版電影畫面。
4. 錯圖必須自動重試、QC、保存並續跑，不得只回報錯誤後停止。
5. 單一資產最多自動重試三次；三次失敗才標記阻擋，但其他可執行工作仍續跑。
6. 通過的首幀／尾幀立即 Auto-save，然後自動進入下一張。
7. Codex 必須讀取 `HISTORY_TODAY_CODEX_SYSTEM_PROMPT_V2.4.md`。
8. Current Pointer 必須指向 V2.4，低版本不得自行覆蓋。

---

```text
MASTER_DATABASE_VERSION = 2.4
STATUS = CURRENT_EFFECTIVE
READ_FIRST = TRUE
SINGLE_SOURCE_OF_TRUTH = TRUE
CODEX_PROMPT_VERSION = 2.4
AUTO_CONTINUE_AFTER_LOCK = TRUE
RENDERER_ISOLATION = ENFORCED
RENDER_FAIL_AUTO_RECOVERY = ENFORCED
AUTO_SAVE = TRUE
STATIC_VIDEO_MODE = DISABLED
```

**END OF FILE — HISTORY_TODAY_MASTER_DATABASE_V2.4**
