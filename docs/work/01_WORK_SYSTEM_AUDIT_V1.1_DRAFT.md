# 01｜Work System Audit V1.1（DRAFT）

**Status:** V2_SPECIFICATION_REVIEW_PAUSED  
**Evidence policy:** valid evidence statuses are VERIFIED, INFERRED, UNVERIFIED, and CONFLICTED.  
**Scope:** first-batch specification review; no System Specification Lock, Codex implementation, Flow execution, Legacy migration, deletion, or overwrite is authorized.

## 1. Audit conclusion

The physical V2 Google Drive skeleton is VERIFIED. The six first-batch specifications remain drafts. GitHub is the authoritative source for rules, version registers, locks, Asset Index, and Canonical Production State. Google Drive is the authoritative physical store for media and folder identity.

No authoritative EP01/EP02 Production State, Asset Index, B1_V2.0, A2_V1.1, or S1 Flow Package file was available in the reviewed GitHub evidence set. Their ownership, state, and dependencies are UNVERIFIED; they must not be promoted into Canonical Production State.

## 2. Verified V2 Drive records

| stable_folder_code | display_name_zh_TW | google_drive_folder_id | parent_folder_id | evidence_status |
|---|---|---|---|---|
| V2_ROOT | MATA AI 原創影片製片系統 V2 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | 0ABSV-eJBI2nfUk9PVA | VERIFIED |
| V2_GLOBAL_OS | 01_全域系統規範 | 1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | VERIFIED |
| V2_ORIGINAL_VIDEO_LIBRARY | 02_原創影片資料庫 | 14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | VERIFIED |
| V2_SHARED_ASSET_LIBRARY | 03_共用素材資料庫 | 1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | VERIFIED |
| V2_PRODUCTION_DATABASE | 04_製片控制與索引 | 1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | VERIFIED |
| V2_ARCHIVE | 05_封存資料庫 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | VERIFIED |
| V2_ARCHIVE_LEGACY_AUDIT | 01_舊系統稽核 | 1HxcUf9pQ4Djjlc_eIoTlRwm1O7XbNqu6 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | VERIFIED |

## 3. Responsibility boundary

| Domain | GitHub responsibility | Google Drive responsibility |
|---|---|---|
| Specification and state | canonical rule, approval, lock, version, state, index | read-only reference copies where needed |
| Folder identity | canonical registry record | immutable folder ID, parent relationship, Chinese display name |
| Media | Asset Index record and approval state | source, generated media, audio, subtitles, editing and final files |
| Exact Asset | source ID, approval and usage policy | approved original binary only |

Drive filenames and folders do not independently change Production State. A Drive asset becomes usable downstream only after the GitHub register records the required approval.

## 4. Blocking controls

1. Only VERIFIED evidence may update Canonical Production State automatically.
2. INFERRED, UNVERIFIED, and CONFLICTED evidence requires human review and source retrieval.
3. Upstream changes invalidate dependent downstream approvals until dependency re-check is recorded.
4. LOCK, FINAL, MASTER, APPROVED and approved originals are immutable; revisions create a new version and version-register entry.
5. Exact Assets must be placed or composited from the approved original. Generative AI must not redraw, imitate, or substitute them.
