from src.tc5_rc85_tax_certificate import build_tax_certificate_row


def test_certificate_export_uses_route_shape():
    row = build_tax_certificate_row({
        "tenant_id": "ember",
        "route_id": "retail",
        "invoice_id": "inv-502",
        "exempt_cents": 75,
        "certificate_id": "cert-75",
    })
    assert row["route_id"] == "retail"
    assert row["status"] == "exempt"
    assert row["source"] == "rc85-route-tax"


def test_missing_certificate_is_taxable():
    row = build_tax_certificate_row({"tenant_id": "ember", "route_id": "web", "invoice_id": "inv-220"})
    assert row["status"] == "taxable"


def test_zero_cent_exemption_with_certificate_stays_exempt_snake_case():
    row = build_tax_certificate_row({
        "tenant_id": "ember",
        "route_id": "retail",
        "invoice_id": "inv-502",
        "exempt_cents": 0,
        "certificate_id": "cert-zero",
    })
    assert row["status"] == "exempt"
