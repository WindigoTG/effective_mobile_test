from dataclasses import dataclass
import datetime
from enum import IntEnum


class EntryCategory(IntEnum):
    """ Перечисление категорий записи. """
    Income = 1
    Spend = 2


CATEGORY = {
    EntryCategory.Income: "Доход",
    EntryCategory.Spend: "Расход",
}


@dataclass(frozen=True)
class WalletEntry:
    """ Класс, представляющий запись в кошельке. """
    date: datetime.date
    category: EntryCategory
    amount: float
    description: str

    def __str__(self):
        return "Дата: {date}\nКатегория: {cat}\nСумма: {amt}\n" \
               "Описание: {desc}".format(
                    date=self.date,
                    cat=CATEGORY[self.category],
                    amt=round(self.amount, 2),
                    desc=self.description,
                )

    def to_json(self):
        return {
            "date": self.date.isoformat(),
            "category": self.category.value,
            "amount": round(self.amount, 2),
            "description": self.description,
        }
