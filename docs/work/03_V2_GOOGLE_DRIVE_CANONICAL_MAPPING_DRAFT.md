# 03｜V2 Google Drive Canonical Mapping（DRAFT）

**Status:** DRAFT — verification completed; not a SYSTEM SPECIFICATION LOCK  
**Verified at:** 2026-07-26T04:45:00Z  
**Verification scope:** existing Google Drive IDs; metadata, direct-child listings, and exact-name searches.  
**Change authority:** none. This document records the post-rename state only.

## 1. Verification conclusion

The V2 root was renamed in place. Its Google Drive folder ID is unchanged. The root contains exactly five direct child folders, all using the approved 「編號＋繁體中文顯示名稱」 convention.

The historic folder `MATA AI VIDEO STUDIO OS` remains a separate Legacy root under the same shared-drive parent. It is not a parallel directory inside V2. No folders matching the former English V2 root names or the prohibited parallel structure `00_GLOBAL_OS / 01_SERIES / 02_EPISODES` were found.

## 2. Canonical records

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | child_folder_count | verification_status | verified_at |
|---|---|---|---|---:|---|---|
| V2_ROOT | MATA AI 原創影片製片系統 V2 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0ABSV-eJBI2nfUk9PVA | 5 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_GLOBAL_OS | 01_全域系統規範 | 1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ORIGINAL_VIDEO_LIBRARY | 02_原創影片資料庫 | 14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_SHARED_ASSET_LIBRARY | 03_共用素材資料庫 | 1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_PRODUCTION_DATABASE | 04_製片控制與索引 | 1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE | 05_封存資料庫 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 1 | VERIFIED | 2026-07-26T04:45:00Z |
| V2_ARCHIVE_LEGACY_AUDIT | 01_舊系統稽核 | 1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 4 | VERIFIED | 2026-07-26T04:45:00Z |

## 3. Root and child verification

- Root display name: `MATA AI 原創影片製片系統 V2` — VERIFIED.
- Root parent folder ID: `0ABSV-eJBI2nfUk9PVA` — VERIFIED.
- Root direct-child count: **5** — VERIFIED.
- Root direct children: exactly the five canonical V2 folders in Section 2 — VERIFIED.
- 05_封存資料庫 direct child: `01_舊系統稽核` — VERIFIED.
- 01_舊系統稽核 direct-child count: **4** — VERIFIED:
  - `01_保留清單`
  - `02_遷移清單`
  - `03_封存清單`
  - `04_待刪除候選清單`

## 4. Parallel-structure check

| Check target | Result | Interpretation |
|---|---|---|
| Former English root names: `01_GLOBAL_OS`, `02_ORIGINAL_VIDEO_LIBRARY`, `03_SHARED_ASSET_LIBRARY`, `04_PRODUCTION_DATABASE`, `05_ARCHIVE` | NOT FOUND | No English-name V2 parallel root found. |
| Prohibited parallel structure: `00_GLOBAL_OS`, `01_SERIES`, `02_EPISODES` | NOT FOUND | No prohibited V2 parallel hierarchy found. |
| V2 root direct children | Exactly 5 | No additional Chinese or English sibling root under V2. |
| `MATA AI VIDEO STUDIO OS` | FOUND outside V2; ID `1euWtGAXp4CflYr7mEG3gTYoOVJWjXs3p`; parent `0ABSV-eJBI2nfUk9PVA` | Legacy source retained for audit; not V2 structure and not to be renamed, moved, or deleted by this work. |

## 5. Mapping rules now in force

1. `stable_folder_code` is immutable and is the programmatic reference.
2. `display_name_zh_TW` is the Drive-facing display name.
3. `google_drive_folder_id` is immutable for an in-place rename and must be used for writes and relationship checks.
4. Paths are explanatory only; folder ID plus parent ID is the authoritative location check.
5. A folder is not Canonical merely because its title is similar. It must match the registered stable code, Drive ID, and parent ID.
6. No migration, deletion, or creation of a parallel hierarchy is authorized by this document.

## 6. Open follow-up

This verification establishes only the current physical skeleton. Episode-level folder templates, asset registry fields, and migration decisions remain DRAFT work items and require separate approval before any Drive mutation.
