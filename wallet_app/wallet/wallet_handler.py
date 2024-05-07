from typing import Callable, Dict

from wallet_app.menu.main_menu import MainMenu, MenuOptions
from wallet_app.menu.entries_menu import EntriesMenu
from wallet_app.utils.json_handler import JsonHandler
from wallet_app.wallet.entry import WalletEntry
from wallet_app.wallet.wallet import Wallet


class WalletHandler:
    """ Класс, отвечающий за работу с кошельком. """
    wallet: Wallet = None
    json_handler: JsonHandler
    actions: Dict[MenuOptions, Callable]

    def __init__(self, default_filepath: str):
        """
        Args:
             default_filepath (str): пусть для сохранения/загрузки
                                     кошелька по умолчанию.
        """
        self.actions = {
            MenuOptions.ShowBalance: self._show_balance,
            MenuOptions.AddEntry: self._add_entry,
            MenuOptions.EditEntry: self._edit_entry,
            MenuOptions.FindEntry: self._find_entries,
            MenuOptions.DisplayEntries: self._show_all_entries,
            MenuOptions.Save: self._save_current_wallet,
            MenuOptions.SaveAs: self._save_wallet_as,
            MenuOptions.LoadDefault: self._load_default_wallet,
            MenuOptions.LoadSelected: self._load_selected_wallet,
            MenuOptions.New: self._create_new_wallet,
        }

        self.json_handler = JsonHandler(default_filepath)
        self.wallet_path = ""

    def run(self) -> None:
        """ Запуск основного рабочего цикла. """

        while True:
            user_choice = MainMenu.get_user_menu_choice(self.wallet is None)
            if user_choice == MenuOptions.Quit:
                break

            self.actions[user_choice]()

    def _show_balance(self) -> None:
        """ Показать баланс кошелька. """

        if not self.wallet:
            return

        MainMenu.print_message(
            "Общий доход: {inc}\nОбщий расход: {spend}\nБаланс: {bal}".format(
                inc=self.wallet.total_income,
                spend=self.wallet.total_spending,
                bal=self.wallet.balance,
            )
        )

    def _add_entry(self) -> None:
        """ Добавление записи в кошелёк. """
        if not self.wallet:
            return

        entry_data = EntriesMenu.get_data_for_new_entry()

        if not entry_data:
            return

        new_entry = WalletEntry(**entry_data)

        self.wallet.add_entry(new_entry)
        MainMenu.print_message("Новая запись добавлена.")

    def _edit_entry(self) -> None:
        """ Изменение записи в кошельке. """
        if not self.wallet:
            return

        if not len(self.wallet):
            MainMenu.print_message("Нет записей для изменения.")
            return

        entry_idx = EntriesMenu.get_entry_number() - 1

        _, entry = self.wallet[entry_idx]
        if not entry:
            MainMenu.print_message("Запись не найдена.")
            return

        updated_data = EntriesMenu.get_data_to_edit_entry(entry)

        updated_entry = WalletEntry(**updated_data)
        self.wallet[entry_idx] = updated_entry
        MainMenu.print_message(
            f"Запись номер {entry_idx} обновлена.",
        )

    def _find_entries(self) -> None:
        """ Поиск записей в кошельке. """
        if not self.wallet:
            return

        if not len(self.wallet):
            MainMenu.print_message("Нет записей для поиска.")
            return

        search_query = EntriesMenu.get_search_query()

        if not search_query:
            return

        entries = self.wallet.find_entries(*search_query)

        if not entries:
            MainMenu.print_message("Не найдено подходящих записей.")

        EntriesMenu.show_entries(entries)

    def _show_all_entries(self) -> None:
        """ Показать все записи в кошельке. """
        if not self.wallet:
            return

        if not len(self.wallet):
            MainMenu.print_message("Нет записей для отображения.")
            return

        entries = self.wallet[0:]
        EntriesMenu.show_entries(entries)

    def _save_current_wallet(self) -> None:
        """ Сохранение текущего кошелька по ранее открытому пути. """
        if not self.wallet:
            return

        self._save_wallet(self.wallet_path)

    def _save_wallet_as(self) -> None:
        """ Сохранение текущего кошелька с запросом пути для сохранения. """
        if not self.wallet:
            return

        path = MainMenu.get_filepath(True)
        self._save_wallet(path)

    def _save_wallet(self, path: str) -> None:
        """
        Сохранения текущего кошелька в файл.

        Args:
            path (str): путь к файлу для сохранения.
        """
        if not self.wallet:
            return

        if self.json_handler.save_json(
            self.wallet.to_json(),
            path,
        ):
            message = "Кошелёк сохранён {path}"
            self.wallet_path = path
        else:
            message = "Не удалось сохранить кошелёк {path}"

        MainMenu.print_message(
                message.format(
                    path=path if path else '',
                )
            )

    def _load_default_wallet(self) -> None:
        """ Загрузка кошелька по умолчанию. """
        self._load_wallet()

    def _load_selected_wallet(self) -> None:
        """ Загрузка кошелька с выбором пути к файлу. """
        path = MainMenu.get_filepath(True)
        self._load_wallet(path)

    def _load_wallet(self, path: str = '') -> None:
        """
        Загрузка кошелька из файла.

        Args:
            path (str): путь файла для загрузки.
        """
        wallet_data = self.json_handler.load_json(path)
        if not wallet_data:
            MainMenu.print_message(
                "Не удалось загрузить кошелёк. Не удалось прочитать файл."
            )
            return

        wallet = Wallet.from_json(wallet_data)

        if wallet:
            self.wallet = wallet
            if path:
                self.wallet_path = path
            MainMenu.print_message("Кошелёк загружен.")
        else:
            MainMenu.print_message(
                "Не удалось загрузить кошелёк. Некорректные данные."
            )

    def _create_new_wallet(self) -> None:
        """ Создание нового кошелька. """
        self.wallet = Wallet()
        self.wallet_path = ''
        MainMenu.print_message("Создан новый кошелёк.")
