DEFAULT_OWNER = "engineering-ops"


def normalize_owner(owner: str | None) -> str:
    """Return a stable routing owner for operational records."""
    normalized = (owner or "").strip().lower()
    return normalized or DEFAULT_OWNER


def resolve_retry_budget(requested: int | None, default: int = 3) -> int:
    """Preserve explicit retry overrides while supporting a default."""
    if requested is None:
        return default
    if requested < 0:
        raise ValueError("retry budget cannot be negative")
    return requested
