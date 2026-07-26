# Tool Handoff Specification V2.0｜草案

**狀態：DRAFT／NOT LOCKED。所有交接均為人工／檔案化交接；不假設工具間自動控制。**

| 交接 | 輸入 | 輸出 | 責任人 | 失敗條件／Gate |
|---|---|---|---|---|
| ChatGPT → Work | scope、VERIFIED evidence、已核准決策 | Brief／Story／Gate-ready package | Mata老師＋人工審閱 | 缺核准、scope 混淆、Evidence 非 VERIFIED 即停止 |
| Work → Codex | 已發布規格、Backlog、驗收案例 | 實作提案／唯讀驗證結果 | 未來獲授權的 Codex | Publication Gate、Lock 或實作授權未完成即不得啟動 |
| ChatGPT／Gemini → Flow | approved storyboard、keyframe、prompt manifest、Exact placements | 人工可貼入的 Flow manifest | 使用者 | 無 `keyframe_lock` PASS、Rejected reference、Exact 重繪要求即阻塞 |
| Flow → CapCut | 已登錄 Flow media、audio、edit manifest | 人工剪輯候選與 QC 資料 | 使用者 | 無 Drive File ID／checksum、dependency 未通過即阻塞 |
| GitHub ↔ Drive Metadata | Asset ID、version、folder/file ID、checksum、evidence | 同步可稽核 Index／Register metadata | 人工責任人 | ID 缺失、checksum/版本衝突即 `CONFLICTED`，不覆寫任一端 |

每個 handoff manifest 必填：`handoff_id`、from/to、scope、input refs、output refs、owner、version refs、evidence status、dependency status、approval/Gate、timestamp、failure action。人工 Gate 是六 Gate 的唯一核准點；ChatGPT、Gemini、Codex 不可自行宣稱通過。無額外付費 API 為預設；Codex 不直接控制 Flow 或 CapCut。
