def build_certificate_row(payload, ledger_defaults):
    raw_waived = payload.get("waived_cents")
    if raw_waived is None or raw_waived == "":
        raw_waived = ledger_defaults.get("waived_cents", 0)
    waived_cents = int(raw_waived)
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
