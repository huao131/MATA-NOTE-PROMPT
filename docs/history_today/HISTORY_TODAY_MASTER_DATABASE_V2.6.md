# 《歷史上的今天》AI 自動化主控資料庫 V2.6

**文件代號：** `HISTORY_TODAY_MASTER_DATABASE_V2.6`  
**狀態：** `CURRENT_EFFECTIVE / READ_FIRST / SINGLE_SOURCE_OF_TRUTH`  
**適用時區：** `Asia/Taipei`  
**定位：** 指定日期、單一 Episode、從研究到剪輯交付與歸檔的完整 No-Loss 製片規格。  

> 本版完整取代 V2.5 作為 CURRENT，不是附錄。日常只使用一種通關密語。

---

# 1. 唯一通關密語

唯一合法格式：

```text
[歷史上的今天 YYYY-MM-DD]
```

範例：

```text
[歷史上的今天 2026-08-04]
```

不得建立其他日常通關密語。

指定日期是唯一 Episode 定位鍵：

1. 該日期不存在 Episode：建立新 Episode，從史實研究與選題開始。
2. 該日期已有未完成 Episode：讀取該日 Production State、Asset Index、QC，從第一個未完成步驟接續。
3. 該日期已完成：回報正式成片與歸檔位置，不得重做。
4. 不得猜測最近 Episode。
5. 不得繼承其他日期的主題、人物、Scene Prompt、圖片、影片或狀態。

首次只回報：

```text
EPISODE_DATE =
EPISODE_STATUS = NEW / RESUME / COMPLETE
CURRENT_STAGE =
NEXT_ACTION =
```

---

# 2. 完整 No-Loss 狀態機

```text
DATE_VERIFICATION
→ HISTORICAL_RESEARCH
→ TOPIC_CANDIDATES
→ MATA_TOPIC_APPROVAL
→ STORY_DIRECTION
→ HOOK
→ VOICE_SCRIPT
→ FIVE_SCENE_STORYBOARD
→ VIDEO_TOOL_MODE
→ PRODUCTION_INPUT_LOCK
→ START_AND_END_FRAMES
→ FLOW_META_CANVA_VIDEO_PROMPTS
→ FIVE_ANIMATED_CLIPS
→ VOICE_GENERATION
→ VOICE_FIRST_TIMING
→ ZH_TW_AND_EN_SUBTITLES
→ MUSIC_SFX_AMBIENCE
→ FIXED_ENDING
→ EDIT_TIMELINE_AND_MASTER
→ EDITOR_IMPORT_OR_UPLOAD
→ FINAL_QC
→ MANIFEST_SHA256_ARCHIVE
```

內容 Gate 尚未核准前不得跳到正式視覺生成。Topic、故事方向、Hook、旁白、5 Scene Storyboard 與 Video Tool Mode 全部核准並建立 Production Input Lock 後，不得再次詢問是否繼續。

狀態只允許：

```text
PENDING / AWAITING_MATA / APPROVED / PASS / LOCKED / BLOCKED / FAIL / NOT_REQUESTED
```

---

# 3. 研究、選題與內容鎖定

## 3.1 研究與候選

每個日期至少提供：

- 人物候選 3 個。
- 事件候選 3 個。

每項包含：日期與史實、可靠來源、故事角度、前三秒 Hook、視覺潛力、情緒曲線、適合度、敏感或史實風險。

候選只代表推薦，不代表核准。

## 3.2 旁白

- 繁體中文。
- 單一主題。
- 先故事、後畫面。
- 避免百科流水帳、虛構引語與未查證細節。
- 原則 50～90 秒。
- Mata 核准後鎖定，不得自行改寫。

## 3.3 5 Scene Storyboard

每幕必須包含：

- Scene 名稱與對應旁白。
- Start State、End State、Visible Change。
- 人物、年代、服裝、場景與道具。
- 鏡頭運動。
- 人物、物件、環境動態。
- 光線、色調、情緒。
- 下一幕銜接。
- Video Tool。
- START Prompt、END Prompt、Negative Prompt。
- 中文 Headline、繁中精簡字幕、英文小字幕。

