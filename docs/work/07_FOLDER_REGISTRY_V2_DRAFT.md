# 07｜Folder Registry V2（DRAFT）

**Status:** V2_SPECIFICATION_REVIEW_PAUSED  
**Evidence statuses:** VERIFIED, INFERRED, UNVERIFIED, CONFLICTED. Only VERIFIED evidence may automatically update Canonical Production State.

## Canonical folder records

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | folder_purpose | allowed_content | prohibited_content | verification_status | verified_at |
|---|---|---|---|---|---|---|---|---|
| V2_ROOT | MATA AI 原創影片製片系統 V2 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0ABSV-eJBI2nfUk9PVA | 唯一 V2 根目錄 | 五大 V2 根目錄 | 平行根目錄、未登錄資產 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_GLOBAL_OS | 01_全域系統規範 | 1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 共用規範副本 | 全域參考、受控副本 | Episode 媒體與單集規則 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ORIGINAL_VIDEO_LIBRARY | 02_原創影片資料庫 | 14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | Industry→Series→Episode 媒體 | Episode 資產 | 全域 Master、未登錄來源 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_SHARED_ASSET_LIBRARY | 03_共用素材資料庫 | 1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 可重用 Master 與 Exact Assets | 核准角色、場景、道具、Exact Assets | 未核准生成替代品 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_PRODUCTION_DATABASE | 04_製片控制與索引 | 1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 受控匯出、manifest、log 副本 | Drive manifests、logs、受控匯出 | Canonical Production State 唯一來源 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE | 05_封存資料庫 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 封存與舊系統稽核 | 封存資產、稽核清單 | 新 V2 生產資產 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE_LEGACY_AUDIT | 01_舊系統稽核 | 1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | Legacy 分類證據 | 保留、遷移、封存、待刪除候選清單 | 自動移轉或刪除 | VERIFIED | 2026-07-26T04:45:00Z |

## Identity and write controls

- Stable code and Drive ID are the identity pair; Chinese display name is an interface label only.
- Before a write, resolve stable_folder_code, then verify Drive ID and parent ID. If any ID is absent or mismatched, stop and report; do not create a replacement folder.
- Do not infer canonical status from a similar title. No Chinese/English parallel hierarchy is permitted.
- Partner installations use their own V2_ROOT and their own independent mapping; no partner may reuse Mata老師’s Drive IDs.
- Existing V2 folder skeleton is VERIFIED; proposed Series, Episode, and subfolder nodes are UNVERIFIED until separately approved and physically verified.

## GitHub and Drive boundary

GitHub is canonical for specification, Asset Index, Production State, approvals, locks, version and dependency registers. Drive is canonical for physical files, folder IDs and media storage. Drive placement alone never changes Canonical Production State.

## Freeze

No SYSTEM SPECIFICATION LOCK V2.0, Codex implementation, Flow-point use, Legacy move, deletion, migration, or overwrite is authorized.

## Registry operations

A rename changes only display_name_zh_TW after re-verification. A new record begins UNVERIFIED and cannot become a write target until its physical folder ID and parent relationship are VERIFIED. The external legacy root is a historical reference, not a V2 write target.
