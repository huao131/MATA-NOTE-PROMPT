# Workflow Schema V2.0｜草案

**狀態：DRAFT／NOT LOCKED；此文件是 Legacy MASTER SOP 的 V2 流程對應，Legacy 僅唯讀基線。**

| Stage | 輸入 | 輸出 | Gate／阻塞 |
|---|---|---|---|
| 0 Intake | 需求、scope、來源證據 | Brief candidate | 缺 scope／權利／Evidence 即 BLOCKED |
| 1 Creative | VERIFIED Brief | Creative package | `creative_lock` PASS |
| 2 Story | Creative package | Story／Narration | `story_lock` PASS |
| 3 Story Visual | Story、Visual Bible、Storyboard、Exact refs | Visual package | `story_visual_lock` PASS；Rejected 禁用 |
| 4 Keyframe | Visual package | approved Keyframes／manifest | `keyframe_lock` PASS |
| 5 Production | Keyframe manifest、人工 Flow 輸出 | registered Flow Media | `production_lock` PASS；不直接控制 Flow |
| 6 Edit/QC | Flow Media、Audio、Edit manifest | QC evidence／delivery candidate | Dependency PASS；不直接控制 CapCut |
| Final | VERIFIED QC、Final Asset List | approved delivery／Register event | `final_approved` PASS |

## Schema 關係與欄位

`GLOBAL → SERIES → EPISODE → SEGMENT → ASSET` 是繼承方向；Global 規則可被 Episode 引用，Episode 設定不得反向升格。`BRIEF → STORY → (VISUAL_BIBLE + STORYBOARD) → KEYFRAME → FLOW_MEDIA → EDIT → QC_EVIDENCE → FINAL_DELIVERY`；`STORY → AUDIO → EDIT` 為平行支線。

每個 workflow record 必填：`workflow_id`、`scope_type`、`scope_id`、`stage`、`input_asset_ids`、`output_asset_ids`、`gate_id`、`gate_status`、`evidence_status`、`dependency_status`、`version_refs`、`owner`、`updated_at`、`blocked_reason`。Asset 同時必須遵守 Asset Index 的 ID、Drive File ID、checksum 與 lifecycle 欄位。

Episode／Segment／Asset 狀態均依 04 定義。Segment Ready 不能推升 Episode Ready；任何上游新版本、缺 Drive ID、Lock 衝突、非 VERIFIED 證據、Rejected reference 或 failed dependency 都使受影響路徑進入 `DEPENDENCY_RECHECK_REQUIRED`／BLOCKED。

Recovery：停止輸出、保全證據、建立新版本或 Register 關聯、標記受影響下游並人工 recheck。禁止覆寫正式資產、刪除 Legacy 或以平行資料夾規避問題。
