# 2026-08-03｜Scene 01 Frame and Flow Prompts V1

**Episode ID:** `HISTORY_TODAY_2026_08_03_COLUMBUS_DEPARTURE`  
**Scene:** `01 港口的最後一次告別`  
**Status:** `CURRENT_EFFECTIVE / READY_FOR_ISOLATED_RENDERER`  
**Tool:** `FLOW`

---

## Execution Contract

```text
ONE_TASK = ONE_FRAME
OUTPUT = ONE_SINGLE_9_16_IMAGE
START_FRAME_AND_END_FRAME_MUST_BE_SEPARATE_FILES
NO_STORYBOARD_IMAGE
NO_INFOGRAPHIC
NO_TEXT
NO_LOGO
NO_UI
NO_BORDER
NO_COLLAGE
```

---

## Start Frame Prompt

A single full-frame 9:16 historical cinematic still. Dawn on August 3, 1492, at Palos de la Frontera harbor in Spain. Foreground: restrained farewell figures seen from behind on the stone quay, one hand slightly raised. Midground: sailors handling ropes, wooden barrels and rigging beside three late-15th-century Iberian sailing ships still close to the dock. Background: low harbor buildings, pale blue morning mist and the narrow harbor exit. Quiet tension, farewell, uncertainty, cool dawn haze with the first warm sunlight, realistic wood, canvas, stone and clothing, 35mm cinematic lens, natural depth of field.

### Start Frame Negative Prompt

text, subtitle, title, logo, watermark, UI, border, storyboard, infographic, table, collage, multi-panel, split screen, prompt sheet, production dashboard, modern harbor, motorboat, engine, steamship, fantasy ship, pirate costume, duplicate ship, extra mast, warped rigging, broken hull, modern architecture, people looking at camera, horizontal image, 16:9

### Start Frame Target File

```text
20260803_SCENE_01_START_V1.png
```

---

## End Frame Prompt

A single full-frame 9:16 historical cinematic still. The same three late-15th-century Iberian ships have now left Palos harbor and are moving beyond the harbor mouth into open water. The nearest ship is seen from a low rear three-quarter maritime angle, sails beginning to fill with a light morning wind, a natural wake spreading behind it. The quay and farewell figures are now small in the far background and softened by mist. Warm sunlight breaks across the water while the harbor visibly recedes. Quiet determination, irreversible departure, realistic sea physics, historically accurate hulls, rigging and clothing, cinematic depth.

### End Frame Negative Prompt

text, subtitle, title, logo, watermark, UI, border, storyboard, infographic, table, collage, multi-panel, split screen, prompt sheet, production dashboard, modern harbor, motorboat, engine, steamship, fantasy ship, pirate costume, duplicate ship, extra mast, warped rigging, broken hull, storm, giant waves, heroic cheering, modern architecture, horizontal image, 16:9

### End Frame Target File

```text
20260803_SCENE_01_END_V1.png
```

---

## Flow Motion Prompt

Begin exactly from the approved Scene 01 Start Frame. The final mooring ropes are released. Sailors complete restrained, coordinated movements on deck. The three ships begin to pull away from the quay at a physically believable pace. Their sails gradually catch a light morning wind. Water ripples naturally around the hulls; canvas and small flags move gently. The camera performs a slow rightward lateral drift combined with a subtle backward reveal, keeping the farewell figures visible in the first moments before allowing the departing ships to dominate the frame. The distance between shore and vessels steadily increases. Morning light warms gradually without changing direction. End exactly at the approved Scene 01 End Frame, with the harbor receding in haze and the ships committed to open water.

### Flow Negative Prompt

no sudden acceleration, no camera jump, no zoom snap, no duplicated ships, no changing ship identity, no changing crew count, no new people, no modern objects, no fantasy movement, no hull deformation, no mast bending, no extra sails, no giant waves, no storm, no cheering, no text, no subtitle, no logo, no watermark, no UI, no infographic, no collage

### Flow Target File

```text
20260803_SCENE_01_FLOW_PROMPT_V1.md
```

---

## Gate Logic

```text
START_FRAME_RENDER
→ START_FRAME_QC_PASS
→ SAVE_START_FRAME
→ END_FRAME_RENDER
→ END_FRAME_QC_PASS
→ SAVE_END_FRAME
→ ACTIVATE_FLOW_PROMPT
→ SUBMIT_FLOW_TASK
```

The Flow prompt remains `READY_BUT_NOT_SUBMITTABLE` until both independent 9:16 frame files pass QC.
