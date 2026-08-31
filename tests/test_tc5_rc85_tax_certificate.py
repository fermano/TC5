from src.tc5_rc85_tax_certificate import build_tax_certificate_row


def test_camel_zero_cent_certificate_stays_exempt():
    row = build_tax_certificate_row({
        "tenant_id": "ember",
        "destination_id": "retail",
        "invoice_id": "inv-502",
        "exemptCents": "0",
        "certificateId": "cert-zero",
    })
    assert row["status"] == "exempt"
    assert row["exempt_cents"] == 0
