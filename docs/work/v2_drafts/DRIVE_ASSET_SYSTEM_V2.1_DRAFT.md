# Drive Asset System V2.1｜草案

**狀態：DRAFT／NOT LOCKED**  
**Folder Registry：唯一引用 `07_FOLDER_REGISTRY_V2.1_DRAFT.md` 的七筆定義；本文件不得自行建立縮減或不同的 Mapping。**

## 儲存責任與分類

GitHub 保存規格、Schema、版本、Approval、Lock、Register、Asset Index、Production State 與證據紀錄。Google Drive 保存圖片、影片、音訊、字幕、剪輯包與其他大型實體資產；每個 Drive File ID 與 Metadata 必須回寫 GitHub Asset Index。

Episode 邏輯資產分類為 `BRIEF`、`STORY`、`VISUAL_BIBLE`、`STORYBOARD`、`KEYFRAME`、`FLOW_MEDIA`、`AUDIO`、`EDIT`、`QC_EVIDENCE`、`FINAL_DELIVERY`、`REJECTED_QUARANTINE`。任何 Episode 子資料夾或檔案未個別驗證前，不得宣稱為 Canonical。

## 命名、版本與狀態

檔名格式：`<SERIES_ID>_<EPISODE_ID>_<SEGMENT_ID-or-GLOBAL>_<ASSET_CLASS>_<ASSET_SLUG>_v<MAJOR>.<MINOR>_<LIFECYCLE_STATUS>.<ext>`；檔名不是主鍵。`lifecycle_status` 僅允許 `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED`，品質進度使用獨立 `qc_status`。

變更故事、鏡頭、權利、角色連續性或交付語意時升 MAJOR；其他修正升 MINOR。Approved／Locked 後修改必須新版本或新 asset ID，原檔不得覆寫。

## Exact Asset、Rejected 與依賴

Exact Asset 必須記錄 Exact Asset ID、核准原檔 Drive File ID、checksum、核准版本、使用位置、是否允許裁切或縮放；禁止生成式 AI 重繪、仿製或替代。

Rejected 資產只可留在 Rejected／Archive 作歷史與教學紀錄，不可進入 Character、Scene、Prop、Flow Reference、下游 Generation Dependency 或 Final Asset List。

上游資產被新版本取代時，強制 `DEPENDENCY_RECHECK_REQUIRED`，並記錄 `affected_assets`、`affected_segments`、`affected_outputs`、`recheck_owner`、`recheck_result`。只有 Approved／Locked 上游且依賴檢查通過的資產可流向下游；Segment 通過不等於 Episode 通過。
