# WORK SYSTEM AUDIT V1.2｜第一批 P0 修復草案

**狀態：DRAFT／NOT LOCKED**  
**基準：`00_FIRST_BATCH_REMEDIATION_V1.0_DRAFT.md`；`fd5d011a980251514ff405973c36158556bdf9c9` 為 `INVALID_BASELINE`，不得引用。**

## 結論與範圍

本文件只建立第一批重新審閱所需的證據與治理規則；不得進入第二批、SYSTEM SPECIFICATION LOCK、Codex Implementation、Legacy Migration 或 Flow 操作。舊 Draft、Legacy 與 `LOCK`／`FINAL`／`MASTER`／`APPROVED` 原檔均不得回寫。

## 證據規則

`evidence_status` 只允許 `VERIFIED`、`INFERRED`、`UNVERIFIED`、`CONFLICTED`。工作流程另用 `verification_workflow_status`，協調另用 `reconciliation_status`；兩者不可取代證據狀態。`INFERRED` 或 `UNVERIFIED` 絕不得寫入 Canonical Production State。

| 對象 | evidence_status | Canonical Production State | 強制處置 |
|---|---|---|---|
| EP01 | `UNVERIFIED` | 不得寫入 | 等待正式來源 SHA、Drive File ID、人工核對與 Dependency Check。 |
| EP02 | `UNVERIFIED` | 不得寫入 | 同上；現有旁證不得自動升格。 |
| A2_V1.1 | `INFERRED` | 不得寫入 | 僅可作候選證據。 |
| B1_V2.0 | `UNVERIFIED` | 不得寫入 | 不得歸屬任何 Episode。 |
| S1 Flow Package | `INFERRED` | 不得寫入 | 不得推定 Episode Ready。 |
| REVISION_REQUIRED | `UNVERIFIED` | 不得寫入 | 不得作為既有 Canonical State。 |

## 責任邊界與停止規則

- GitHub 保存規格、Schema、版本、Approval、Lock、Register、Asset Index、Production State 與證據紀錄。
- Google Drive 保存圖片、影片、音訊、字幕、剪輯包與其他大型實體資產；Drive File ID 與資產 Metadata 必須回寫 GitHub Asset Index。
- Drive 名稱不是唯一定位；以 Drive ID 為主。Folder Registry 的唯一正式定義為 `07_FOLDER_REGISTRY_V2.1_DRAFT.md`。
- 上游資產被新版本取代時，必須記錄 `DEPENDENCY_RECHECK_REQUIRED`、`affected_assets`、`affected_segments`、`affected_outputs`、`recheck_owner`、`recheck_result`。

## 審閱前提

六份新 Draft 須全部受 Git 追蹤、位於同一個可解析 Local Commit，且提交後工作樹乾淨。未設定 remote 時，此結果只能稱為 Local Commit。
