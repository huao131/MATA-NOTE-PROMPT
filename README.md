# MATA AI VIDEO STUDIO

This repository is the canonical runtime and episode state source for MATA AI VIDEO STUDIO.

## Daily use

1. Open the repository in Codex.
2. Run `python scripts/validate_episode.py episodes/<episode>`.
3. Only when validation passes, continue the current legal action from `PRODUCTION_STATE.json`.
4. After every Gate or asset approval, update state and commit.
5. Store large media in Google Drive and record Drive file IDs in `ASSET_INDEX.json`.

## Create a new episode

`python scripts/create_episode.py EP03 餐飲業`
