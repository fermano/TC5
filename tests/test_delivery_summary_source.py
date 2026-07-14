import unittest

from src.ticket_workflow_seed import delivery_summary


class DeliverySummarySourceTests(unittest.TestCase):
    def test_default_summary_ignores_source_metadata(self):
        record = {"owner": "billing", "status": "queued", "source": "csv-import"}

        self.assertEqual(
            delivery_summary(record),
            {"owner": "billing", "status": "queued"},
        )

    def test_opt_in_summary_trims_and_includes_source(self):
        record = {"owner": "billing", "status": "queued", "source": " csv-import "}

        self.assertEqual(
            delivery_summary(record, include_source=True),
            {"owner": "billing", "status": "queued", "source": "csv-import"},
        )

    def test_opt_in_summary_uses_unknown_for_blank_source(self):
        record = {"owner": "billing", "status": "queued", "source": "   "}

        self.assertEqual(
            delivery_summary(record, include_source=True)["source"],
            "unknown",
        )

    def test_opt_in_summary_uses_unknown_for_missing_source(self):
        record = {"owner": "billing", "status": "queued"}

        self.assertEqual(
            delivery_summary(record, include_source=True)["source"],
            "unknown",
        )

    def test_summary_does_not_mutate_the_input_record(self):
        record = {"owner": "billing", "status": "queued", "source": " csv-import "}
        original = record.copy()

        delivery_summary(record, include_source=True)

        self.assertEqual(record, original)


if __name__ == "__main__":
    unittest.main()
