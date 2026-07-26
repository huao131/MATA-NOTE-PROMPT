# Production State and Gate Model V2.1｜第二批草案

**狀態：DRAFT／NOT LOCKED**  
**基準 Commit：`4e1182f3de4aa4ef63cccc642b6b150e3d3bd3bf`（Local Review Baseline）**  
**本文件不授權 SYSTEM SPECIFICATION LOCK、Codex Implementation、Legacy Migration、Flow 操作或正式資產變更。**

## 1. 目的、適用範圍與責任邊界

本模型定義 GitHub 中 Episode／Segment／Asset 的可追溯 Production State 與 Gate Register。它完整採用第一批的 Evidence、Lifecycle 與 Dependency 規則：

- `evidence_status` 僅可為 `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`；只有 `VERIFIED` 證據可寫入 Canonical Production State。
- `lifecycle_status` 僅可為 `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED`；不得以 `QC_PENDING` 或工作流程詞彙取代。
- GitHub 保存本 State、Gate、Version／Lock Register、Approval、規格、Asset Index 與證據紀錄；Google Drive 只保存圖片、影片、音訊、字幕、剪輯包等大型實體資產。Drive File ID 與 Metadata 必須回寫 GitHub Asset Index。
- Drive 名稱與路徑不是主鍵；任何 Drive 參照必須使用 `07_FOLDER_REGISTRY_V2.1_DRAFT.md` 登錄的 `google_drive_folder_id` 與 Asset Index 的 `google_drive_file_id`。

本文件不自行宣告 EP01、EP02、A2_V1.1、B1_V2.0、S1 Flow Package 或 `REVISION_REQUIRED` 的 Canonical 狀態；其第一批 Evidence 均未達可寫入門檻。

## 2. Canonical Production State 最小 Schema

每一筆 Episode、Segment 或 Asset State 必須具備以下欄位。值未知時保持空值或 `NOT_EVALUATED`，不可由聊天、檔名、資料夾名稱或推論補值。

| 欄位 | 定義與規則 |
|---|---|
| `scope_type`／`scope_id` | `EPISODE`、`SEGMENT` 或 `ASSET`，及其不可變識別碼。 |
| `current_phase` | 當前流程位置；只可為 `INTAKE`、`CREATIVE`、`STORY`、`STORY_VISUAL`、`KEYFRAME`、`PRODUCTION`、`FINAL_QC`、`CLOSED`。非狀態、非證據。 |
| `health_status` | `HEALTHY`、`AT_RISK`、`BLOCKED`、`NOT_EVALUATED`；反映可繼續性，不可取代 Gate 或 Evidence。 |
| `episode_status` | 僅適用 Episode：`NOT_STARTED`、`IN_PROGRESS`、`REVISION_REQUIRED`、`READY`、`APPROVED`、`CLOSED`、`NOT_EVALUATED`。`READY` 必須為 Episode 層所有必要 Gate 與依賴皆通過的結果。 |
| `segment_status` | 僅適用 Segment：`NOT_STARTED`、`IN_PROGRESS`、`REVISION_REQUIRED`、`READY`、`APPROVED`、`NOT_EVALUATED`。不得回寫或自動推升 `episode_status`。 |
| `asset_status` | 僅適用 Asset：採用 `lifecycle_status` 允許值；品質以獨立 `qc_status` 表達。`REJECTED` 不可成為任何下游依賴。 |
| `gate_register` | 依第 3 節的逐 Gate 紀錄；不得只存布林值。 |
| `dependency_status` | `NOT_EVALUATED`、`PASS`、`FAIL`、`DEPENDENCY_RECHECK_REQUIRED`、`BLOCKED_BY_UPSTREAM`。 |
| `next_action` | 一項可執行、可驗證的下一步；不得填入「繼續製作」等無法稽核的文字。 |
| `blocked_reason` | `health_status=BLOCKED`、Gate `BLOCKED`／`FAIL`，或依賴未通過時必填；否則為空。 |
| `evidence_source` | 可解析的 Git Commit SHA、repo path、Drive File ID／Folder ID、核准紀錄或人工核對紀錄；並須對應 `evidence_status`。 |
| `evidence_status` | 第一批唯一允許的四值；非 `VERIFIED` 不得形成 Canonical Production State 的事實主張。 |
| `updated_at`／`updated_by` | ISO 8601 時間與責任人，供稽核使用。 |

## 3. Gate Register

Gate 順序為 `creative_lock` → `story_lock` → `story_visual_lock` → `keyframe_lock` → `production_lock` → `final_approved`。後續 Gate 不得在前置 Gate 未通過、依賴未通過或證據未達 `VERIFIED` 時標示為 `PASS`。

