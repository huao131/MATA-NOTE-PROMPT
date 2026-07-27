# CODEX IMPLEMENTATION AUTHORIZATION V1.0｜正式授權紀錄

**Authorization ID：** `CODEX-AUTH-V1.0-20260726-001`  
**Scope：** `GLOBAL / MATA_AI_ORIGINAL_VIDEO_STUDIO_OS_V2`  
**Status：** `AUTHORIZED_WITH_PHASE_GATES`  
**Approved by：** Mata老師  
**Approved at：** `2026-07-26T23:06:48+08:00`  
**Repository：** `huao131/MATA-AI-VIDEO-STUDIO`  
**Locked Specification Head：** `b2215507075b9f90c02f4c6b992a7285a0956d99`  
**Implementation Branch：** `implementation/v2-p0-foundation`

## 1. 授權依據

本授權建立於`SYSTEM SPECIFICATION LOCK V2.0`正式成立之後。Codex只能依下列治理來源工作：

- `docs/work/v2_locks/SYSTEM_SPECIFICATION_LOCK_V2.0_RECORD.md`
- `docs/work/v2_registers/SYSTEM_SPECIFICATION_LOCK_REGISTER_V2.0.json`
- `docs/work/v2_drafts/20_SYSTEM_SPECIFICATION_LOCK_CANDIDATE_MANIFEST_V2.1_DRAFT.md`
- Manifest V2.1列為`CURRENT_EFFECTIVE`且`codex_read_allowed=true`的D01–D12文件
- 本授權紀錄與Codex在實作分支上自行建立的實作、測試與報告文件

歷史Draft、未列入Manifest的文件、Legacy資料與聊天推論不得作為實作依據。

## 2. 實作分支與發布邊界

- 實作分支固定為：`implementation/v2-p0-foundation`
- 基準來源為已包含正式Lock Record與本授權的發布分支
- 不得直接修改或推送`main`
- 不得force push
- 不得重寫正式Repository歷史
- 所有實作必須透過獨立Commit與Pull Request接受審查
- `main`合併目前**未授權**

## 3. 階段授權

### P0｜AUTHORIZED

Codex目前只獲准執行：

1. Schema驗證
2. Folder Registry讀取與驗證
3. Asset Index讀寫契約
4. Version／Lock保護
5. Evidence Status驗證
6. Dependency Recheck引擎
7. Repository治理基礎與必要測試架構
8. P0單元測試、錯誤處理與驗證報告

### P1｜BLOCKED_PENDING_P0_ACCEPTANCE

New Episode初始化、Production State、Gate Register、Segment／Asset狀態、Prompt Library、Storyboard與Flow Handoff資料結構，須等P0驗收PASS後另行授權。

### P2｜BLOCKED_PENDING_P1_ACCEPTANCE

Drive ID映射、實體資產登錄、Exact Asset驗證、CapCut Editing Manifest、SRT與Voiceover Handoff，須等P1驗收PASS後另行授權。

### P3｜BLOCKED_PENDING_P2_ACCEPTANCE

Rejected隔離、Broken Dependency偵測、Lock違規攔截、重複版本攔截、Missing Drive ID停止規則、Rollback與Recovery，須等P2驗收PASS後另行授權。

## 4. 明確禁止行為

Codex不得：

- 覆寫、改名、移動或刪除任何LOCK／FINAL／MASTER／APPROVED文件
- 修改Legacy Episode、Legacy資產或正式媒體
- 直接控制Flow、CapCut、Google Drive或其他外部帳號
- 消耗Flow點數或新增未核准的付費API依賴
- 將非`VERIFIED`證據寫入Canonical Production State
- 將Rejected資產作為Reference或Final Asset
- 以生成內容替代Exact Asset
- 讓Segment Ready自動推升Episode Ready
- 跳過Dependency Recheck、Gate或人工核准
- 合併`main`

## 5. P0測試與驗收條件

P0必須至少證明：

1. 非`VERIFIED`證據無法寫入Canonical State。
2. 受保護文件無法被覆寫。
3. 重複版本號會被拒絕並`STOP_AND_REPORT`。
4. 上游變更會觸發`DEPENDENCY_RECHECK_REQUIRED`。
5. Segment Ready不會推升Episode Ready。
6. 缺少Drive ID會阻塞需要實體資產識別的操作。
7. Rejected資產無法成為Reference。
8. Exact Asset不能被生成資產替代。
9. 所有P0單元測試通過。
10. 沒有引入額外付費API依賴。

P0交付時必須提供：

- Implementation Commit SHA
- 變更檔案清單
- 測試報告
- 失敗案例與Recovery報告
- 受保護文件零修改證據
- 外部API與成本依賴聲明

只有Mata老師核准`P0 ACCEPTANCE = PASS`後，才能建立P1授權。

## 6. 目前授權狀態

```text
SYSTEM_SPECIFICATION_LOCK_V2.0：LOCKED
CODEX_IMPLEMENTATION_AUTHORIZATION：ACTIVE
P0：AUTHORIZED
P1：BLOCKED
P2：BLOCKED
P3：BLOCKED
MAIN_MERGE：NOT_AUTHORIZED
FLOW／CAPCUT CONTROL：NOT_AUTHORIZED
LEGACY／FORMAL ASSET CHANGE：NOT_AUTHORIZED
```
