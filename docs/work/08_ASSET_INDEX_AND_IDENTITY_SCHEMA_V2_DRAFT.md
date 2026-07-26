# 08｜Asset Index and Identity Schema V2（DRAFT）

**Status:** V2_SPECIFICATION_REVIEW_PAUSED  
**Authority:** GitHub holds the canonical Asset Index and approval/version registers. Google Drive stores physical assets and immutable file/folder IDs.

## 1. Required identity fields

| Field | Rule |
|---|---|
| asset_id | Immutable programmatic identifier; never derived only from a filename |
| episode_id | Required for Episode assets; null only for governed global/shared assets |
| stable_folder_code | Must resolve through Folder Registry V2 |
| display_name_zh_TW | Drive-facing folder display name; not an identity key |
| google_drive_folder_id | Required Drive location identity |
| parent_folder_id | Required for folder assertion |
| google_drive_file_id | Required for registered Drive file |
| asset_type | Controlled category: brief, lock, keyframe, flow_input, flow_output, audio, subtitle, edit_package, final, exact_asset |
| version | Explicit semantic version, e.g. V1.0, V1.1; no silent overwrite |
| approval_status | DRAFT, PASSED, APPROVED, LOCKED, REJECTED, ARCHIVED |
| evidence_status | VERIFIED, INFERRED, UNVERIFIED, or CONFLICTED |
| source_asset_ids | All direct upstream source assets |
| downstream_dependency_ids | All known downstream consumers |
| created_at / verified_at | ISO 8601 timestamps |
| approval_record_id | Required for APPROVED or LOCKED |
| rejection_reason | Required for REJECTED |
| exact_asset | Boolean; requires approved_source_file_id when true |

## 2. Filename grammar

{episode_id}__{asset_type}__{logical_name}__{version}__{approval_status}.{ext}

Examples:

- EP02__KEYFRAME__B1__V2.0__APPROVED.png
- EP02__FLOW_PACKAGE__S1__V1.0__DRAFT.md
- GLOBAL__EXACT_ASSET__SUNLIGHT_GLOBAL_LOGO__V1.0__LOCKED.svg

Filename is a human-readable locator only. The Asset Index keys assets by asset_id and google_drive_file_id.

## 3. State, version, approval and lock rules

- New work is DRAFT; PASSED is QC-passed but not human-approved.
- APPROVED requires an approval record; LOCKED additionally fixes the dependency baseline for downstream use.
- REJECTED must retain its source ID, reason and timestamp in the rejected/archive location and may never be selected as an approved input.
- Historical LOCK, FINAL, MASTER and APPROVED files are never overwritten. Create a new version, then write CURRENT_EFFECTIVE or SUPERSEDED only in the external version/lock register.
- Any source change marks direct and transitive downstream dependencies RECHECK_REQUIRED in the register; no automatic promotion occurs.

## 4. Exact Asset protection

Exact Assets include supplied logos, brand marks, approved portraits, licensed images and any designated source file. They must be copied, linked, masked, composited or otherwise placed from their approved original file ID. Generative AI must not redraw, regenerate, imitate, approximate or replace an Exact Asset. A generated result that contains a substituted Exact Asset is REJECTED.

## 5. Evidence gate

INFERRED, UNVERIFIED, and CONFLICTED rows cannot be written into Canonical Production State automatically. Only an evidence-complete VERIFIED row can be proposed for that state, and normal human approval still applies.
