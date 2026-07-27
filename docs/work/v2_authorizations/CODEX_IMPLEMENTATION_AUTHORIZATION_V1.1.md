# CODEX IMPLEMENTATION AUTHORIZATION V1.1

**Authorization ID：** `CODEX-AUTH-V1.1-20260727-001`  
**Status：** `AUTHORIZED_WITH_PHASE_GATES`  
**Supersedes：** `CODEX-AUTH-V1.0-20260726-001`（僅P0讀取白名單與治理基準）  
**Repository：** `huao131/MATA-AI-VIDEO-STUDIO`  
**Implementation Branch：** `implementation/v2-p0-foundation`

## 1. 授權基準

Codex必須讀取：

- `docs/work/v2_locks/SYSTEM_SPECIFICATION_LOCK_V2.0_RECORD.md`
- `docs/work/v2_locks/SYSTEM_SPECIFICATION_LOCK_V2.0_ADDENDUM_V1.0.md`
- `docs/work/v2_registers/SYSTEM_SPECIFICATION_LOCK_REGISTER_V2.0.json`
- `docs/work/v2_drafts/20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.2_DRAFT.md`
- Manifest V2.2列出的D01–D12與S01–S02

## 2. 階段授權

- P0：AUTHORIZED
- P1：BLOCKED_PENDING_P0_ACCEPTANCE
- P2：BLOCKED_PENDING_P1_ACCEPTANCE
- P3：BLOCKED_PENDING_P2_ACCEPTANCE

## 3. P0範圍

1. Schema驗證基礎
2. Folder Registry讀取與驗證
3. Asset Index讀寫契約
4. Version／Lock保護
5. Evidence Status驗證
6. Dependency Recheck引擎
7. Repository治理基礎
8. P0單元測試
9. P0驗證報告

S01與S02已獲正式讀取授權，Codex不得再以白名單缺口為由推測契約，也不得擴張其範圍。

## 4. 禁止事項

- 不得修改、覆寫、改名、移動或刪除任何LOCK／FINAL／MASTER／APPROVED文件
- 不得修改main、合併main、force push、rebase或reset --hard
- 不得修改Legacy、媒體、Exact Asset或正式資產
- 不得操作Google Drive、Flow、CapCut
- 不得使用付費API或新增第三方套件，除非另行核准
- 不得進入P1、P2、P3
- 發現新的規格衝突必須STOP_AND_REPORT

## 5. 驗收條件

Codex完成P0後必須提供：Commit SHA、完整變更清單、測試指令與結果、未通過項目、Rollback方式、受保護文件零修改證據、Legacy／正式資產零接觸證據、額外費用狀態、P0驗證報告及PASS／PASS_WITH_CONDITIONS／FAIL結論。

本授權不允許合併main。P0完成後須先進入P0 Acceptance Review。
