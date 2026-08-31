def build_certificate_row(payload, ledger_defaults):
    waived_cents = int(payload.get("waived_cents") or ledger_defaults.get("waived_cents", 0))
    certificate_id = payload.get("certificate_id", "")
    has_certificate = bool(certificate_id)
    taxable = not (has_certificate and waived_cents)
    return {
        "tenant": payload["tenant"],
        "invoice_id": payload["invoice_id"],
        "ledger": ledger_defaults["ledger"],
        "certificate_id": certificate_id,
        "waived_cents": waived_cents,
        "taxable": taxable,
        "artifact_stage": ledger_defaults.get("artifact_stage", "rc105"),
        "ledger_key": ledger_defaults.get("ledger_key", "unset"),
    }
