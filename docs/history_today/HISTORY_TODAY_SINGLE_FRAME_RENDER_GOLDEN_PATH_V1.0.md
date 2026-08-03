# HISTORY TODAY｜Single Frame Render Golden Path V1.0

Status: CURRENT_EFFECTIVE
Effective date: 2026-08-03
Required consumers: ChatGPT, Work, Codex, RendererOrchestrator, QC

## 1. Purpose

Prevent storyboard, collage, infographic, subtitle, logo, or multi-scene contamination during image generation.

## 2. Canonical Rule

ONE FRAME = ONE IMAGE_GENERATION INVOCATION.

ONE INVOCATION = ONE CLEAN VISUAL PROMPT.

Every START frame and END frame is a separate image-generation call and a separate output file.

## 3. Prompt Isolation Contract

Each image-generation payload may contain only:

- current episode ID
- current scene ID
- current frame role: START or END
- pure visual description for that single frame
- 9:16 vertical requirement
- negative constraints

It must not contain:

- complete storyboard
- other scenes
- START and END in the same request
- narration script
- workflow instructions
- markdown tables
- subtitles
- headers
- logos
- brand copy
- layout instructions
- contact sheets
- storyboard sheets
- infographic language

## 4. Output Contract

- exactly one standalone image
- portrait 9:16
- no text
- no subtitles
- no logo
- no UI
- no table
- no collage
- no split screen
- no storyboard grid
- START and END saved as independent files

Canonical file names:

- `{EPISODE_DATE}_{SCENE_ID}_START_V1.png`
- `{EPISODE_DATE}_{SCENE_ID}_END_V1.png`

## 5. Execution Sequence

1. Read CURRENT master database and current episode Production Input Lock.
2. Select exactly one scene and one frame role.
3. Create a clean single-frame visual prompt.
4. Call ChatGPT image generation exactly once.
5. Inspect the returned image.
6. If PASS, save and register the asset.
7. Generate the opposite frame in a new, separate invocation.
8. After START and END both PASS, create the Flow or Meta motion prompt.
9. Continue to the next scene.

## 6. Retry Rule

A failed image may be retried up to three times.

Each retry must remain a single-frame invocation. Do not add storyboard context or multiple alternatives into one request.

## 7. Role Separation

- ChatGPT: production control, prompt isolation, one-by-one image generation, review, continuation.
- Work: specification governance, audit, cross-document consistency, versioning.
- Codex: implementation, testing, forensic recovery, automation code; not the daily interactive image renderer unless explicitly required.
- GitHub: persistent system memory and single source of truth.
- OneDrive: episode assets and production outputs.

## 8. Startup Handshake

At the beginning of every new History Today production chat, ChatGPT must read:

1. `HISTORY_TODAY_MASTER_DATABASE_CURRENT.json`
2. the current master database document
3. this Single Frame Render Golden Path
4. the current episode Production Input Lock
5. current Production State and Asset Index when available

ChatGPT must then report only:

- ACTIVE_EPISODE
- ACTIVE_SCENE
- ACTIVE_FRAME_ROLE
- NEXT_ACTION

It must not ask the user to restate already locked rules.

## 9. Fail-Closed Conditions

Stop before image generation when:

- episode identity is ambiguous
- topic conflicts with Production Input Lock
- more than one frame is included in the request
- prompt contains storyboard, table, subtitle, logo, or multi-scene instructions
- current frame state cannot be determined

## 10. Acceptance Test

PASS requires:

- one invocation produces one standalone image
- portrait 9:16
- no text, table, collage, split screen, or storyboard layout
- START and END generated in separate invocations
- Flow or Meta prompt created only after both frames pass

## 11. Provenance

Recovered from the successful 2026-08-02 Bartholdi Codex session:

- Codex built-in image generation
- five final Scene images produced as separate image-generation invocations
- generated images copied into the Episode visual asset directory
- Golden Runner consumed existing images and did not generate them

The reusable method is the invocation pattern, not a Codex-only dependency.
