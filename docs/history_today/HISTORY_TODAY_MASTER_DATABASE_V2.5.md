# 《歷史上的今天》AI 自動化主控資料庫 V2.5

**文件代號：** `HISTORY_TODAY_MASTER_DATABASE_V2.5`  
**狀態：** `CURRENT_EFFECTIVE / READ_FIRST / SINGLE_SOURCE_OF_TRUTH`  
**建立日期：** 2026-08-03  
**適用時區：** `Asia/Taipei`  
**用途：** 作為《歷史上的今天》每日新 Episode、跨 Chat 接續、單張首尾幀生成、全動態影片、後製、QC 與歸檔的唯一主控規格。  

> 本版是對 V2.4 的乾淨替代，不是增量附錄。舊事故紀錄、重複規則、失效技術路徑與額外品牌角色內容均不再置於 CURRENT 主控文件。

---

# 0. 最高原則

1. 不以聊天記憶取代正式狀態。
2. 不重做 `PASS / APPROVED / LOCKED` 的步驟。
3. 不把完整 Storyboard、流程、表格、品牌或其他 Scene 送入生圖器。
4. 每個正式 Frame 必須使用乾淨 Renderer Chat 生成。
5. 每次生圖只生成一張獨立 9:16 圖。
6. 五個 Scene 全部必須是動態影片，不允許用單張靜態圖或 Ken Burns 代替正式 Scene。
7. 動態影片工具只允許 Flow、Meta、Canva 或三者混合。
8. 未連接的外部工具、檔案系統或 Runner，不得假裝已自動執行或保存。
9. 主控文件只保留現行有效規則；歷史事故與淘汰方案另行封存。

---

# 1. 啟動通關密語

## 1.1 建立當日新 Episode

使用者輸入：

```text
[歷史上的今天]
```

系統必須：

1. 讀取 CURRENT 主控文件。
2. 取得使用者當地日期。
3. 建立當日新 Episode，或確認當日是否已存在 Episode。
4. 新 Episode 只能繼承 Global／Series 規格，不得繼承前一日主題、人物、Scene Prompt、圖片或影片。
5. 依序進入：日期查證 → 候選題 → Mata 選題 → 故事方向 → Hook → 旁白 → 5 Scene Storyboard → Production Input Lock。

首次回報只需：

```text
STARTUP_MODE = NEW_EPISODE
ACTIVE_DATE =
ACTIVE_EPISODE =
CURRENT_STAGE =
NEXT_REQUIRED_APPROVAL =
```

不得輸出冗長系統稽核清單。

## 1.2 接續最近未完成 Episode

使用者輸入：

```text
[繼續歷史上的今天]
```

系統必須優先讀取：

```text
HISTORY_TODAY_ACTIVE_PRODUCTION_STATE_CURRENT.md
```

只要短狀態檔包含下列欄位，就必須直接執行 `NEXT_ACTION`：

```text
ACTIVE_EPISODE =
PRODUCTION_INPUT_LOCK =
LAST_COMPLETED_ACTION =
ACTIVE_SCENE =
ACTIVE_FRAME_ROLE =
NEXT_ACTION =
NEXT_RENDER_PROMPT =
```

接續時只回報一行：

```text
RESUME = <Episode> / <Scene> / <Frame Role> / <Next Action>
```

禁止在狀態完整時重新列出 Gate、文件清單、品牌規格或技術稽核。

只有短狀態檔不存在、內容互相矛盾或有多個未完成 Episode 時，才進入 Recovery Gate。

---

# 2. 文件與狀態架構

## 2.1 CURRENT 指標

固定入口：

```text
docs/history_today/HISTORY_TODAY_MASTER_DATABASE_CURRENT.json
```

CURRENT 必須指向：

- 本主控文件。
- Project Chat Startup Protocol。
- Single Frame Render Golden Path。
- 當集 Active Production State Pointer。

## 2.2 每集正式文件

每個 Episode 至少包含：

```text
PRODUCTION_INPUT_LOCK.md
PRODUCTION_STATE.json
ASSET_INDEX.json
QC_LOG.md
```

## 2.3 短狀態指標

固定名稱：

```text
HISTORY_TODAY_ACTIVE_PRODUCTION_STATE_CURRENT.md
```

用途：讓同一專案中的新 Chat 不必重新稽核整套系統，即可定位下一步。

每次完成一個 Frame、Prompt、影片、Voice 或後製階段後，必須更新這份短狀態檔。

---

# 3. 角色分工

## 3.1 ChatGPT Master Chat

負責：

- 日期與史實研究。
- 候選題、故事方向、Hook、旁白與 5 Scene Storyboard。
- Production Input Lock。
- 讀取短狀態檔並決定下一步。
- 產生每張純 Renderer Prompt。
- 進行 AI QC。
- 建立 Flow／Meta／Canva 動態提示詞。
- 整合 Runner 與成片驗收結果。

