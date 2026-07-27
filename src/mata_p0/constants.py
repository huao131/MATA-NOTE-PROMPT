"""Locked P0 vocabulary from Manifest V2.2 deliverables and contracts."""

EVIDENCE_STATUSES = frozenset(
    {"VERIFIED", "INFERRED", "UNVERIFIED", "CONFLICTED"}
)
LIFECYCLE_STATUSES = frozenset(
    {
        "DRAFT",
        "REVIEW",
        "APPROVED",
        "LOCKED",
        "SUPERSEDED",
        "ARCHIVED",
        "REJECTED",
    }
)
DEPENDENCY_STATUSES = frozenset(
    {
        "NOT_EVALUATED",
        "PASS",
        "FAIL",
        "DEPENDENCY_RECHECK_REQUIRED",
        "BLOCKED_BY_UPSTREAM",
    }
)
RECHECK_RESULTS = frozenset(
    {
        "NOT_REQUIRED",
        "PASS",
        "FAIL",
        "PENDING",
        "DEPENDENCY_RECHECK_REQUIRED",
    }
)
GATE_STATUSES = frozenset(
    {"NOT_STARTED", "PENDING", "PASS", "FAIL", "BLOCKED", "SUPERSEDED"}
)
GATE_IDS = (
    "creative_lock",
    "story_lock",
    "story_visual_lock",
    "keyframe_lock",
    "production_lock",
    "final_approved",
)
ASSET_USAGE_ROLES = frozenset(
    {"REFERENCE", "DEPENDENCY", "FINAL_ASSET_LIST"}
)
PROTECTED_DESIGNATIONS = frozenset(
    {"LOCK", "FINAL", "MASTER", "APPROVED"}
)
PROTECTED_OPERATIONS = frozenset(
    {"WRITE", "OVERWRITE", "RENAME", "MOVE", "DELETE"}
)
MEDIA_EXTENSIONS = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".svg",
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".flac",
    }
)
