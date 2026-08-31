from src.rc105_ember_certificate_export import build_certificate_row


def test_absent_certificate_is_taxable():
    row = build_certificate_row(
        {"tenant": "ember", "invoice_id": "inv-502"},
        {"ledger": "retail", "waived_cents": 0, "artifact_stage": "candidate", "ledger_key": "em-a"},
    )

    assert row["taxable"] is True
    assert row["artifact_stage"] == "candidate"
    assert row["ledger_key"] == "em-a"


def test_positive_snake_waiver_with_certificate_is_exempt():
    row = build_certificate_row(
        {"tenant": "ember", "invoice_id": "inv-503", "certificate_id": "cert-77", "waived_cents": "25"},
        {"ledger": "retail", "waived_cents": 0},
    )

    assert row["taxable"] is False
    assert row["waived_cents"] == 25
