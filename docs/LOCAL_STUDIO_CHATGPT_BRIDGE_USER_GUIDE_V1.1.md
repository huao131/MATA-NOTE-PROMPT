# LOCAL STUDIO CHATGPT BRIDGE USER GUIDE V1.1

Status: IMPLEMENTATION_READY_FOR_COMMIT
Acceptance: HUMAN_ACCEPTANCE_PENDING

This guide documents the Local Studio V1.1 ChatGPT Work Package Bridge behavior for local-only creative and production review.

## Capabilities
- Create episodes locally and keep the worktree isolated from paid AI execution.
- Generate a ChatGPT work package with specification context, next-step guidance, and Drive mapping metadata.
- Submit artifacts and gate approvals through the local studio workflow.
- Review the dashboard for Git build context, specification context, and Drive availability.

## Dashboard Fields
- Worktree
- Branch
- Commit SHA
- Active Specification Ref
- Specification Commit SHA
- SOP Version
- Specification Sync Status
- Google Drive Sync Status
- paid_ai_api_calls
- working_tree_dirty
- uncommitted_changes_count

## Notes
- Git execution uses the configured local Git binary at the documented absolute path.
- Drive connection remains local-only and never fabricates uploads or verification.
