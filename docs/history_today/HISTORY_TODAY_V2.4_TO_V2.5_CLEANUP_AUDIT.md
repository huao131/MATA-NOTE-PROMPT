# 《歷史上的今天》V2.4 → V2.5 清理稽核

## 結論

V2.5 採「乾淨替代」而非增量附錄。V2.4 中不符現況、重複或容易污染 Renderer 的內容已移除或改寫。

## 已移除

- 額外品牌角色與其解剖、動作、後製規則。
- 將品牌角色資料庫列入每次啟動必讀的做法。
- V6 Camera Motion 作為正式 Scene 生成路徑。
- Image V6、靜態第一版、Ken Burns 正式影片分支。
- 「第一版完成後才選配 Flow」等與全動態決策衝突的規則。
- 舊事故紀錄、重複修正附錄與重複版本紀錄。
- 固定舊 Branch／Commit 作為永久真相的內容。
- 未連線卻宣稱可自動呼叫外部工具或自動寫入 OneDrive 的內容。
- 新 Chat 必須先輸出大量稽核清單的做法。

## 已改正

- 五幕全部為動畫影片。
- 影片工具允許 Flow、Meta、Canva 或混合模式。
- 主製片長 Chat 不直接生成正式 Frame。
- 正式 Frame 使用同一專案中的 Clean Renderer Chat。
- `ONE FRAME = ONE CLEAN RENDERER CHAT = ONE IMAGE GENERATION INVOCATION`。
- START 與 END 分開生成、分開 QC、分開保存。
- START／END 都 PASS 後，才建立動態影片提示詞。
- 新增短狀態檔 `HISTORY_TODAY_ACTIVE_PRODUCTION_STATE_CURRENT.md`，讓 `[繼續歷史上的今天]` 直接執行 NEXT_ACTION。
- 自動保存改為依 Runner／檔案系統是否實際連線判定。

## 保留

- Topic、Story Direction、Hook、Narration、Storyboard、Production Input Lock 的內容 Gate。
- Voice-first。
- Edge TTS 指定聲線。
- 雙語字幕、三層聲音與固定片尾。
- OneDrive 正式歸檔、Asset Index、Production State、QC、SHA256。
- 已 PASS／APPROVED／LOCKED 不重做。

## 今日單張生圖驗證

A 測試結果：同一專案中的新 Chat，使用純單張 Prompt，可正確生成單張 9:16 歷史電影畫面。

因此根因判定為：

```text
MASTER_MARKDOWN_CAUSE = NO
PROJECT_INSTRUCTION_CAUSE = NO
LONG_MASTER_CHAT_CONTEXT_CONTAMINATION = YES
```

正式方法：

```text
Master Chat 決定 NEXT_ACTION
→ 建立純 Renderer Prompt
→ 同一專案新 Clean Renderer Chat
→ 一次生成一張
→ 回 Master Chat QC／登錄／接續
```
