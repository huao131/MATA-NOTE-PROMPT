# Version and Lock Register V2.1｜第二批草案

**狀態：DRAFT／NOT LOCKED**  
**基準 Commit：`4e1182f3de4aa4ef63cccc642b6b150e3d3bd3bf`（Local Review Baseline）**  
**本文件不授權 SYSTEM SPECIFICATION LOCK、Codex Implementation、Legacy Migration、Flow 操作或正式資產變更。**

## 1. 不可覆寫原則

`LOCK`、`FINAL`、`MASTER`、`APPROVED` 標記的文件、媒體或 Exact Asset 原檔皆為受保護歷史證據：

1. 不得覆寫內容、不得原地更新、不得改名、不得移動以假造新版本、不得回寫 `SUPERSEDED`。
2. 任何內容變更都必須建立新檔案與新版本；若資產身分、語意或權利範圍改變，建立新 `asset_id`。
3. 相同 `scope_id + artifact_id + version` 組合不得重複；登錄前必須查 Register，若已存在即 `STOP_AND_REPORT`。
4. 舊檔維持原始檔名、原始位置與原始生命週期。它是否已被取代，只能寫入外部 Version／Lock Register 的關聯欄位，不得回寫到舊檔。
5. GitHub 保存 Register、版本、Approval、Lock、State、Evidence 與 Asset Index；Google Drive 保存大型實體檔。實體檔的 Drive File ID、checksum 與 Metadata 必須回寫 GitHub Asset Index／Register。Drive 名稱不是主鍵。

## 2. Register 的唯一位置與最小 Schema

Version／Lock Register 是 GitHub 的受控治理資料；Production Database Drive 根目錄只能保存其大型證據資產或資料交接，不取代可版本化 Register。Register 的每筆 Record 至少包含：

| 欄位 | 要求 |
|---|---|
| `register_id` | 不可變唯一 ID。 |
| `scope_type`／`scope_id` | `GLOBAL`、`SERIES`、`EPISODE`、`SEGMENT`、`ASSET` 及對應 ID。 |
| `artifact_id`／`artifact_type` | 被控管文件或資產的不可變身分與類型。 |
| `version` | 唯一版本，例如 `v2.1`；不可重複。重大故事、鏡頭、權利、角色連續性、交付語意變更升 MAJOR；其他修正升 MINOR。 |
| `lifecycle_status` | 只允許 `DRAFT`、`REVIEW`、`APPROVED`、`LOCKED`、`SUPERSEDED`、`ARCHIVED`、`REJECTED`。QC 另用 `qc_status`。 |
| `protected_designation` | `NONE`、`LOCK`、`FINAL`、`MASTER`、`APPROVED`；可多值記錄時須保留原有標記。 |
| `repo_path`／`commit_sha` | GitHub 正式來源的路徑與可解析 Commit SHA；未發布的本機紀錄須明標 `publication_status=LOCAL_ONLY`。 |
| `google_drive_file_id`／`checksum` | 有實體媒體時必填；GitHub 內純文件可為空。 |
| `evidence_status`／`evidence_source` | 僅用第一批四值及可解析來源；非 `VERIFIED` 不得當作 Canonical 事實。 |
| `change_reason` | 新版本必填，描述為何建立新檔／版本。 |
| `affected_scope` | 新版本必填，列出 Global／Series／Episode／Segment／Asset 的影響範圍。 |
| `upstream_impact`／`downstream_impact` | 新版本必填；無影響時明載 `NONE_VERIFIED`，不可省略。 |
| `supersedes_register_id` | 新版取代舊版時必填；舊版不改檔，由其外部 Register Record 標示 `superseded_by_register_id`。 |
| `dependency_recheck_status` | `NOT_REQUIRED`、`PENDING`、`PASS`、`FAIL`、`DEPENDENCY_RECHECK_REQUIRED`。 |
| `approval_ref`／`lock_ref` | 連至 Gate Register 或正式核准／Lock 證據。 |
| `created_at`／`created_by` | ISO 8601 時間與建立者。 |

