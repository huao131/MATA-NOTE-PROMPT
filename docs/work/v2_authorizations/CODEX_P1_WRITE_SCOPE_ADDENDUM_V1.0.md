# CODEX P1 WRITE SCOPE ADDENDUM V1.0

## 1. Addendum Identity

| Field | Value |
|---|---|
| Addendum ID | `CODEX-P1-WRITE-SCOPE-ADDENDUM-V1.0-20260727-001` |
| Parent authorization | `CODEX-P1-AUTH-V1.0-20260727-001` |
| Status | `AUTHORIZED` |
| Effective date | `2026-07-27` |
| Repository | `huao131/MATA-AI-VIDEO-STUDIO` |
| P0 accepted baseline | `296a70fd87e4bde4b3bcc064e9aa6612531a4cb1` |

## 2. Governance Basis

本 Addendum 只依據 Current Effective D04、D05、D06、D08、D09、D11、
D12 與已通過 Acceptance Review 的 P0 實作。D06 定義 GitHub 邏輯
結構；P0 Accepted Implementation 已建立 `src/mata_p0/`、
`schemas/p0/`、`tests/p0/` 與 `docs/work/v2_reports/` 的隔離模式。

Current Effective 文件沒有唯一指定 P1 的實體路徑。因此本 Addendum
採用最小、隔離、可回復的 P1 專用路徑，並將它們核准為實作位置。
這是父授權的治理補充，不修改任何 Locked 規格或擴張 P1-01～P1-06。

## 3. Exact Authorized Write Paths

### P1-01 — New Episode initialization plan

- `src/mata_p1/episode_initialization.py`
- `schemas/p1/episode_initialization.schema.json`
- `tests/p1/test_episode_initialization.py`
- `tests/p1/fixtures/TEST_*`

### P1-02 — Production State update workflow

- `src/mata_p1/production_state.py`
- `schemas/p1/production_state.schema.json`
- `tests/p1/test_production_state.py`
- `tests/p1/fixtures/TEST_*`

### P1-03 — Gate Register operations

- `src/mata_p1/gate_register.py`
- `schemas/p1/gate_register.schema.json`
- `tests/p1/test_gate_register.py`
- `tests/p1/fixtures/TEST_*`

### P1-04 — Segment／Asset status handling

- `src/mata_p1/status_handling.py`
- `schemas/p1/segment_asset_status.schema.json`
- `tests/p1/test_status_handling.py`
- `tests/p1/fixtures/TEST_*`

### P1-05 — Prompt Library metadata model

- `src/mata_p1/prompt_metadata.py`
- `schemas/p1/prompt_library_metadata.schema.json`
- `tests/p1/test_prompt_metadata.py`
- `tests/p1/fixtures/TEST_*`

### P1-06 — Storyboard／Flow handoff manifest

- `src/mata_p1/handoff_manifest.py`
- `schemas/p1/storyboard_flow_handoff.schema.json`
- `tests/p1/test_handoff_manifest.py`
- `tests/p1/fixtures/TEST_*`

### Shared P1 files

- `src/mata_p1/__init__.py`
- `src/mata_p1/constants.py`
- `src/mata_p1/errors.py`
- `tests/p1/__init__.py`
- `tests/p1/_support.py`

### P1 validation report

- `docs/work/v2_reports/P1_IMPLEMENTATION_VALIDATION_REPORT_V1.0.md`

## 4. Fixture Boundary

`tests/p1/fixtures/TEST_*` 只允許測試資料。Fixture 必須：

- 以 `TEST_` 開頭；
- 不含正式 Episode、Production State、媒體或 Exact Asset；
- 不含真實 Drive 憑證或對外服務秘密；
- 不觸發 Google Drive、Flow 或 CapCut；
- 只使用離線資料或模擬輸入。

## 5. Scope Enforcement

本 Addendum 不授權整個 `src/`、`schemas/`、`tests/` 或 `docs/`。
除第 3 節明列的精確路徑與 `TEST_*` fixture pattern 外，任何寫入均為
`STOP_AND_REPORT_REQUIRED`。

下列路徑仍不得修改：

- `src/mata_p0/`
- `schemas/p0/`
- `tests/p0/`
- 兩份 P0 報告
- Locked／Final／Master／Approved artifacts
- `legacy/`
- 正式 Episode／Production State
- 圖片、影片、音訊與 Exact Asset

## 6. Phase and External Boundaries

- P1：只有在 P1 Authorization Review PASS 後，才可依父授權開始。
- P2：`BLOCKED`
- P3：`BLOCKED`
- Google Drive operations：禁止
- Flow operations：禁止
- CapCut operations：禁止
- Paid APIs：禁止
- Unapproved third-party packages：禁止
- `implementation/v2-p1-orchestration`：本治理 remediation 不建立。

## 7. Recovery

本 Addendum 與父授權的 remediation 必須以獨立 Commit 發布。若需
Rollback，使用一般 `git revert <remediation-commit-sha>` 建立可稽核
反向 Commit；不得 amend、rebase、reset hard 或 force push。
