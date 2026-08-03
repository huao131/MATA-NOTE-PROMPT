/**
 * Codex built-in image-generation adapter used by History Today.
 *
 * This module is intended for the Codex tool runtime where
 * tools.image_gen__imagegen is available. The built-in tool does not accept
 * an output path or deterministic pixel-size parameter; it saves under
 * CODEX_HOME/generated_images and the caller then copies the selected PNG.
 */
export async function render_single_frame(
  scene_id,
  frame_role,
  visual_prompt,
  negative_prompt,
  output_path,
  width = 1080,
  height = 1920,
) {
  const runtimeTools = globalThis.tools;
  if (!runtimeTools?.image_gen__imagegen) {
    throw new Error("Codex built-in image_gen runtime is unavailable");
  }
  if (!scene_id || !frame_role || !visual_prompt || !output_path) {
    throw new Error("scene_id, frame_role, visual_prompt, and output_path are required");
  }
  if (Math.abs(width / height - 9 / 16) > 0.001) {
    throw new Error(`Requested frame must be 9:16; received ${width}x${height}`);
  }

  const prompt = [
    "Use case: historical-scene.",
    `Asset type: vertical 9:16 cinematic scene image, ${scene_id}, ${frame_role}.`,
    visual_prompt.trim(),
    `Target framing: portrait 9:16 (${width}x${height} delivery canvas); keep useful negative space at top and bottom.`,
    "Create exactly one standalone image.",
    `Avoid: ${negative_prompt || "text, captions, tables, collage, split panels, logos, watermark, modern objects"}.`,
  ].join(" ");

  const result = await runtimeTools.image_gen__imagegen({ prompt });
  return {
    scene_id,
    frame_role,
    prompt,
    output_path,
    width,
    height,
    built_in_result: result,
    save_rule: "Copy the selected generated PNG from CODEX_HOME/generated_images to output_path without altering the source asset.",
  };
}
