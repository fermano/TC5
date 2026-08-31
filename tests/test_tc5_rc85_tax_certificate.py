import unittest

from src.tc5_rc85_tax_certificate import ARTIFACT_SCHEMA, build_tax_certificate_row

RELEASE_ROW_FIELDS = {
    "tenant_id",
    "route_id",
    "invoice_id",
    "exempt_cents",
    "certificate_id",
    "status",
    "source",
    "artifact_schema",
    "tax_key",
}


class RC85TaxCertificateTests(unittest.TestCase):
    def test_certificate_export_uses_route_shape(self):
        row = build_tax_certificate_row({
            "tenant_id": "ember",
            "route_id": "retail",
            "invoice_id": "inv-502",
            "exempt_cents": 75,
            "certificate_id": "cert-75",
        })
        self.assertEqual(row["route_id"], "retail")
        self.assertEqual(row["status"], "exempt")
        self.assertEqual(row["source"], "rc85-route-tax")
        self.assertEqual(row["artifact_schema"], ARTIFACT_SCHEMA)
        self.assertEqual(row["tax_key"], "retail:inv-502:exempt")

    def test_missing_certificate_is_taxable(self):
        row = build_tax_certificate_row(
            {"tenant_id": "ember", "route_id": "web", "invoice_id": "inv-220"}
        )
        self.assertEqual(row["status"], "taxable")

    def test_ember_camel_case_zero_cent_replay_row_stays_exempt(self):
        """The rc85-ember-tax-20260831-f sample from GitHub #96."""
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "destinationId": "retail",
            "invoiceId": "inv-502",
            "certificateId": "cert-zero",
            "exemptCents": "0",
        })
        self.assertEqual(row["status"], "exempt")
        self.assertEqual(row["exempt_cents"], 0)
        self.assertEqual(row["certificate_id"], "cert-zero")
        self.assertEqual(row["route_id"], "retail")
        self.assertEqual(row["tax_key"], "retail:inv-502:exempt")

    def test_snake_case_zero_cent_exemption_stays_exempt(self):
        row = build_tax_certificate_row({
            "tenant_id": "ember",
            "route_id": "retail",
            "invoice_id": "inv-502",
            "exempt_cents": 0,
            "certificate_id": "cert-zero",
        })
        self.assertEqual(row["status"], "exempt")
        self.assertEqual(row["exempt_cents"], 0)

    def test_camel_case_input_keeps_release_route_row_fields(self):
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "destinationId": "retail",
            "invoiceId": "inv-502",
            "certificateId": "cert-zero",
            "exemptCents": "0",
        })
        self.assertEqual(set(row), RELEASE_ROW_FIELDS)
        self.assertNotIn("destination_id", row)
        self.assertEqual(row["artifact_schema"], ARTIFACT_SCHEMA)

    def test_zero_cent_without_certificate_stays_taxable(self):
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "routeId": "retail",
            "invoiceId": "inv-503",
            "exemptCents": "0",
        })
        self.assertEqual(row["status"], "taxable")
        self.assertEqual(row["tax_key"], "retail:inv-503:taxable")

    def test_certificate_without_exemption_amount_stays_taxable(self):
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "routeId": "retail",
            "invoiceId": "inv-504",
            "certificateId": "cert-none",
        })
        self.assertEqual(row["status"], "taxable")
        self.assertEqual(row["exempt_cents"], 0)

    def test_string_exemption_amounts_are_coerced_to_cents(self):
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "routeId": "retail",
            "invoiceId": "inv-505",
            "certificateId": "cert-75",
            "exemptCents": "75",
        })
        self.assertEqual(row["exempt_cents"], 75)
        self.assertEqual(row["status"], "exempt")

    def test_blank_certificate_or_amount_is_not_an_exemption(self):
        row = build_tax_certificate_row({
            "tenantId": "ember",
            "routeId": "retail",
            "invoiceId": "inv-506",
            "certificateId": "   ",
            "exemptCents": "0",
        })
        self.assertEqual(row["status"], "taxable")
        self.assertIsNone(row["certificate_id"])

    def test_route_id_wins_over_destination_id(self):
        row = build_tax_certificate_row({
            "tenant_id": "ember",
            "route_id": "retail",
            "destination_id": "legacy",
            "invoice_id": "inv-507",
        })
        self.assertEqual(row["route_id"], "retail")

    def test_route_defaults_to_primary(self):
        row = build_tax_certificate_row({"tenantId": "ember", "invoiceId": "inv-508"})
        self.assertEqual(row["route_id"], "primary")
        self.assertEqual(row["tax_key"], "primary:inv-508:taxable")

    def test_missing_required_identifier_raises(self):
        with self.assertRaises(KeyError):
            build_tax_certificate_row({"tenantId": "ember"})


if __name__ == "__main__":
    unittest.main()
