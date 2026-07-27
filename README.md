# MATA AI VIDEO STUDIO

This repository is the canonical runtime and episode state source for MATA AI VIDEO STUDIO.

## Daily use

1. Open the repository in Codex.
2. Run `python scripts/validate_episode.py episodes/<episode>`.
3. Only when validation passes, continue the current legal action from `PRODUCTION_STATE.json`.
4. After every Gate or asset approval, update state and commit.
5. Store large media in Google Drive and record Drive file IDs in `ASSET_INDEX.json`.

## Local Studio MVP

Windows 本機網站啟動：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_local_studio.ps1
```

然後開啟 `http://127.0.0.1:8765`。本機網站只監聽 localhost，不呼叫付費 AI API，不自動操作 Flow 或 CapCut。完整設定、OAuth、安全與備份說明請見 `docs/LOCAL_STUDIO_USER_GUIDE_V1.0.md`。

## Create a new episode

`python scripts/create_episode.py EP03 餐飲業`