| gate_id | 通過條件 | 必要上游／禁止事項 |
|---|---|---|
| `creative_lock` | Creative Brief、目標、受眾、輸出語意與核准版本已可解析且證據為 `VERIFIED`。 | 不可由未驗證聊天摘要建立。 |
| `story_lock` | Story Treatment、Script／Narration、角色與情節決策已核准；變更原因與版本已登錄。 | `creative_lock=PASS`；故事修改不得覆寫既有 Lock。 |
| `story_visual_lock` | Storyboard、Visual Bible、Character／Scene／Prop／Exact Asset 參照與鏡頭依賴已核對。 | `story_lock=PASS`；Exact Asset 不得由生成式 AI 重繪或替代。 |
| `keyframe_lock` | 關鍵影格、角色／場景／道具連續性、Prompt Check 與必要的參考資產均已核准。 | `story_visual_lock=PASS`；`REJECTED` 不得作為 Reference。 |
| `production_lock` | 影片生成與剪輯所用資產已核准或鎖定，Flow／下游輸出依賴檢查為 `PASS`。 | `keyframe_lock=PASS`；`DEPENDENCY_RECHECK_REQUIRED` 未結案時禁止通過。 |
| `final_approved` | Final QC、Final Asset List、交付語意與核准記錄均為已驗證證據。 | `production_lock=PASS`；Segment Ready 本身不是本 Gate 的依據。 |

每一個 Gate Register entry 必須保存下列欄位：

| 欄位 | 規則 |
|---|---|
| `gate_id` | 僅限上述六個固定 Gate 名稱。 |
| `gate_status` | `NOT_STARTED`、`PENDING`、`PASS`、`FAIL`、`BLOCKED`、`SUPERSEDED`。 |
| `approved_version` | 通過時必填，且必須對應 Version／Lock Register 的唯一版本；未通過不得假填。 |
| `approved_by` | 通過時必填之核准者；未核准時為空。 |
| `approved_at` | 通過時必填 ISO 8601 時間；未核准時為空。 |
| `basis_documents` | GitHub repo path 與可解析 Commit SHA；Drive 資產另加 File ID。 |
| `evidence_status` | 四值之一；`INFERRED`、`UNVERIFIED`、`CONFLICTED` 時 `gate_status` 不得為 `PASS`。 |
| `superseded_by_new_version` | 布林值；為真時 `superseding_version_ref` 必填，舊 Gate 改為 `SUPERSEDED`，不可回寫原受保護檔。 |
| `dependency_recheck_result` | `NOT_REQUIRED`、`PASS`、`FAIL`、`PENDING`、`DEPENDENCY_RECHECK_REQUIRED`；觸發重查時必填 affected 範圍與責任人。 |
| `blocked_reason` | Gate 為 `FAIL`／`BLOCKED` 或重查未通過時必填。 |

## 4. Dependency 與 Ready 隔離規則

1. 任何上游 Story、Visual、Keyframe、Exact Asset、權利、角色連續性或交付語意的新版取代，必須先在 Version／Lock Register 登錄 `change_reason`、`affected_scope`、`upstream_impact`、`downstream_impact`，再將所有受影響下游標為 `DEPENDENCY_RECHECK_REQUIRED`。
2. 重查紀錄至少包含 `affected_assets`、`affected_segments`、`affected_outputs`、`recheck_owner`、`recheck_result` 與證據來源。結果不是 `PASS` 時，受影響 Gate 不得 `PASS`。
3. `segment_status=READY` 僅代表該 Segment 自身的已驗證範圍通過；它不得自動改變 `episode_status`、不得使 `final_approved=PASS`，也不得略過其他 Segment、Episode 全域依賴、Final QC 或交付檢查。
4. Episode `READY` 僅可由 Episode 層的已驗證 Gate Register、全 Segment 要求、所有上游／下游 Dependency Check 和未解除 Blocker 共同判定；此為人工可稽核的匯總，不是自動推導。
5. `REJECTED` 資產只能留作 Rejected／Archive 的歷史或教學紀錄，禁止進入 Character、Scene、Prop、Flow Reference、Generation Dependency 或 Final Asset List。

## 5. State 範例（Schema 示意，非 EP01／EP02 事實）

```yaml
scope_type: EPISODE
scope_id: EXAMPLE_EPISODE_ONLY
current_phase: STORY
health_status: BLOCKED
episode_status: NOT_EVALUATED
segment_status: null
asset_status: null
dependency_status: DEPENDENCY_RECHECK_REQUIRED
next_action: "完成已列明之上游版本影響範圍與人工 Dependency Recheck。"
blocked_reason: "上游 Story 資產已由新版本取代，尚無 VERIFIED recheck evidence。"
evidence_source:
  - "Git commit: <resolvable-sha>"
evidence_status: UNVERIFIED
gate_register:
  - gate_id: story_lock
    gate_status: BLOCKED
    approved_version: null
    approved_by: null
    approved_at: null
    basis_documents: ["<repo-path>@<resolvable-sha>"]
    evidence_status: UNVERIFIED
    superseded_by_new_version: false
    dependency_recheck_result: DEPENDENCY_RECHECK_REQUIRED
    blocked_reason: "Recheck evidence pending."
```

## 6. 停止條件

遇到不可解析 Commit SHA、未登錄 Drive ID、Evidence 非 `VERIFIED`、受保護檔需改寫、Gate 或 Dependency 未通過時，停止狀態推進並 `STOP_AND_REPORT`。本 Draft 完成不等於 SYSTEM SPECIFICATION LOCK；Repository Publication Gate 的 remote、同步、可解析性與 non-force-push 條件另行處理。