## 3. 新版建立與取代流程

1. **先查唯一性與保護標記**：查 `scope_id + artifact_id + version`、原檔保護標記、可解析 Git Commit 與 Drive ID；無法確認即停止。
2. **建立新檔**：採新檔名與新版本；不得覆寫、改名或搬動既有 `LOCK`／`FINAL`／`MASTER`／`APPROVED` 原檔。
3. **建立新版 Register Record**：在同一變更組登錄 `change_reason`、`affected_scope`、`upstream_impact`、`downstream_impact`、來源、Evidence 與預期關聯。
4. **在 Register 建立外部 Supersession 關係**：新版填 `supersedes_register_id`；舊版的外部 Register Record 填 `superseded_by_register_id` 與 `superseded_at`。這是 Register 的新增紀錄／關聯，不是改寫舊檔或其 metadata。
5. **觸發重查**：只要上游被新版取代，立即對所有受影響下游設 `dependency_recheck_status=DEPENDENCY_RECHECK_REQUIRED`，並在 Production State 的 `dependency_status` 同步反映。記錄 `affected_assets`、`affected_segments`、`affected_outputs`、`recheck_owner`、`recheck_result`。
6. **重新核准**：Dependency Recheck 結果為 `PASS` 前，受影響 Gate 不得 `PASS`；必要時建立新的 Gate Register entry。任何舊核准不得被假設延續到新版本。

## 4. Gate 與 Ready 分離

- Gate 的正式狀態、核准版本、核准者、核准時間、依據文件、Evidence Status、版本取代關係及 Dependency Recheck 結果，均以 `04_PRODUCTION_STATE_AND_GATE_MODEL_V2.1_DRAFT.md` 的 Gate Register 為唯一模型。
- Version／Lock Register 對每筆受控項目提供版本、保護與取代關係；它不自行讓 Gate 通過，也不覆蓋 Evidence 規則。
- `Segment Ready` 只代表該 Segment 的可驗證範圍；不得自動推升 `Episode Ready`、`production_lock` 或 `final_approved`。Episode Ready 需要 Episode 層完整 Gate、全部必要 Dependency Check、Final QC 與已驗證 Evidence。
- `REJECTED` 項目不得成為任何下游依賴或 Final Asset List；它的歷史關聯可存 Register／Archive，但不賦予可使用性。

## 5. Supersession 例外與禁止行為

| 情境 | 正確處置 | 禁止行為 |
|---|---|---|
| 已 Lock 的 Story 要修訂 | 建立新的 Story 檔與新版本，新增 Register Record，標記下游 `DEPENDENCY_RECHECK_REQUIRED`。 | 覆寫或將原 Story 改名為 `SUPERSEDED`。 |
| Approved Keyframe 被新影格取代 | 新增 Keyframe／版本及 checksum、Drive File ID；以 Register 關聯取代關係。 | 修改 Approved 原檔像素、名稱或其內嵌狀態。 |
| FINAL 交付發現錯誤 | 建立新交付版本、重新走 Final QC 與 Gate。 | 直接替換 Final 檔案或沿用舊 final approval。 |
| 同版本號已存在 | 停止並回報，確認版本策略後建立唯一新版本。 | 以相同版本號建立第二份「修正版」。 |
| 上游版本更新 | 登錄四項影響欄位並完成 Recheck。 | 因 Segment 已 Ready 而跳過 Episode 或下游重查。 |

## 6. Local Review 與發布限制

本 Draft 所在 Commit 在尚未完成 GitHub remote 確認、Commit 同步、remote 可解析、正式 GitHub 路徑可重現及 non-force-push 驗證前，只能標示為 `LOCAL_ONLY`。Register 不得將 Local Commit 誤稱 GitHub 已發布來源。

遇到相同版號、來源不可解析、證據非 `VERIFIED`、Drive ID 不符、試圖修改受保護檔，或 Dependency Recheck 未通過時，立即 `STOP_AND_REPORT`。本條件未解除前，不得進入 SYSTEM SPECIFICATION LOCK 或 Codex Implementation。
