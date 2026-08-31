"""RC85 tax certificate export helper."""


def _present(payload, name):
    return name in payload and payload[name] is not None


def build_tax_certificate_row(payload, defaults=None):
    defaults = {"taxable_cents": 100, **(defaults or {})}
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    exempt_cents = int(payload.get("exempt_cents") or 0)
    certificate_id = payload.get("certificate_id")
    status = "exempt" if certificate_id and _present(payload, "exempt_cents") else "taxable"
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "invoice_id": payload["invoice_id"],
        "exempt_cents": exempt_cents,
        "certificate_id": certificate_id,
        "status": status,
        "source": "rc85-route-tax",
    }
