from src.rc105_ember_certificate_export import build_certificate_row


def test_partner_zero_waiver_alias_keeps_certificate_exempt():
    row = build_certificate_row(
        {"tenant": "ember", "invoice_id": "inv-502", "certificate_id": "cert-78", "waivedCents": "0"},
        {"ledger": "retail", "waived_cents": 0, "ledger_key": "em-a"},
    )

    assert row["taxable"] is False
    assert row["waived_cents"] == 0
