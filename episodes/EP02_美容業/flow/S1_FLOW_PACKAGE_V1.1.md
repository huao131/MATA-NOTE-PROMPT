# EP02｜S1 FLOW PRODUCTION PACKAGE V1.1

**Status:** READY_FOR_GENERATION  
**Episode:** EP02｜美容業｜如果 AI 幫你把客人找回來？  
**Segment:** S1  
**Story Lock:** V1.1 FINAL／LOCKED  
**Visual Masters:** V1.0 LOCKED  
**Aspect Ratio:** 9:16  
**Target Duration:** 10 seconds  

## PRE-FLIGHT

```text
PRE-FLIGHT
Episode: EP02
Runtime State: FLOW_PACKAGE_READY
Story Lock: PASS
Character Master: PASS
Scene Master: PASS
Prop Master: PASS
Exact Asset: PASS
Start Frame A1: PASS
End Frame A2_V1.1: PASS
Next Legal Action: GENERATE_FLOW_S1
```

## 1. Story task

從「日光美學館主理人正在平靜工作」推進到「她看見今日預約大量空缺，開始感到克制而明確的經營壓力」。觀眾不需字幕，也能理解客人變少。

## 2. Input assets

| Role | Asset | Drive File ID | Status |
|---|---|---|---|
| First frame | A1.png | `1VZAg0Uube2FiPKB7d0M7THw3N8vTnt-E` | LOCKED |
| Last frame | A2_V1.1.png | `1yRgyTakLEmN2rz6iCJUIHAhRjJtI6VYL` | LOCKED |
| Character reference | CHARACTER_MASTER_林沐晴.png | `1ZJZlAiTiiQsqd6jnwP4WLjW_G01XJZnb` | LOCKED |
| Scene reference | SCENE_MASTER_日光美學館.png | `1qJxZKC62YY7M6WuUycFBnORIbE1iRS12` | LOCKED |
| Prop reference | PROP_MASTER_日光美學館.png | `1HEKEGLDkajXXk6Jx-aYvyY2MhZO8RB2v` | LOCKED |

## 3. Generation setup

- **Mode:** First frame + last frame / Frames to Video
- **Recommended model:** Flow 內支援首尾影格控制的模型；現有工作流優先使用 OmniNow
- **Target duration:** 10 秒
- **Fallback:** 若 Flow 當下只提供 8 秒，先生成 8 秒；後製延長尾幀停留至 10 秒
- **Camera:** 緩慢推近，帶極輕微側向移動，以自然銜接 A2 V1.1
- **Audio:** 不生成對白；可保留極輕微美容館環境音，正式聲音於後製處理

## 4. Motion timeline

| Time | Motion |
|---:|---|
| 0.0–1.5s | 從 A1 完整廣角開始；林沐晴自然呼吸、眨眼，維持專業平靜。 |
| 1.5–5.5s | 鏡頭緩慢推近；既有黑色螢幕在底座上自然轉向觀眾，不變形、不複製。林沐晴視線移向預約表。 |
| 5.5–8.0s | 林沐晴眉頭輕微收緊、嘴唇微抿，右手自然抬起指向大量空白時段。 |
| 8.0–10.0s | 精準穩定在 A2 V1.1；螢幕呈現大量空白格與兩個金色預約區塊，停留讓觀眾理解。 |

## 5. Continuity locks

- 林沐晴的五官、年齡感、膚色、長深色波浪髮、米色制服與身形比例不變。
- 前台大理石、暖木、產品層架、花材、植栽與 3000K 暖白光不變。
- 只有一台既有黑色工作螢幕；螢幕必須以物理旋轉完成角度變化，不得融化或變形。
- 預約畫面只保留簡潔格線、大量空白與兩個低飽和金色區塊。
- 不生成 Logo、品牌文字、字幕、CTA 或任何可讀介面文字。

## 6. Primary prompt

```text
Create a photorealistic cinematic vertical 9:16 frames-to-video shot using the approved first frame A1 and approved last frame A2_V1.1.

Begin exactly from A1: Lin Muqing stands calmly behind the reception counter in the same Sunlight Aesthetics clinic. Over the shot, use a slow, smooth camera push-in with only a very subtle lateral adjustment. The existing single black work monitor rotates naturally on its physical base toward the audience; it must not morph, melt, duplicate, resize unnaturally, or become a different device.

Lin Muqing first remains professionally calm with natural breathing and one subtle blink. As the monitor becomes visible, her gaze shifts toward the appointment schedule. Her eyebrows gradually knit slightly and her lips gently press together, showing restrained professional concern—not sadness, panic, or shock. She naturally raises one hand and lightly points toward the mostly empty schedule.

The monitor shows a clean generic appointment calendar grid with many empty pale cells and only two small muted-gold appointment blocks. Use simple geometric cells and icons only. No readable words, names, dates, numbers, interface copy, logo, watermark, subtitles, or CTA.

Preserve Lin Muqing's exact identity, facial structure, age, skin tone, long dark wavy hair, beige clinic uniform, anatomy, and proportions. Preserve the same marble reception counter, warm wood materials, product shelves, flowers, plants, and constant 3000K warm white lighting. Keep the background stable and realistic.

End exactly on A2_V1.1 and hold the final composition long enough for the audience to understand that the appointment schedule is mostly empty. No dialogue and no lip-sync.
```

## 7. Negative constraints

```text
No identity drift, face replacement, hairstyle change, clothing change, age change, extra people, duplicated person, extra hands, malformed fingers, floating hand, exaggerated sadness, crying, panic, speaking, lip-sync, sudden camera movement, whip pan, zoom jump, scene change, lighting change, product-shelf movement, flower movement, monitor morphing, duplicate monitor, tablet substitution, phone, paper calendar, random UI animation, readable text, dates, numbers, logo, brand text, subtitles, CTA, watermark, flicker, frame warping, geometry drift, or ending-frame mismatch.
```

## 8. Ending state

- 畫面必須收束到核准的 `A2_V1.1.png`。
- 林沐晴位於右側，螢幕位於左前景。
- 預約格大量空白，只有兩個金色預約區塊。
- 林沐晴的情緒為克制、專業、可辨識的擔憂。
- 尾幀至少保留 1–2 秒的視覺理解時間。

## 9. Flow operation checklist

1. 下載 A1 與 A2 V1.1 原始 PNG。
2. 在 Flow 選擇首尾影格／Frames to Video。
3. A1 設為 First Frame；A2 V1.1 設為 Last Frame。
4. 設定 9:16；優先 10 秒，若只支援 8 秒則採 fallback。
5. 貼入 Primary Prompt。
6. 首次只生成一版，先做人物、螢幕、手部與尾幀一致性 QC。
7. 生成結果下載原始檔並上傳 Drive `07_FLOW_VIDEO`，再進入 `FLOW_QC`。

## 10. QC checklist

- [ ] 人物身分與制服一致
- [ ] 螢幕只有一台且旋轉自然
- [ ] 手指與手掌結構正常
- [ ] 預約稀少可一眼辨識
- [ ] 無可讀文字、Logo、字幕或 CTA
- [ ] 場景與燈光無漂移
- [ ] 結尾準確落在 A2 V1.1
- [ ] 無閃爍、融化、物件複製或跳切

