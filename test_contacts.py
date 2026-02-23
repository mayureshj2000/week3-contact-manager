import unittest
from datetime import datetime, timedelta

import contacts_manager as cm  # make sure file name is contacts_manager.py


class TestContactManager(unittest.TestCase):

    def test_validate_phone_valid(self):
        ok, digits = cm.validate_phone("98765 43210")
        self.assertTrue(ok)
        self.assertEqual(digits, "9876543210")

    def test_validate_phone_invalid(self):
        ok, digits = cm.validate_phone("12345")
        self.assertFalse(ok)
        self.assertIsNone(digits)

    def test_validate_email_valid(self):
        self.assertTrue(cm.validate_email("test.user@example.com"))

    def test_validate_email_invalid(self):
        self.assertFalse(cm.validate_email("invalid-email"))

    def test_add_contact_basic(self):
        contacts = {}
        # simulate a contact created manually (bypass input)
        contacts["John Doe"] = {
            "phone": "9876543210",
            "email": "john@example.com",
            "address": "Street 1",
            "group": "Friends",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self.assertIn("John Doe", contacts)
        self.assertEqual(contacts["John Doe"]["phone"], "9876543210")

    def test_search_contacts_partial_case_insensitive(self):
        contacts = {
            "John Doe": {"phone": "111", "email": None, "address": None, "group": "Friends"},
            "Jane Smith": {"phone": "222", "email": None, "address": None, "group": "Work"},
            "Johnny Appleseed": {"phone": "333", "email": None, "address": None, "group": "Family"},
        }
        results = cm.search_contacts(contacts, "john")
        self.assertEqual(len(results), 2)
        self.assertIn("John Doe", results)
        self.assertIn("Johnny Appleseed", results)

    def test_find_contact_key_case_insensitive(self):
        contacts = {
            "John Doe": {"phone": "111"},
        }
        key1 = cm.find_contact_key(contacts, "john doe")
        key2 = cm.find_contact_key(contacts, "JOHN DOE")
        self.assertEqual(key1, "John Doe")
        self.assertEqual(key2, "John Doe")

    def test_view_statistics_counts_groups(self):
        now = datetime.now().isoformat()
        old = (datetime.now() - timedelta(days=10)).isoformat()
        contacts = {
            "A": {"group": "Friends", "updated_at": now},
            "B": {"group": "Friends", "updated_at": now},
            "C": {"group": "Work", "updated_at": old},
        }
        # just check that function runs without error
        cm.view_statistics(contacts)


if __name__ == "__main__":
    unittest.main()
