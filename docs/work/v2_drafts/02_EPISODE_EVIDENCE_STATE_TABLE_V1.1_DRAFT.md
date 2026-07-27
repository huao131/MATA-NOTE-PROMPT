# EPISODE EVIDENCE STATE TABLE V1.1｜草案

**狀態：DRAFT／NOT LOCKED**  
**無效基準：`fd5d011a980251514ff405973c36158556bdf9c9` 是 `INVALID_BASELINE`。**

`evidence_status` 唯一允許值：`VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`。此欄位不混用 workflow 或 reconciliation 值；`INFERRED` 與 `UNVERIFIED` 不得寫入 Canonical Production State。

| 對象 | evidence_status | verification_workflow_status | reconciliation_status | 可寫入 Canonical Production State？ | 必要完成項 |
|---|---|---|---|---:|---|
| EP01 | `UNVERIFIED` | `NOT_STARTED` | `NOT_REQUIRED` | 否 | 正式來源 SHA、Drive File ID、人工核對、Dependency Check。 |
| EP02 | `UNVERIFIED` | `NOT_STARTED` | `NOT_REQUIRED` | 否 | 正式來源 SHA、Drive File ID、人工核對、Dependency Check。 |
| A2_V1.1 | `INFERRED` | `PENDING_SOURCE_VERIFICATION` | `PENDING` | 否 | 完整來源與比對後才可重新判定。 |
| B1_V2.0 | `UNVERIFIED` | `NOT_STARTED` | `NOT_REQUIRED` | 否 | 來源、歸屬與 Dependency Check。 |
| S1 Flow Package | `INFERRED` | `PENDING_SOURCE_VERIFICATION` | `PENDING` | 否 | Package、Drive File ID、人工核對與依賴結果。 |
| REVISION_REQUIRED | `UNVERIFIED` | `NOT_STARTED` | `NOT_REQUIRED` | 否 | 可解析正式來源與狀態定義。 |

證據完成前，任何 Episode 或 Asset 的 Canonical Production State 一律留白；不可用旁證、聊天紀錄或檔名推定。Folder 定位僅引用 `07_FOLDER_REGISTRY_V2.1_DRAFT.md` 的七筆正式 Registry。