Master Chat 不得直接生成正式 Frame，避免長對話上下文污染。

## 3.2 Clean Renderer Chat

負責唯一工作：

```text
ONE CLEAN RENDERER CHAT = ONE FRAME TARGET
```

每個 Renderer Chat 只能收到：

- 當前 Episode ID。
- 當前 Scene ID。
- Frame Role：START 或 END。
- 單張純畫面描述。
- 9:16 規格。
- 負面限制。

不得收到：

- CURRENT 全文。
- Production State。
- Storyboard 全文。
- 其他 Scene。
- START 與 END 同時生成。
- 完整旁白。
- 工作流程、Gate、表格、Dashboard。
- 字幕、Logo、品牌角色或片尾規則。

## 3.3 Work

負責：

- 規格治理。
- CURRENT、LOCK、SUPERSEDED 管理。
- 跨文件一致性與版本審查。

Work 不負責每日互動式生圖。

## 3.4 Codex／Local Runner

負責：

- Episode 資料夾與檔案管理。
- 配音、字幕、音訊、合成、QC、索引、SHA256、Log 與歸檔。
- 工程修復與自動化程式。

Codex 不作為每日生圖的人工必經介面，也不得改寫已核准內容。

## 3.5 Mata老師

負責核准：

- Topic。
- Story Direction。
- Hook。
- Voice Script。
- 5 Scene Storyboard。
- Video Tool Mode。
- 第一版成片與最終版。

---

# 4. 內容 Gate

正式順序：

```text
DATE_RESOLUTION
→ HISTORICAL_RESEARCH
→ TOPIC_CANDIDATE_GATE
→ MATA_TOPIC_SELECTION
→ STORY_DIRECTION_GATE
→ HOOK_GATE
→ NARRATION_GATE
→ STORYBOARD_GATE
→ VIDEO_TOOL_MODE_GATE
→ PRODUCTION_INPUT_LOCK
```

未完成上游核准，不得進入正式視覺生成。

狀態定義：

- `PENDING`
- `AWAITING_MATA`
- `APPROVED`
- `PASS`
- `LOCKED`
- `BLOCKED`
- `FAIL`
- `NOT_REQUESTED`

---

# 5. 每日選題

若使用者未指定題目，至少提供：

- 人物候選 3 個。
- 事件候選 3 個。

每項包含：

- 日期與核心史實。
- 故事角度。
- 前 3 秒 Hook。
- 視覺潛力。
- 情緒曲線。
- 適合度。
- 史實或敏感風險。

候選題只代表推薦，不代表核准。

---

# 6. 旁白與 Storyboard

## 6.1 旁白

- 使用繁體中文。
- 單一主題。
- 先故事、後畫面。
- 避免百科流水帳與無來源虛構引語。
- 原則 50～90 秒。
- Mata 核准後鎖定，不得自行改寫。

## 6.2 Voice-first

```text
VOICE_SCRIPT_LOCKED
→ 全篇一次生成配音
→ 讀取實際 Duration
→ 分配 5 Scene 時間
→ 動態片段 Retiming
```

## 6.3 5 Scene Storyboard

每幕必須包含：

- Scene 名稱。
- 對應旁白。
- Start State。
- End State。
- Visible Change。
- 人物、場景、年代與服裝。
- 鏡頭運動。
- 人物、物件與環境動態。
- 光線、色調與情緒。
- 下一幕銜接。
- Video Tool。

Storyboard 只使用 Markdown／JSON／YAML，不生成分鏡總覽圖作為正式 Renderer 輸入。

---

# 7. Production Input Lock

全部內容核准後建立：

```text
PRODUCTION_INPUT_LOCK = LOCKED
AUTO_CONTINUE = TRUE
NO_ADDITIONAL_CONFIRMATION_REQUIRED = TRUE
```

必填欄位：

```yaml
episode_date:
episode_id:
topic_title:
historical_date:
story_direction:
hook:
core_message:
voice_script:
scene_count: 5
scene_01:
scene_02:
scene_03:
scene_04:
scene_05:
video_tool_mode:
voice_profile:
subtitle_profile:
audio_profile:
ending_asset:
approval_timestamp:
approved_by: MATA
```

---

# 8. 單張圖片生成 Golden Path

## 8.1 已驗證方法

2026-08-03 對照測試已確認：

- 同一專案中的新 Chat 可以成功生成乾淨單張歷史電影畫面。
- 舊長對話容易吸收流程、Dashboard、角色與狀態語意，造成錯誤資訊圖。
- 問題不是 Master Markdown 本身，也不是專案指令本身。
- 正式 Frame 必須在乾淨 Renderer Chat 中生成。

正式規則：

