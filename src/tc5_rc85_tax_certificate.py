"""Prototype tax certificate normalizer from before RC85 route rows."""


def _value(payload, snake, camel):
    if snake in payload and payload[snake] is not None:
        return payload[snake]
    if camel in payload and payload[camel] is not None:
        return payload[camel]
    return None


def build_tax_certificate_row(payload, defaults=None):
    cert = _value(payload, "certificate_id", "certificateId")
    exempt = _value(payload, "exempt_cents", "exemptCents")
    exempt_cents = int(exempt or 0)
    return {
        "tenant_id": payload["tenant_id"],
        "destination_id": payload.get("destination_id") or payload.get("route_id") or "primary",
        "invoice_id": payload["invoice_id"],
        "exempt_cents": exempt_cents,
        "certificate_id": cert,
        "status": "exempt" if cert and exempt is not None else "taxable",
        "source": "mainline-tax-cert-normalizer",
    }
