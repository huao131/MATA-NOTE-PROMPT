# Issue #16 render_frame integration acceptance

- Date: 2026-08-03 (Asia/Taipei)
- Route: local GitHub-inbox-compatible transport → Windows Watcher → Bridge → Codex image_gen handoff → Episode copy → QC → SHA-256 → Asset Index / Production State → callback result
- START: `20260803_SCENE_01_START_V1.png`
- START SHA-256: `B8195CF8ECADA547E0B398BFEFC64629CD3C938D9124B4434F880753AD6155CE`
- END: `20260803_SCENE_01_END_V1.png`
- END SHA-256: `2133CF0C27208211E5BFEF2700C2CEC8D00184465BCEE0D20FA5CC13112A1742`
- FLOW prompt: `20260803_SCENE_01_FLOW_PROMPT_V1.md`
- FLOW prompt SHA-256: `878217EB994B1994C48D295D6F6C1ACE20F174672FEEF204E82D09E2370CB627`
- Frame QC: PASS (PNG, 941×1672, portrait 9:16, single image)
- Unit tests: `python -m unittest tests.test_render_frame_bridge -v` → 3/3 PASS
- Core runner note: existing `CURRENT_RELEASE.json` SHA does not match the checked-out runner; render_frame bypasses Core release loading by design and the Core files were not changed.
