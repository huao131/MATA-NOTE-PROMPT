# HISTORY TODAY PROJECT CHAT STARTUP PROTOCOL V1.1

**Status:** `CURRENT_EFFECTIVE`

## 唯一通關密語

唯一合法格式：

```text
[歷史上的今天 YYYY-MM-DD]
```

範例：

```text
[歷史上的今天 2026-08-04]
```

不得建立其他日常通關密語。

## 日期定位與接續

1. 先讀 `HISTORY_TODAY_MASTER_DATABASE_CURRENT.json`。
2. 使用者指定日期是唯一 Episode 定位鍵。
3. 該日期無 Episode：建立新 Episode，從日期查證、研究與選題開始。
4. 該日期有未完成 Episode：讀取該日 Production State、Asset Index、QC，從第一個未完成步驟接續。
5. 該日期已完成：回報正式成片與歸檔位置，不得重做。
6. 不得猜測最近 Episode，不得繼承其他日期的內容或資產。

首次只回報：

```text
EPISODE_DATE =
EPISODE_STATUS = NEW / RESUME / COMPLETE
CURRENT_STAGE =
NEXT_ACTION =
```

## 完整 No-Loss 流程

```text
日期查證
→ 史實研究與來源
→ 人物／事件候選
→ Mata 選題
→ 故事方向
→ Hook
→ 完整繁中旁白
→ 5 Scene Storyboard
→ Video Tool Mode
→ Production Input Lock
→ Scene 01～05 START／END Frames
→ Flow／Meta／Canva 動態提示詞與 Negative Prompt
→ 5 段動畫影片
→ Edge TTS 全篇配音
→ Voice-first Timing
→ 繁中 SRT
→ 英文 SRT
→ 中英雙語 ASS／樣式字幕
→ BGM／SFX／Ambience／Ducking／Audio Master
→ 固定片尾
→ MASTER_PREVIEW 與無字幕 Master
→ Timeline／Edit Guide／Editor Delivery Package
→ 剪映／CapCut／Canva 或指定剪輯軟體匯入／上傳
→ Final QC
→ Asset Index／Manifest／SHA256／Archive
```

不得漏掉研究來源、核准紀錄、10 張首尾幀、5 段動畫、動態提示詞、中英文字幕時間碼、音訊、片尾、Timeline、Edit Guide、Asset Index、Manifest 或 SHA256。

## 正式 Frame 規則

```text
ONE FRAME = ONE CLEAN RENDERER CONTEXT = ONE IMAGE GENERATION INVOCATION = ONE OUTPUT IMAGE
```

Renderer 只能收到當前 Episode、Scene、START 或 END、單張純畫面描述、9:16 與負面限制。不得收到 Master Database、完整 Storyboard、其他 Scene、完整旁白、流程、Gate、表格、Dashboard、字幕、Logo 或片尾規則。

## 外部工具誠實規則

- 工具已連接且可寫入：執行並驗證實際輸出。
- 工具未連接或不支援原生工程檔：交付完整可匯入 Editor Delivery Package。
- 未實際生成、保存、匯入或上傳時，不得宣稱完成。
