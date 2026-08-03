# 0802 Bartholdi image-generation audit

Verdict: `A. CODEX_DIRECT_IMAGE_TOOL_CONFIRMED`.

Evidence:

- Codex session `019fc1d8-8413-7381-9872-d0b0340c30e2` records built-in `tools.image_gen__imagegen` calls between 2026-08-02 17:46 and 17:58 Asia/Taipei.
- The five final files are byte-identical to five files under `C:\Users\huao3\.codex\generated_images\019fc1d8-8413-7381-9872-d0b0340c30e2`.
- PowerShell `Copy-Item` commands copied those files into the Episode `03_視覺素材` directory.
- `RUN_END_TO_END_GOLDEN_PATH.ps1` only checks that five scene PNG files exist, then uses FFmpeg to scale/crop them for the 1080x1920 motion timeline. It has no image-generation call.

The built-in generator received portrait 9:16 instructions in each prompt. It did not receive width, height, or output-path parameters. Native returned PNG dimensions were 941x1672; downstream FFmpeg normalized the video canvas to 1080x1920.

The reusable Codex-runtime adapter is `tools/history_today/render_single_frame.codex.js`.
