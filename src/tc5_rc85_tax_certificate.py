"""RC85 tax certificate export helper."""

ARTIFACT_SCHEMA = "rc85.tax.v2"

# The RC85 release artifact is produced from an upstream replay that may use
# either snake-case release-fixture keys or camel-case client keys.  Both spell
# the same field, so the release code path resolves them together instead of
# depending on the fixture dialect.
FIELD_ALIASES = {
    "tenant_id": ("tenant_id", "tenantId"),
    "route_id": ("route_id", "routeId"),
    "destination_id": ("destination_id", "destinationId"),
    "invoice_id": ("invoice_id", "invoiceId"),
    "certificate_id": ("certificate_id", "certificateId"),
    "exempt_cents": ("exempt_cents", "exemptCents"),
}


def _lookup(payload, field):
    """Return ``(present, value)`` for ``field`` across its accepted spellings.

    A field counts as present only when a spelling carries a real value: ``None``
    and blank strings are treated as absent.  A supplied zero is present, which
    is what keeps a zero-cent exemption distinguishable from a missing amount.
    """
    for name in FIELD_ALIASES[field]:
        if name not in payload:
            continue
        value = payload[name]
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue
        return True, value
    return False, None


def _required(payload, field):
    present, value = _lookup(payload, field)
    if not present:
        raise KeyError(field)
    return value


def build_tax_certificate_row(payload, defaults=None):
    defaults = {"taxable_cents": 100, **(defaults or {})}
    tenant_id = _required(payload, "tenant_id")
    invoice_id = _required(payload, "invoice_id")
    route_id = _lookup(payload, "route_id")[1] or _lookup(payload, "destination_id")[1] or "primary"
    exempt_present, exempt_value = _lookup(payload, "exempt_cents")
    exempt_cents = int(exempt_value) if exempt_present else 0
    certificate_id = _lookup(payload, "certificate_id")[1]
    # A certificate plus a supplied exemption amount is an exemption, including
    # when that amount is zero.  Truthiness of the amount is not the test.
    status = "exempt" if certificate_id and exempt_present else "taxable"
    return {
        "tenant_id": tenant_id,
        "route_id": route_id,
        "invoice_id": invoice_id,
        "exempt_cents": exempt_cents,
        "certificate_id": certificate_id,
        "status": status,
        "source": "rc85-route-tax",
        "artifact_schema": ARTIFACT_SCHEMA,
        "tax_key": f"{route_id}:{invoice_id}:{status}",
    }
