# MATA AI VIDEO STUDIO｜MASTER SOP 補充規範 V1.1

## Golden Rule
GitHub Repository is the ONLY execution source of truth for production. Chat context is working memory only.

Before EVERY keyframe/image/video generation the system MUST:
1. Read latest GitHub MASTER/SOP/LOCK/APPROVED.
2. Read current Production State.
3. Read previous APPROVED keyframe as visual reference.
4. Lock scene, composition, props, camera, aspect ratio and exact assets.
5. If any step fails, STOP generation.
6. Never regenerate an entire scene when only story action changes.
7. Never rely on conversation memory instead of GitHub.

This rule has highest priority over conversation context.