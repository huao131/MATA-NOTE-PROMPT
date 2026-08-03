# render_single_frame

This adapter preserves the confirmed 0802 method: one Codex built-in `image_gen` invocation per scene asset, prompt-level 9:16 framing, followed by an explicit copy from `CODEX_HOME/generated_images` to the requested destination.

It does not modify the Golden Path or Core Pipeline. The downstream Golden runner only validates and consumes existing `Scene_01.png` through `Scene_05.png`.
