import datetime
from enum import IntEnum
from typing import Any, Dict, List, Optional, Tuple

from utils import filters
from wallet.entry import EntryCategory, WalletEntry


class SearchField(IntEnum):
    Category = 1,
    Date = 2,
    Amount = 3


FILTER_FUNCS = {
    SearchField.Category: filters.category_filter,
    SearchField.Date: filters.date_filter,
    SearchField.Amount: filters.amount_filter,
}


class Wallet:
    """ Класс, представляющий кошелёк. """
    _entries: Dict[int, WalletEntry]
    _total: Dict[EntryCategory, float]

    def __init__(self, entries: Optional[List[WalletEntry]] = None):
        """
        Args:
            entries (List[WalletEntry]): список записей кошелька.
        """
        self._entries = {}
        self._total = {
            EntryCategory.Income: 0,
            EntryCategory.Spend: 0,
        }

        if entries:
            for idx, entry in enumerate(entries):
                self._entries[idx] = entry
                self._total[entry.category] += entry.amount

    @property
    def balance(self) -> float:
        """ Текущий баланс кошелька. """
        return round(
            self._total[EntryCategory.Income] - self._total[EntryCategory.Spend],
            2,
        )

    @property
    def total_income(self) -> float:
        """ Сумма доходов кошелька. """
        return round(self._total[EntryCategory.Income], 2)

    @property
    def total_spending(self) -> float:
        """ Сумма расходов кошелька. """
        return round(self._total[EntryCategory.Spend], 2)

    def add_entry(self, new_entry: WalletEntry) -> None:
        """
        Добавить новую запись.

        Args:
            new_entry (WalletEntry): добавляемая запись.
        """

        self._entries[len(self._entries)] = new_entry

        self._total[new_entry.category] += new_entry.amount

    def __setitem__(self, entry_index: int, updated_entry: WalletEntry) -> None:
        """
        Обновление данных записи.

        Args:
            entry_index (int): номер обновляемой записи.
            updated_entry (WalletEntry): запись с обновлёнными данными.
        """

        old_entry = self._entries.get(entry_index)

        if not old_entry:
            print('Несуществующая запись.\n')
            return

        self._total[old_entry.category] -= old_entry.amount

        self._entries[entry_index] = updated_entry

        self._total[updated_entry.category] += updated_entry.amount

    def __getitem__(self, entry_index: int) -> Any:
        """ Получение записи или списка записей. """

        if isinstance(entry_index, int):
            entry = self._entries.get(entry_index)
            if not entry:
                return
            return entry_index, entry

        return list(
            zip(
                list(self._entries.keys())[entry_index],
                list(self._entries.values())[entry_index],
            )
        )

    def __len__(self):
        return len(self._entries)

    def find_entries(
        self,
        search_field: SearchField,
        value: Any,
    ) -> List[Tuple[int, WalletEntry]]:
        """
        Поиск записей.

        Args:
            search_field (SearchField): поле, по которому производится поиск.
            value: искомое значение

        Returns:
            List[Tuple[int, WalletEntry]]
        """
        return list(
            filter(FILTER_FUNCS[search_field](value), self._entries.items())
        )

    def to_json(self):
        return {
            "entries": [entry.to_json() for entry in self._entries.values()]
        }

    @staticmethod
    def from_json(wallet_data: Dict) -> Optional["Wallet"]:
        try:
            entries = wallet_data.get("entries")
            if entries:
                entries = [
                    WalletEntry(
                        date=datetime.date.fromisoformat(entry["date"]),
                        category=EntryCategory(entry["category"]),
                        amount=entry["amount"],
                        description=entry["description"],
                    )
                    for entry in entries
                ]

            return Wallet(entries)
        except ValueError:
            return
