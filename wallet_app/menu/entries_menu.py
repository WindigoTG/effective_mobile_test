from datetime import date
import sys
from typing import Any, Dict, List, Optional, TextIO, Tuple

from wallet.entry import CATEGORY, EntryCategory, WalletEntry
from wallet.wallet import SearchField


class EntriesMenu:
    """
    Класс, представляющий меню для взаимодействия с пользователем
    для работы с записями кошелька.
    """
    @staticmethod
    def get_data_for_new_entry(
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[Dict[str, Any]]:
        """
        Запросить у пользователя данные для новой записи в кошелке.

        Args:
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            Dict[str, Any] или None в случае отмены.
        """

        entry_date = EntriesMenu._get_date(input_stream=input_stream)
        if not entry_date:
            return

        category = EntriesMenu._get_category(input_stream=input_stream)
        if not category:
            return

        amount = EntriesMenu._get_amount(input_stream=input_stream)
        if not amount:
            return

        print("Введите описание:\n")
        description = input_stream.readline().rstrip('\n')

        return {
            "date": entry_date,
            "category": category,
            "amount": amount,
            "description": description,
        }

    @staticmethod
    def get_data_to_edit_entry(
        entry: WalletEntry,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Dict[str, Any]:
        """
        Запросить у пользователя данные для редактирования записи в кошелке.

        Args:
            entry (WalletEntry): существующая запись для редактирования.
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            Dict[str, Any]
        """

        entry_date = EntriesMenu._get_date(
            entry.date,
            input_stream=input_stream,
        )
        if not entry_date:
            entry_date = entry.date

        category = EntriesMenu._get_category(
            entry.category,
            input_stream=input_stream,
        )
        if not category:
            category = entry.category

        amount = EntriesMenu._get_amount(
            entry.amount,
            input_stream=input_stream,
        )
        if not amount:
            amount = entry.amount

        print("Введите описание:\n")
        description = input_stream.readline().rstrip('\n')

        if not description:
            while True:
                print("1) Очистить описание\n2) Не менять описание")
                user_input = input_stream.readline().rstrip('\n')
                if user_input not in ["1", "2"]:
                    continue

                if user_input == "2":
                    description = entry.description
                break

        return {
            "date": entry_date,
            "category": category,
            "amount": amount,
            "description": description,
        }

    @staticmethod
    def _get_date(
        prev_date: Optional[date] = None,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[date]:
        """
        Запросить у пользователя новую дату.

        Args:
            prev_date (date) предыдущая дата.
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            datetime.date или None в случае отмены.
        """

        message = "Введите дату в формате ГГГГ-ММ-ДД"
        if prev_date:
            message += f" Предыдущая дата: {prev_date}"

        while True:
            print(message)
            print(
                "(пустой ввод - {term})".format(
                    term="пропустить" if prev_date else "отмена",
                ),
            )
            user_input = input_stream.readline().rstrip('\n')
            if not user_input:
                return

            try:
                return date.fromisoformat(user_input)
            except ValueError:
                print("Некорректный ввод.\n")

    @staticmethod
    def _get_category(
        prev_category: Optional[EntryCategory] = None,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[EntryCategory]:
        """
        Запросить у пользователя категорию записи.

        Args:
            prev_category (EntryCategory) предыдущая категория.
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            EntryCategory или None в случае отмены.
        """

        message = "Выберите категорию:"
        if prev_category:
            message += f" (Сейчас: {CATEGORY[prev_category]})"
        message += "\n1) Доход.\n2) Расход."

        while True:
            print(message)
            print(
                "(пустой ввод - {term})".format(
                    term="пропустить" if prev_category else "отмена",
                )
            )
            user_input = input_stream.readline().rstrip('\n')
            if not user_input:
                return

            try:
                return EntryCategory(int(user_input))
            except ValueError:
                print("Некорректный ввод.\n")

    @staticmethod
    def _get_amount(
        prev_amount: Optional[float] = None,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[float]:
        """
        Запросить у пользователя сумму.

        Args:
            prev_amount (float) предыдущая сумма.
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            float или None в случае отмены.
        """

        message = "Введите сумму:"
        if prev_amount:
            message += f" (Сейчас: {round(prev_amount, 2)})"

        while True:
            print(message)
            print(
                "(пустой ввод - {term})".format(
                    term="пропустить" if prev_amount else "отмена",
                )
            )
            user_input = input_stream.readline().rstrip('\n')
            if not user_input:
                return

            try:
                amount = round(float(user_input), 2)
                if amount < 0:
                    raise ValueError()
                return amount
            except ValueError:
                print("Некорректный ввод.\n")

    @staticmethod
    def get_entry_number(
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[int]:
        """
        Запросить у пользователя номер записи.

        Args:
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            int или None в случае отмены.
        """

        while True:
            print("Введите номер записи:")
            print("(пустой ввод - отмена)")
            user_input = input_stream.readline().rstrip('\n')
            if not user_input:
                return

            try:
                number = int(user_input)
                if number <= 0:
                    raise ValueError
                return number
            except ValueError:
                print("Некорректный ввод.\n")

    @staticmethod
    def show_entries(
        entries: List[Tuple[int, WalletEntry]],
        per_page: int = 5,
    ) -> None:
        """
        Показать пользователю список записей кошелька.

        Args:
             entries (List[Tuple[int, WalletEntry]]): список записей.
             per_page (int): количество одновременно показанных записей.
        """

        first_index = 0

        while True:
            for number, entry in entries[first_index: first_index + per_page]:
                print(f"{number}) {entry}\n")

            first_index += per_page
            if first_index >= len(entries):
                break

            print(f"Осталось еще {len(entries) - first_index} записей.")
            user_input = input("Продолжить? (Y/n)\n")
            if user_input.lower() not in ["y", "yes"]:
                break

    @staticmethod
    def get_search_query(
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Optional[Tuple[SearchField, str]]:
        """
        Запросить данные для поиска записей у пользователя.

        Args:
            input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            Optional[Tuple[SearchField, str]] или None в случае отмены.
        """

        search_field = None
        while not search_field:
            print(
                "Выберите критерий поиска:\n1) Категория\n2) Дата\n3) Сумма\n",
            )
            user_input = input_stream.readline().rstrip('\n')
            if not user_input:
                return

            try:
                search_field = SearchField(int(user_input))
            except ValueError:
                print("Неверный ввод.")

        search_value = EntriesMenu._get_search_value(
            search_field,
            input_stream=input_stream,
        )

        if not search_value:
            return

        return search_field, search_value

    @staticmethod
    def _get_search_value(
        search_field: SearchField,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> Any:
        if search_field == SearchField.Date:
            return EntriesMenu._get_date(input_stream=input_stream)

        if search_field == SearchField.Category:
            return EntriesMenu._get_category(input_stream=input_stream)

        if search_field == SearchField.Amount:
            return EntriesMenu._get_amount(input_stream=input_stream)