```text
ONE FRAME
= ONE CLEAN RENDERER CHAT
= ONE IMAGE GENERATION INVOCATION
= ONE OUTPUT IMAGE
```

## 8.2 固定順序

每個 Scene 嚴格依序：

```text
START FRAME
→ AI QC
→ SAVE / REGISTER
→ END FRAME
→ CONTINUITY QC
→ SAVE / REGISTER
→ FLOW / META / CANVA VIDEO PROMPT
→ ANIMATED CLIP
→ NEXT SCENE
```

## 8.3 Renderer Prompt Contract

每次 Prompt 只能包含：

```text
只生成一張獨立的直式 9:16 電影畫面。

<當前單張純畫面描述>

禁止任何文字、字幕、Logo、表格、UI、資訊圖表、拼貼、多格版面、Dashboard、品牌角色或製作流程。
```

## 8.4 輸出規格

- 單一滿版畫面。
- 直式 9:16。
- 建議 1080×1920 或模型可提供的最接近原生比例。
- 無文字。
- 無字幕。
- 無 Logo。
- 無 UI。
- 無表格。
- 無拼貼。
- 無 Storyboard Grid。

檔名：

```text
YYYYMMDD_SCENE_XX_START_V1.png
YYYYMMDD_SCENE_XX_END_V1.png
```

## 8.5 QC

每張至少檢查：

- 是否只有一張圖。
- 是否 9:16。
- 是否無文字、表格、拼貼、Dashboard。
- 是否符合當前 Scene 與 Frame Role。
- 是否年代、服裝、人物、船隻與場景合理。
- END 是否與 START 具備清楚的敘事變化與連續性。

不合格最多重試 3 次。每次重試仍必須使用新的乾淨 Renderer Chat 或完全乾淨的 Renderer Context。

---

# 9. 五幕全動態影片

## 9.1 正式模式

五個 Scene 全部必須生成為動畫影片。

允許模式：

```text
FLOW_FULL
META_FULL
CANVA_FULL
FLOW_META_MIXED
FLOW_CANVA_MIXED
META_CANVA_MIXED
FLOW_META_CANVA_MIXED
```

禁止模式：

```text
STATIC_FIRST_DRAFT
IMAGE_V6_VIDEO
KEN_BURNS_AS_FINAL_SCENE
SINGLE_IMAGE_AS_FINAL_CLIP
```

## 9.2 每幕動態套件

```yaml
scene_narration:
start_frame_asset:
end_frame_asset:
visible_change:
video_tool:
video_motion_prompt:
video_negative_prompt:
camera_path:
subject_motion:
object_motion:
environment_motion:
physics_constraints:
historical_constraints:
identity_constraints:
duration_target:
next_scene_handoff:
fallback_tool:
```

## 9.3 動態提示詞

正式影片提示詞只能在 START 與 END 都 PASS 後建立，且必須描述：

- 從 START 到 END 的動態轉換。
- 鏡頭路徑。
- 人物動作。
- 物件動作。
- 環境動態。
- 光線變化。
- 物理限制。
- 歷史一致性。
- 禁止新增角色、船隻、建築或現代物件。

## 9.4 工具失敗回退

任一 Scene 失敗時只重試該 Scene。必要時可切換 Flow、Meta 或 Canva，但不得改變已核准旁白、Story State、START 或 END Frame。

---

# 10. 配音

正式設定：

```text
Engine = Microsoft Edge TTS
Voice = zh-TW-HsiaoChenNeural
Rate = -4%
Pitch = -2Hz
Mode = 全篇旁白一次生成
```

Voice Gate 必須確認：

- 可播放與可解碼。
- Duration 可讀取。
- 聲線正確。
- 無機械音替代。
- 無逐句換聲線。

Voice 失敗時只修 Voice，不重做已 PASS 視覺資產。

---

# 11. 後製

## 11.1 字幕與版型

- 上方固定系列標示：`歷史上的今天`。
- 暖金細線與日期／事件小標。
- 下方薄型深色半透明字幕帶。
- 繁中主字幕＋英文小字幕。
- 左下品牌文字：`AI加速研究院・MATA`。

## 11.2 聲音

三層架構：

```text
VOICE + MUSIC + SPACE / AMBIENCE / SFX
```

包含：

- 開場慢速 Tick。
- Scene 切換約 0.75 秒翻頁／Whoosh。
- 年代與地點 Ambience。
- Emotional Lift。
- Ducking。
- Audio Master。

建議基準：

```text
Target Loudness = -16 LUFS
True Peak Max = -1.5 dBTP
Sample Rate = 48 kHz
Channels = Stereo
```

## 11.3 固定片尾

使用已核准《時光翻頁｜品牌片尾 V1.0》。片尾為獨立影片資產，在後製時接入，不在歷史 Scene 生圖 Prompt 中提及。

---

# 12. 保存與歸檔

