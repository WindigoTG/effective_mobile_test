import unittest
import sys
sys.path.append("..")

from datetime import date

from wallet.entry import EntryCategory, WalletEntry
from wallet.wallet import SearchField, Wallet


class TestWallet(unittest.TestCase):
    def setUp(self) -> None:
        self.blank_wallet = Wallet()
        self.entries = [
            WalletEntry(
                date=date.fromisoformat("2024-05-02"),
                category= EntryCategory.Income,
                amount=123.45,
                description="test entry 1",
            ),
            WalletEntry(
                date=date.fromisoformat("2024-05-02"),
                category=EntryCategory.Spend,
                amount=67.89,
                description="test entry 2",
            ),
            WalletEntry(
                date=date.fromisoformat("2024-05-03"),
                category=EntryCategory.Income,
                amount=384.99,
                description="test entry 3",
            ),
            WalletEntry(
                date=date.fromisoformat("2024-05-03"),
                category=EntryCategory.Spend,
                amount=12.95,
                description="test entry 4",
            ),
            WalletEntry(
                date=date.fromisoformat("2024-05-04"),
                category=EntryCategory.Income,
                amount=512.0,
                description="test entry 5",
            ),
            WalletEntry(
                date=date.fromisoformat("2024-05-04"),
                category=EntryCategory.Spend,
                amount=59.99,
                description="test entry 6",
            ),
        ]
        self.wallet = Wallet(self.entries)

    def test_wallet_add_entry(self):
        initial_entries_amt = len(self.blank_wallet)
        self.blank_wallet.add_entry(self.entries[0])
        new_entries_amt = len(self.blank_wallet)
        self.assertEqual(new_entries_amt, initial_entries_amt + 1)

    def test_wallet_get_item(self):
        entry = self.wallet[0]
        expected = (0, self.entries[0])
        self.assertEqual(entry, expected)

    def test_wallet_get_item_out_of_range(self):
        entry = self.blank_wallet[4]
        self.assertIsNone(entry)

    def test_wallet_get_item_range(self):
        entries = self.wallet[2:4]
        expected = [(idx, self.entries[idx]) for idx in range(2, 4)]
        self.assertEqual(entries, expected)

    def test_wallet_get_item_range_with_step(self):
        entries = self.wallet[1:6:2]
        expected = [(idx, self.entries[idx]) for idx in range(1, 6, 2)]
        self.assertEqual(entries, expected)

    def test_wallet_get_item_range_out_of_range(self):
        entries = self.wallet[8:10]
        expected = []
        self.assertEqual(entries, expected)

    def test_wallet_to_json(self):
        self.blank_wallet.add_entry(self.entries[0])
        wallet_json =  self.blank_wallet.to_json()
        expected = {
            "entries" : [
                self.entries[0].to_json(),
            ]
        }
        self.assertEqual(wallet_json, expected)

    def test_wallet_from_json(self):
        wallet_data = {
            "entries": [
                self.entries[4].to_json(),
            ]
        }
        wallet = Wallet.from_json(wallet_data)
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(len(wallet), 1)
        self.assertEqual(wallet[0], (0, self.entries[4]))

    def test_wallet_balance(self):
        initial_balance = self.blank_wallet.balance
        initial_total_income = self.blank_wallet.total_income
        initial_total_spending = self.blank_wallet.total_spending

        self.blank_wallet.add_entry(self.entries[0])

        balance_after_income = self.blank_wallet.balance
        total_income_after_income = self.blank_wallet.total_income
        total_spending_after_income = self.blank_wallet.total_spending

        self.blank_wallet.add_entry(self.entries[1])

        balance_after_spend = self.blank_wallet.balance
        total_income_after_spend = self.blank_wallet.total_income
        total_spending_after_spend = self.blank_wallet.total_spending

        self.assertAlmostEqual(
            balance_after_income,
            initial_balance + self.entries[0].amount,
        )
        self.assertAlmostEqual(
            total_income_after_income,
            initial_total_income + self.entries[0].amount,
        )
        self.assertAlmostEqual(
            total_spending_after_income,
            initial_total_spending,
        )
        self.assertAlmostEqual(
            balance_after_spend,
            balance_after_income - self.entries[1].amount,
        )
        self.assertAlmostEqual(
            total_income_after_spend,
            total_income_after_income,
        )
        self.assertAlmostEqual(
            total_spending_after_spend,
            total_spending_after_income + self.entries[1].amount,
        )

    def test_search_entries_by_date(self):
        found = self.wallet.find_entries(SearchField.Date, "2024-05-02")
        expected = [(idx, self.entries[idx]) for idx in range(2)]
        self.assertEqual(found, expected)

    def test_search_entries_by_date_negative(self):
        found = self.wallet.find_entries(SearchField.Date, "2023-05-02")
        expected = []
        self.assertEqual(found, expected)

    def test_search_entries_by_amount_negative(self):
        found = self.wallet.find_entries(
            SearchField.Amount,
            1024.0,
        )
        expected = []
        self.assertEqual(found, expected)

    def test_search_entries_by_category(self):
        found = self.blank_wallet.find_entries(
            SearchField.Category,
            EntryCategory.Spend,
        )
        expected = []
        self.assertEqual(found, expected)