Storyboard 只使用 Markdown／JSON／YAML；不得生成總覽圖作為 Renderer 輸入。

## 3.4 Production Input Lock

必填：

```yaml
episode_date:
episode_id:
topic_title:
historical_date:
research_sources:
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

鎖定狀態：

```text
PRODUCTION_INPUT_LOCK = LOCKED
AUTO_CONTINUE = TRUE
NO_ADDITIONAL_CONFIRMATION_REQUIRED = TRUE
```

---

# 4. 單張首尾幀 Golden Path

正式規則：

```text
ONE FRAME
= ONE CLEAN RENDERER CONTEXT
= ONE IMAGE GENERATION INVOCATION
= ONE OUTPUT IMAGE
```

每個 Scene 固定順序：

```text
START FRAME
→ AI QC
→ SAVE / REGISTER
→ END FRAME
→ CONTINUITY QC
→ SAVE / REGISTER
→ FLOW / META / CANVA MOTION PROMPT
→ ANIMATED CLIP
→ NEXT SCENE
```

Renderer 只能收到：

- 當前 Episode。
- 當前 Scene。
- START 或 END。
- 單張純畫面描述。
- 直式 9:16。
- 當前畫面的 Negative Prompt。

Renderer 禁止收到：

- Master Database 全文。
- Production State 表格。
- 完整 Storyboard。
- 其他 Scene。
- START 與 END 同時。
- 完整旁白。
- 工作流程、Gate、Dashboard。
- 字幕、Logo、品牌角色或片尾規則。

輸出要求：單一滿版 9:16、無文字、無字幕、無 Logo、無 UI、無表格、無拼貼、無多格、無 Storyboard Grid。

檔名：

```text
YYYYMMDD_SCENE_XX_START_V1.png
YYYYMMDD_SCENE_XX_END_V1.png
```

每張最多重試 3 次；重試仍必須是單張、乾淨 Renderer Context。

---

# 5. 五幕全動畫

五個 Scene 全部必須是動畫影片，不得使用靜態圖或 Ken Burns 作正式 Scene。

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

禁止：

```text
STATIC_FIRST_DRAFT
IMAGE_V6_VIDEO
KEN_BURNS_AS_FINAL_SCENE
SINGLE_IMAGE_AS_FINAL_CLIP
```

每幕必須保存：

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

正式動態提示詞只能在 START 與 END 都 PASS 後建立，並描述從 START 到 END 的鏡頭路徑、人物動作、物件動作、環境動態、光線變化、物理限制與歷史一致性。

工具失敗只重試該 Scene；可切換 Flow、Meta 或 Canva，但不得改變已核准旁白、Story State 或首尾幀。

---

# 6. Voice-first、字幕與聲音

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
VOICE_SCRIPT_LOCKED
→ GENERATE_FULL_VOICE
→ VOICE_CHECKPOINT
→ READ_ACTUAL_DURATION
→ RETIME_5_SCENES
→ SUBTITLE_TIMECODES
→ AUDIO_DESIGN
```

必須交付：

- 完整中文旁白音檔。
- 繁體中文字幕 SRT。
- 英文字幕 SRT。
- 中英雙語 ASS 或等效樣式字幕。
- 中文主字幕＋英文小字幕版型。
- 所有字幕時間碼與 Voice-first Timeline 對齊。
- 英文字幕忠於中文語意，不使用生硬逐字直譯。

聲音固定三層：

```text
VOICE + MUSIC + SPACE / AMBIENCE / SFX
```

包含慢速 Tick、約 0.75 秒翻頁／Whoosh、年代與地點 Ambience、Emotional Lift、Ducking、Audio Master。

建議基準：

```text
Target Loudness = -16 LUFS
True Peak Max = -1.5 dBTP
Sample Rate = 48 kHz
Channels = Stereo
```

---

# 7. 版型與固定片尾

