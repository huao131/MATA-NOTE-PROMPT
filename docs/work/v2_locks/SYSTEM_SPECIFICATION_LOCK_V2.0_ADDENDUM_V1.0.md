# SYSTEM SPECIFICATION LOCK V2.0｜P0 Supporting Contract Addendum V1.0

**Addendum ID：** `SYS-SPEC-LOCK-V2.0-ADDENDUM-20260727-001`  
**Scope：** `GLOBAL / P0 FOUNDATION`  
**Status：** `LOCKED_ADDENDUM`  
**Evidence Status：** `VERIFIED`  
**Parent Lock：** `SYS-SPEC-LOCK-V2.0-20260726-001`  
**Repository：** `huao131/MATA-AI-VIDEO-STUDIO`  
**Branch：** `review/v2-system-specification-publication-v2`

## 1. Addendum目的

本Addendum不修改D01–D12任何已鎖定內容，只補足P0實作所需、且已被D07與D11明確引用的兩份Supporting Contract白名單。

## 2. 新增Current Effective Supporting Contracts

| ID | 文件 | 版本 | 用途 | Codex讀取 |
|---|---|---|---|---|
| S01 | `docs/work/v2_drafts/07_FOLDER_REGISTRY_V2.1_DRAFT.md` | V2.1 | Folder Registry唯一正式定義、七筆Folder資料、stable code與Drive ID契約 | true |
| S02 | `docs/work/v2_drafts/08_ASSET_INDEX_AND_IDENTITY_SCHEMA_V2.1_DRAFT.md` | V2.1 | Asset Index必填欄位、Identity、Exact Asset、Rejected與Dependency契約 | true |

## 3. 治理效果

1. S01、S02只作為P0 Supporting Contracts，不新增D13或D14，也不改變D01–D12責任分工。
2. S01、S02與D01–D12同受SYSTEM SPECIFICATION LOCK V2.0保護；不得原地覆寫、改名、移動或刪除。
3. Codex可在P0範圍讀取S01、S02並據此完成Folder Registry與Asset Index契約。
4. 歷史Draft仍不得作為實作依據。
5. 本Addendum不授權P1、P2、P3，不授權合併main、Flow／CapCut、Legacy或正式資產異動。

## 4. 解除阻擋

Codex先前回報的兩項白名單缺口，於本Addendum及Manifest V2.2生效後解除：

- Folder Registry專用規格白名單缺口：RESOLVED
- Asset Index專用規格白名單缺口：RESOLVED
