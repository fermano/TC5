import unittest

from src.tc5_service import DEFAULT_OWNER, normalize_owner, resolve_retry_budget


class TC5ServiceTests(unittest.TestCase):
    def test_blank_owner_uses_default(self):
        self.assertEqual(normalize_owner("   "), DEFAULT_OWNER)

    def test_owner_is_normalized(self):
        self.assertEqual(normalize_owner(" Platform-Ops "), "platform-ops")

    def test_zero_retry_budget_is_preserved(self):
        self.assertEqual(resolve_retry_budget(0), 0)

    def test_negative_retry_budget_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve_retry_budget(-1)


if __name__ == "__main__":
    unittest.main()
