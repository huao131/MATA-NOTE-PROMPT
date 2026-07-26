# GitHub Repository Structure V2.0｜草案

**狀態：DRAFT／NOT LOCKED。此為 GitHub 邏輯結構，不等同 Google Drive 實體資料夾樹。**

```text
specs/        # canonical specifications and locked references
schemas/      # state, workflow, index schemas
registries/   # version-lock, gates, folder/asset metadata
episodes/     # series/<series_id>/episodes/<episode_id>/ versioned metadata
templates/    # new-episode and handoff templates
tests/        # read-only and TEST_ acceptance fixtures
legacy/       # read-only evidence indexes; original assets remain untouched
docs/work/v2_drafts/ # review drafts, never canonical by filename alone
```

Global rules reside in `specs/` and `schemas/`; Series/Episode metadata resides in `episodes/`; Register and Asset Index records reside in `registries/`. Canonical files use ASCII stable filenames: `<DOMAIN>_V<MAJOR>.<MINOR>_<STATUS>.md` or `<SERIES>_<EPISODE>_<SCOPE>_<TYPE>_v<MAJOR>.<MINOR>_<LIFECYCLE>.<ext>`. Filename is not identity; registers provide immutable ID, version, commit SHA and Drive metadata.

Draft and Canonical are separate: `*_DRAFT.md` is never a Lock by itself. Lock／Version／Asset Index／Production State locations are versioned GitHub records；large media stays in Drive and is referenced by ID/checksum. Legacy is read-only: no move, delete, rename, overwrite or in-place status edit. New V2 records may point to Legacy evidence but cannot mutate it. Repository structure must never be interpreted as a request to duplicate the five Drive root folders.