正式根目錄：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\
```

建議 Episode 結構：

```text
YYYY\MM\MMDD_TOPIC\
  00_控制與狀態\
  01_研究與來源\
  02_腳本與分鏡\
  03_圖片\01_首幀\
  03_圖片\02_尾幀\
  03_圖片\03_未採用\
  04_影片提示詞\01_Flow\
  04_影片提示詞\02_Meta\
  04_影片提示詞\03_Canva\
  05_動態影片\01_Flow\
  05_動態影片\02_Meta\
  05_動態影片\03_Canva\
  06_配音\
  07_字幕\
  08_音樂與音效\
  09_半成品\
  10_成品\
  11_QC與Log\
  12_剪輯交付包\
  13_封存\
```

保存規則：

- Runner 已連接時，QC PASS 後自動保存、更新 Asset Index、SHA256 與 Production State。
- Runner 未連接時，明確標記暫存路徑與待匯入狀態，不得宣稱已寫入 OneDrive。
- Rejected 資產移入未採用資料夾。
- 修正不得覆寫同版本，必須升版。

---

# 13. Canonical QC

## Content

- 日期、人物、事件正確。
- 旁白與 Storyboard 為鎖定版本。
- 5 Scene 順序一致。

## Visual

- 五幕皆為動畫。
- START／END 各自為單張 9:16。
- 無拼貼、文字、Logo、UI、Dashboard。
- 年代、人物、服裝、建築與物件合理。
- 五幕構圖、距離、色溫與鏡頭路徑有差異。

## Voice

- Edge TTS 指定聲線。
- 全篇一次生成。
- 無機械音替代。
- Voice-first Timing 正確。

## Audio

- Voice 清楚。
- BGM 不壓旁白。
- Ambience、轉場與 Emotional Curve 存在。
- 片尾聲音自然收束。

## Delivery

- MASTER_PREVIEW。
- 無字幕 Master。
- Scene 01～05 動態片段。
- Voice、字幕、音樂、SFX。
- Production State、Asset Index、QC Log、Manifest、SHA256。
- 歸檔狀態可驗證。

---

# 14. 永久禁止

1. 在主製片長 Chat 直接生成正式 Frame。
2. 把完整 Master Markdown 或 Storyboard 送進生圖器。
3. 一次生成 START 與 END。
4. 一次生成多個 Scene 或多格版面。
5. 將 Dashboard、流程、Gate、表格或品牌角色帶入 Renderer Prompt。
6. 用靜態圖、Image V6 或 Ken Burns 代替正式動態 Scene。
7. 五幕使用完全相同鏡頭與構圖。
8. 未核准就消耗外部生成點數。
9. 工具失敗後重做已 PASS 資產。
10. 用機械音或臨時低品質片尾冒充正式資產。
11. 未實際保存就宣稱已歸檔。
12. 在狀態完整時輸出冗長啟動稽核而不執行 NEXT_ACTION。

---

# 15. 日常標準行為

## 新 Episode

使用者輸入：

```text
[歷史上的今天]
```

系統進入 Topic Candidate Gate。

## 接續 Episode

使用者輸入：

```text
[繼續歷史上的今天]
```

系統讀取短狀態檔，回報一行 RESUME，然後直接執行 NEXT_ACTION。

## 生圖

Master Chat 只輸出純 Renderer Prompt；正式圖在同一專案的新 Clean Renderer Chat 生成。

每張完成後：

```text
QC
→ REGISTER
→ UPDATE SHORT STATE
→ NEXT FRAME OR VIDEO PROMPT
```

---

# 16. 版本治理

- 本 V2.5 取代 V2.4 作為 CURRENT。
- V2.4 移至 `SUPERSEDED`，不得再作為新 Episode 啟動依據。
- 歷史事故、測試紀錄與舊技術分支移至 Archive，不留在 CURRENT 主控文件。
- 後續只在現行規則確實改變時升版，不以聊天補丁方式無限疊加。

## V2.5 主要修正

1. 移除額外品牌角色的所有內容與引用；相關角色影片改由獨立後製接入。
2. 移除靜態影片、Image V6 與 Ken Burns 正式分支。
3. 明定五幕全部使用 Flow、Meta、Canva 或混合模式生成動畫。
4. 新增 `ONE FRAME = ONE CLEAN RENDERER CHAT = ONE IMAGE GENERATION INVOCATION`。
5. 明定主製片長 Chat 禁止直接生成正式 Frame。
6. 新增 Active Production State 短檔，避免新 Chat 只做稽核、不執行。
7. 移除重複事故附錄、舊 Commit、失效技術路徑與互相矛盾的自動化宣稱。
8. 將自動保存改為依 Runner 實際連線狀態誠實判定。

---

**END OF FILE — HISTORY_TODAY_MASTER_DATABASE_V2.5**
