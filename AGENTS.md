# MATA AI VIDEO STUDIO Agent Instructions

Before any production action, read in order:
1. system/MASTER_EXECUTION_SPEC_V1.0_FINAL_LOCK.md
2. system/RUNTIME_STATE_MACHINE_V1.0.md
3. system/QC_GATE_SPEC_V1.0.md
4. current episode/EPISODE_MASTER.md
5. current episode/PRODUCTION_STATE.json
6. current episode/ASSET_INDEX.json
7. current episode/STORYBOARD_MASTER.md

Do not generate if validation fails.
Do not modify LOCKED/MASTER/APPROVED/FINAL content in place.
Exact assets must never be redrawn.
After every image generation, enter QC_WAITING and show only the five legal QC commands.
3+4 means upload and verify first, then advance.
