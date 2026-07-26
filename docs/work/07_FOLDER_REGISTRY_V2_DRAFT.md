# 07｜Folder Registry V2（DRAFT）

**Status:** DRAFT — verified physical-folder registry; no Lock is created by this document.  
**Verified at:** 2026-07-26T04:45:00Z  
**Authority:** GitHub is the registry source of truth; Google Drive is the physical asset store.

## 1. Registry contract

Each folder record must retain all six mandatory identity fields:

- `stable_folder_code`
- `display_name_zh_TW`
- `google_drive_folder_id`
- `parent_folder_id`
- `verification_status`
- `verified_at`

`google_drive_folder_id` and `parent_folder_id` are identifiers, not display labels. A folder rename must update only `display_name_zh_TW` after the physical Drive rename is verified; it must never replace the Drive ID.

## 2. Verified folders

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | child_folder_count | verification_status | verified_at |
|---|---|---|---|---:|---|---|
| V2_ROOT | MATA AI 原創影片製片系統 V2 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0ABSV-eJBI2nfUk9PVA | 5 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_GLOBAL_OS | 01_全域系統規範 | 1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ORIGINAL_VIDEO_LIBRARY | 02_原創影片資料庫 | 14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_SHARED_ASSET_LIBRARY | 03_共用素材資料庫 | 1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_PRODUCTION_DATABASE | 04_製片控制與索引 | 1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE | 05_封存資料庫 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 1 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE_LEGACY_AUDIT | 01_舊系統稽核 | 1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 4 | VERIFIED | 2026-07-26T04:45:00Z |

## 3. Parent-child assertions

| Parent stable code | Expected direct children | Observed | Status |
|---|---|---:|---|
| V2_ROOT | V2_GLOBAL_OS, V2_ORIGINAL_VIDEO_LIBRARY, V2_SHARED_ASSET_LIBRARY, V2_PRODUCTION_DATABASE, V2_ARCHIVE | 5 | VERIFIED |
| V2_ARCHIVE | V2_ARCHIVE_LEGACY_AUDIT | 1 | VERIFIED |
| V2_ARCHIVE_LEGACY_AUDIT | 01_保留清單, 02_遷移清單, 03_封存清單, 04_待刪除候選清單 | 4 | VERIFIED |

## 4. Status vocabulary

- `VERIFIED`: metadata title, folder ID, parent relationship, and direct-child count were observed in Drive.
- `PENDING_VERIFICATION`: planned record not yet physically present or not yet rechecked.
- `MISMATCH`: a physical Drive record differs from its registered ID, parent, or required display name.
- `DEPRECATED_REFERENCE`: retained only for historical traceability; never a target for new V2 writes.

## 5. Legacy boundary

The separate historical root `MATA AI VIDEO STUDIO OS` (ID `1euWtGAXp4CflYr7mEG3gTYoOVJWjXs3p`) has the same shared-drive parent as V2 but is outside the V2 root. It is a `DEPRECATED_REFERENCE` for audit only. It must not receive new V2 assets, and it is not a parallel V2 hierarchy.

## 6. Write and change controls

1. Before any write, resolve the target by stable folder code through this registry.
2. Before creating a child, list the intended parent and check the proposed child name and code for collision.
3. After any Drive-side rename, move, or child creation, re-read metadata and update `verification_status` and `verified_at`.
4. A folder title alone must not be used to infer parentage or canonical status.
5. `LOCK`, `FINAL`, `MASTER`, and `APPROVED` files are not altered by registry maintenance.
6. The legacy root may be audited but may not be moved, renamed, or deleted under the V2 work scope.

## 7. Deferred records

Episode templates, Series nodes, Project Control folders, and registry/index files are intentionally absent from this registry because they do not yet physically exist in V2. They must be added first as `PENDING_VERIFICATION` only after their creation is separately approved.
