from collections.abc import Iterable


DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = (owner or "").strip().lower()
    return normalized or DEFAULT_OWNER


def filter_delivery_records(
    records: Iterable[dict],
    owners: Iterable[str] | None,
) -> list[dict]:
    """Return records matching selected owners without changing their order."""
    if owners is None:
        return list(records)

    selected_owners = {normalize_delivery_owner(owner) for owner in owners}
    if not selected_owners:
        return []

    return [
        record
        for record in records
        if normalize_delivery_owner(record.get("owner")) in selected_owners
    ]


def delivery_summary(record: dict) -> dict:
    """Return the stable summary fields currently exposed to callers."""
    return {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
