from datetime import date
from io import StringIO
import unittest
import sys
sys.path.append("..")

from wallet_app.menu.entries_menu import EntriesMenu
from wallet_app.wallet.entry import EntryCategory, WalletEntry
from wallet_app.wallet.wallet import SearchField


class TestEntriesMenu(unittest.TestCase):
    def test_get_data_for_new_entry(self):
        entry_data = EntriesMenu.get_data_for_new_entry(
            input_stream=StringIO("2024-05-02\n1\n123.45\nqwer"),
        )
        expected = {
            "date": date.fromisoformat("2024-05-02"),
            "category": EntryCategory.Income,
            "amount": 123.45,
            "description": "qwer",
        }
        self.assertEqual(entry_data, expected)

    def test_get_data_for_new_entry_cancelled(self):
        entry_data = EntriesMenu.get_data_for_new_entry(
            input_stream=StringIO("2024-05-02\n''\n123.45\nqwer"),
        )
        self.assertIsNone(entry_data)

    def test_get_data_to_edit_entry(self):
        entry = WalletEntry(
            date=date.fromisoformat("2024-05-02"),
            category=EntryCategory.Income,
            amount=123.45,
            description="qwer",
        )
        updated_data = EntriesMenu.get_data_for_new_entry(
            input_stream=StringIO("2024-05-03\n2\n67.89\nqwer"),
        )
        expected = {
            "date": date.fromisoformat("2024-05-03"),
            "category": EntryCategory.Spend,
            "amount": 67.89,
            "description": "qwer",
        }
        self.assertEqual(updated_data, expected)

    def test_get_entry_number(self):
        number = EntriesMenu.get_entry_number(
            input_stream=StringIO("6"),
        )
        self.assertEqual(number, 6)

    def test_search_query_date(self):
        search_query = EntriesMenu.get_search_query(
            input_stream=StringIO("2\n2024-05-03"),
        )
        expected = (SearchField.Date, date.fromisoformat("2024-05-03"))
        self.assertEqual(search_query, expected)

    def test_search_query_category(self):
        search_query = EntriesMenu.get_search_query(
            input_stream=StringIO("1\n2"),
        )
        expected = (SearchField.Category, EntryCategory.Spend)
        self.assertEqual(search_query, expected)

    def test_search_query_amount(self):
        search_query = EntriesMenu.get_search_query(
            input_stream=StringIO("3\n123.45"),
        )
        expected = (SearchField.Amount, 123.45)
        self.assertEqual(search_query, expected)