- 上方固定系列標示：`歷史上的今天`。
- 暖金細線與日期／事件英文小標。
- 下方薄型深色半透明字幕帶。
- 繁中主字幕＋英文小字幕。
- 左下品牌文字：`AI加速研究院・MATA`。
- 固定片尾使用已核准《時光翻頁｜品牌片尾 V1.0》。
- 片尾為獨立影片資產，僅在後製接入，不得進入歷史 Scene 生圖 Prompt。

---

# 8. 剪輯、匯入與上傳

每集必須建立 `EDITOR_DELIVERY_PACKAGE`：

```text
01_MASTER_PREVIEW.mp4
02_MASTER_NO_SUBTITLE.mp4
03_SCENE_01_TO_05_CLIPS/
04_VOICE/
05_SUBTITLES_ZH_TW_EN/
06_BGM_SFX_AMBIENCE/
07_FIXED_ENDING/
08_COVER/
09_TIMELINE.csv
10_EDIT_GUIDE.md
11_ASSET_INDEX.json
12_MANIFEST.json
13_SHA256SUMS.txt
```

剪輯軟體規則：

1. 剪映／CapCut、Canva 或指定剪輯工具已連接且支援寫入時，Runner 直接建立或上傳素材與時間軸，並驗證實際結果。
2. 無法直接建立原生工程檔時，交付完整可匯入資料夾、Timeline、字幕與 Edit Guide，不得宣稱已上傳。
3. 所有 Scene、Voice、字幕、音訊、片尾與封面必須使用穩定檔名；匯入後不需人工猜測順序。
4. `EDITOR_IMPORT_QC = PASS` 後才可標記剪輯交付完成。

---

# 9. 保存與歸檔

正式根目錄：

```text
C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\
```

每集至少包含：控制與狀態、研究與來源、腳本與分鏡、START、END、未採用、Flow／Meta／Canva 提示詞、動畫片段、配音、字幕、音樂音效、半成品、成品、QC Log、剪輯交付包、封存。

Runner 已連接時，QC PASS 後保存並更新 Asset Index、Production State、Manifest 與 SHA256。Runner 未連接時必須標記暫存路徑與待匯入狀態，不得宣稱已寫入 OneDrive。

Rejected 資產移入未採用；修正不得覆寫同版本，必須升版。

---

# 10. No-Loss 完成 Gate

只有以下全部存在並可驗證，Episode 才能標記 `DELIVERY_COMPLETE`：

```text
RESEARCH_COMPLETE
CONTENT_LOCKED
10_FRAMES_PASS
5_ANIMATED_CLIPS_PASS
VOICE_PASS
ZH_TW_SUBTITLE_PASS
EN_SUBTITLE_PASS
BILINGUAL_SUBTITLE_PASS
AUDIO_PASS
ENDING_PASS
MASTER_PREVIEW_PASS
EDITOR_DELIVERY_PACKAGE_PASS
EDITOR_IMPORT_QC_PASS_OR_IMPORT_READY_PASS
MANIFEST_AND_SHA256_PASS
ARCHIVE_PASS
```

任一項缺失時，必須標記具體 BLOCKED 項目，不得以「流程已完成」取代實際資產。

---

# 11. 永久禁止

1. 使用未指定日期的模糊通關密語。
2. 猜測最近 Episode。
3. 跨日期污染。
4. 未核准內容就生成正式視覺。
5. 一次生成多個 Frame、START 與 END 或多 Scene。
6. 將流程、表格、Dashboard、字幕或 Logo 帶入 Renderer。
7. 用靜態影片代替五幕動畫。
8. 漏掉繁中、英文或雙語字幕任一版本。
9. 漏掉 Voice-first Timing、三層聲音、片尾或音訊 Master。
10. 未實際保存、上傳或匯入就宣稱完成。
11. 漏掉 Timeline、Edit Guide、Asset Index、Manifest 或 SHA256。
12. 工具失敗後重做已 PASS 資產。

---

# 12. 版本治理

- V2.6 取代 V2.5 作為 CURRENT。
- V2.5 保留歷史，不再作為啟動依據。
- 後續只有現行規則真正改變時才升版，不以聊天補丁無限疊加。

**END OF FILE — HISTORY_TODAY_MASTER_DATABASE_V2.6**