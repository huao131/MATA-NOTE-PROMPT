# History Today Golden Path Governance

The approved J.K. Rowling V6.2 baseline is immutable. Runtime output, validation output, and regression reports must never be written below `golden/history_today/jk_rowling_v6_2/`.

Every change declares `TARGET_MODULE`, `FROZEN_MODULES`, `ALLOWED_FILES`, and `PROHIBITED_FILES`. Only candidate or release-candidate versions may be created before all gates pass. `runners/CURRENT_RELEASE.json` is not changed by development or validation.

All feature flags default to `false`. With every flag disabled, the candidate must preserve the Golden Path. A failed Golden Regression cannot be offset by a passing feature test.

The permanent Flow contract includes scene selection, complete Chinese and English prompts, negative prompt, source image and SHA256, queue/output paths, `WAITING_FOR_FLOW_ASSET`, locked-runner resume, completed-stage preservation, and binding of the returned Flow asset into the timeline. J.K. Rowling regression uses the approved Scene 03 asset and never consumes Flow credits.

Promotion order: RC implementation → unit tests → feature tests → Golden Regression → transport regression → real content QC → human approval → Current Release update. Every approved release records its version, path, SHA256, release time, Golden Regression report, and rollback target.
