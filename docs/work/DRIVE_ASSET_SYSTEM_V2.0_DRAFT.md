# DRIVE_ASSET_SYSTEM_V2.0（DRAFT｜第一批審閱版）

**Status:** DRAFT — Work specification only.  
**Depends on:** PRODUCT DEFINITION LOCK V2.0 and verified Folder Registry V2.  
**Prohibited at this stage:** SYSTEM SPECIFICATION LOCK V2.0, Codex implementation, Drive migration, deletion, or creation of parallel folders.

## 1. Purpose and boundary

Google Drive is the media and project-asset data store. GitHub remains the authoritative source for specifications, production state, version registers, locks, and asset indexes. Drive must not become an untracked second source of production truth.

V2 adopts one physical root, one Chinese display-name interface, stable codes, and immutable Drive IDs. The logical layers Global OS, Series, and Episode are mapped into the verified five-root structure; they are not separate top-level Drive roots.

## 2. Verified canonical root

| Stable code | Display name | Drive ID | Role |
|---|---|---|---|
| V2_ROOT | MATA AI 原創影片製片系統 V2 | 18kOzPEX3QO7qAAqgWYhtIfgfIynWoPbT | Only V2 physical root |
| V2_GLOBAL_OS | 01_全域系統規範 | 1EN1rMhvq3_RVy1f8wfJ04fup3U6-2n_5 | Global reference copies and reusable operating assets |
| V2_ORIGINAL_VIDEO_LIBRARY | 02_原創影片資料庫 | 14mSHtk6_AGUJgx58qPiyPFl0KarFjqtC | Industry → Series/Content Direction → Episode media hierarchy |
| V2_SHARED_ASSET_LIBRARY | 03_共用素材資料庫 | 1Tv5Y2WslnnshOn6Im4Be2tJFiBYN00aV | Reusable Character, Scene, Prop, Exact Asset masters |
| V2_PRODUCTION_DATABASE | 04_製片控制與索引 | 1cm52SBzr7Lsay3ZIxoXyTGp3Y90fvniG | Controlled export copies, registry snapshots, manifests, logs |
| V2_ARCHIVE | 05_封存資料庫 | 1uLoGd1X1Iri-y-1UQMI0Fsj3jjfng3Wz | Archive and legacy audit containment |

## 3. Logical-to-physical mapping

| Logical layer | Physical Drive location | Rule |
|---|---|---|
| Global OS | 01_全域系統規範, 03_共用素材資料庫, 04_製片控制與索引 | Shared standards and reusable assets only; no Episode-specific rule becomes Global by default. |
| Series | 02_原創影片資料庫 / 產業 / 系列或內容方向 | Series rules are scoped to that Series node. |
| Episode | 02_原創影片資料庫 / 產業 / 系列或內容方向 / Episode | One Episode owns one physical media directory and one GitHub state. |
| Legacy audit | 05_封存資料庫 / 01_舊系統稽核 | Retain and classify only; no automatic migration or deletion. |

## 4. Proposed Episode folder template — not yet created

When separately approved, every new Episode folder uses the following stable-code template beneath its Series node. The Chinese display names are the Drive interface; the codes are recorded in GitHub registries.

| Order | Stable code suffix | Display name | Contents |
|---:|---|---|---|
| 01 | PROJECT_CONTROL | 01_專案控制 | Drive manifest copy, links, read-only handoff references |
| 02 | BRIEF_INSIGHT | 02_企劃與洞察 | Brief, insight evidence, approved references |
| 03 | CREATIVE_HOOK | 03_創意與鉤子 | Creative alternatives and Creative Lock copies |
| 04 | STORY | 04_故事與腳本 | Treatment, script, timeline, Story Lock copies |
| 05 | VISUAL_BIBLE | 05_視覺聖經 | Character/Scene/Prop/Lighting specifications |
| 06 | STORYBOARD | 06_分鏡 | Storyboard sheets and frame plans |
| 07 | KEYFRAMES | 07_關鍵影格 | Draft, passed, approved, locked frame outputs |
| 08 | FLOW_PRODUCTION | 08_Flow製片 | Flow packages, inputs, outputs, retry evidence |
| 09 | AUDIO | 09_音訊 | Narration sources, recordings, music licenses |
| 10 | SUBTITLES | 10_字幕 | SRT, transcript, subtitle QA files |
| 11 | EDITING_PACKAGE | 11_剪輯交接包 | Editing manifest, timeline, exports |
| 12 | FINAL_OUTPUT | 12_正式成品 | Final-approved delivery media only |
| 13 | PRODUCTION_LOG | 13_製片紀錄 | QA evidence, production log, learning exports |
| 14 | REJECTED_ARCHIVE | 14_退件與封存 | Rejected or superseded assets; never treated as approved |

This table is a specification, not authorization to create folders.

## 5. Asset state and version controls

- Drive represents physical media state; GitHub registers the authoritative status and version.
- `DRAFT`: exploratory output; may be regenerated.
- `PASSED`: machine/system QC passed; still awaits human decision where required.
- `APPROVED`: human-approved asset; preserve its file and ID.
- `LOCKED`: immutable reference for downstream continuity.
- `REJECTED`: retained in rejected/archive location with reason; cannot enter approved paths.
- `ARCHIVED`: no longer current but retained under governed archive conditions.
- `SUPERSEDED` and `CURRENT_EFFECTIVE` are recorded in external version/lock registers; they do not alter historical LOCK, FINAL, MASTER, or APPROVED files.

## 6. Asset identity fields

Each registered asset must include: `asset_id`, `episode_id`, `stable_folder_code`, `drive_folder_id`, `google_drive_file_id`, `asset_type`, `version`, `status`, `source_asset_ids`, `created_at`, `verified_at`, and `continuity_dependencies`.

For Exact Assets (logos, brand marks, approved portraits, supplied images), additionally record `exact_asset=true` and the approved source file ID. Generative AI must not recreate them as a substitute.

## 7. Legacy governance

The verified legacy audit area is `05_封存資料庫 / 01_舊系統稽核` and presently contains four classification folders: retain, migrate, archive, and delete candidates. A `DELETE CANDIDATE` classification is not deletion approval. Dependency checks, retention decisions, and human authorization are mandatory before any destructive action.

The older standalone root `MATA AI VIDEO STUDIO OS` is kept as external legacy evidence. It is not a V2 root and must not be copied into a new parallel hierarchy.

## 8. Controls and acceptance checks

Before this draft can be promoted for lock review, the following must be completed:

1. Approve or revise the Episode template and naming convention.
2. Define GitHub schemas for Folder Registry, Asset Index, and Version/Lock Registers.
3. Define a repeatable new-Episode folder creation checklist.
4. Define index write-back timing for each Stage 0–9.
5. Test one new Episode without creating a parallel root.
6. Confirm legacy classification ownership and delete-approval process.

## 9. Explicit non-actions

This document does not authorize any folder creation, rename, move, deletion, migration, version overwrite, production-state rewrite, SYSTEM SPECIFICATION LOCK V2.0, or Codex implementation.
