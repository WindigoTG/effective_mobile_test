import datetime
from typing import Any, Callable, Tuple

from wallet_app.wallet.entry import EntryCategory, WalletEntry


def category_filter(value: Any) -> Callable:
    """ Функция для фильтрования записей кошелька по категории. """
    category = value if isinstance(value, EntryCategory) else None
    if not category:
        try:
            category = EntryCategory(int(value))
        except ValueError:
            pass

    def filter_func(entry: Tuple[int, WalletEntry]) -> bool:
        if not category:
            return False
        return entry[1].category == category

    return filter_func


def amount_filter(value: Any) -> Callable:
    """ Функция для фильтрования записей кошелька по сумме. """
    try:
        value = round(float(value), 2)
    except ValueError:
        value = None

    def filter_func(entry: Tuple[int, WalletEntry]) -> bool:
        if value is None:
            return False
        return abs(round(entry[1].amount, 2) - value) <= 0.001

    return filter_func


def date_filter(value: Any) -> Callable:
    """ Функция для фильтрования записей кошелька по дате. """
    date = value if isinstance(value, datetime.date) else None
    if not date:
        try:
            date = datetime.date.fromisoformat(value)
        except ValueError:
            pass

    def filter_func(entry: Tuple[int, WalletEntry]) -> bool:
        if value is None:
            return False
        return entry[1].date == date

    return filter_func
