"""RC85 tax certificate export helper."""

ARTIFACT_SCHEMA = "rc85.tax.v2"


def build_tax_certificate_row(payload, defaults=None):
    defaults = {"taxable_cents": 100, **(defaults or {})}
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    exempt_cents = payload.get("exempt_cents") or 0
    certificate_id = payload.get("certificate_id")
    status = "exempt" if certificate_id and exempt_cents else "taxable"
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "invoice_id": payload["invoice_id"],
        "exempt_cents": int(exempt_cents),
        "certificate_id": certificate_id,
        "status": status,
        "source": "rc85-route-tax",
        "artifact_schema": ARTIFACT_SCHEMA,
        "tax_key": f"{route_id}:{payload['invoice_id']}:{status}",
    }
