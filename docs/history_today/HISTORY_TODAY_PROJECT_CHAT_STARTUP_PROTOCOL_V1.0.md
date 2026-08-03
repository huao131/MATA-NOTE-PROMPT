# HISTORY TODAY PROJECT CHAT STARTUP PROTOCOL V1.0

## New Episode

Trigger: `[歷史上的今天]`

1. Read `HISTORY_TODAY_MASTER_DATABASE_CURRENT.json`.
2. Follow its V2.5 required reads and establish the new Episode gates.
3. Do not generate a formal Frame until topic, story, storyboard and Production Input Lock approvals are complete.

## Resume Episode

Trigger: `[繼續歷史上的今天]`

1. Read CURRENT.
2. Read `HISTORY_TODAY_ACTIVE_PRODUCTION_STATE_CURRENT.md`.
3. When `ACTIVE_EPISODE`, `ACTIVE_SCENE`, `ACTIVE_FRAME_ROLE` and `NEXT_ACTION` are complete, directly execute `NEXT_ACTION`.
4. Return only:

```text
RESUME = <Episode> / <Scene> / <Frame>
```

5. Do not output a long audit list, re-list every Gate, or ask the user to repeat specifications.
6. If `NEXT_ACTION` is formal image generation, create or point to a Clean Renderer Chat.
7. Enter Recovery Gate only when the short Active Production State is missing or inconsistent.

Formal Frame rule:

```text
ONE FRAME = ONE CLEAN RENDERER CHAT = ONE IMAGE GENERATION INVOCATION = ONE OUTPUT IMAGE
```

Clean Renderer Chat receives only the current Episode, current Scene, START or END role, a single pure visual description, 9:16, and negative constraints for text, subtitles, Logo, UI, tables, dashboards, collages and multi-panel layouts. It must not receive the Master Database, state tables, full Storyboard, other Scenes, both START and END, full narration, workflow explanations, or brand post-production rules.
