import unittest

from src.ticket_workflow_seed import filter_delivery_records


class DeliveryRecordFilterTests(unittest.TestCase):
    def test_missing_owner_selection_returns_all_records_in_order(self):
        records = [
            {"owner": "billing", "status": "queued"},
            {"owner": "support", "status": "done"},
        ]

        self.assertEqual(filter_delivery_records(records, None), records)

    def test_empty_owner_selection_returns_no_records(self):
        records = [{"owner": "billing", "status": "queued"}]

        self.assertEqual(filter_delivery_records(records, []), [])

    def test_empty_owner_selection_does_not_consume_record_iterator(self):
        def records():
            raise AssertionError("records iterator must not be consumed")
            yield {"owner": "billing", "status": "queued"}

        self.assertEqual(filter_delivery_records(records(), []), [])

    def test_matching_uses_canonical_owner_names_and_keeps_input_order(self):
        records = [
            {"owner": " Billing ", "status": "first"},
            {"owner": "Support", "status": "second"},
            {"owner": "billing", "status": "third"},
        ]

        self.assertEqual(
            filter_delivery_records(records, [" SUPPORT ", "BILLING"]),
            records,
        )

    def test_blank_owner_selection_matches_default_routing_owner(self):
        records = [
            {"owner": None, "status": "missing"},
            {"owner": "engineering-ops", "status": "named"},
            {"owner": "support", "status": "other"},
        ]

        self.assertEqual(filter_delivery_records(records, ["  "]), records[:2])

    def test_filter_does_not_mutate_input_records(self):
        records = [{"owner": " Billing ", "status": "queued"}]
        original = [record.copy() for record in records]

        result = filter_delivery_records(records, ["billing"])

        self.assertEqual(records, original)
        self.assertIs(result[0], records[0])


if __name__ == "__main__":
    unittest.main()
