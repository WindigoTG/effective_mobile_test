from typing import Callable, Dict

from wallet_app.menu.main_menu import MainMenu, MenuOptions
from wallet_app.utils.json_handler import JsonHandler
from wallet_app.wallet.entry import EntryCategory, WalletEntry
from wallet_app.wallet.wallet import SearchField, Wallet


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
            MenuOptions.FindEntry: self._find_entry,
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

    def _edit_entry(self) -> None:
        """ Изменение записи в кошельке. """
        if not self.wallet:
            return

    def _find_entry(self) -> None:
        """ Поиск записи в кошельке. """
        if not self.wallet:
            return

    def _show_all_entries(self) -> None:
        """ Показать все записи в кошельке. """
        if not self.wallet:
            return

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
            MainMenu.print_message("Не удалось загрузить кошелёк")
            return

        wallet = Wallet.from_json(wallet_data)

        if wallet:
            self.wallet = wallet
            if path:
                self.wallet_path = path
            MainMenu.print_message("Кошелёк загружен.")
        else:
            MainMenu.print_message("Не удалось загрузить кошелёк")

    def _create_new_wallet(self) -> None:
        """ Создание нового кошелька. """
        self.wallet = Wallet()
        self.wallet_path = ''
        MainMenu.print_message("Создан новый кошелёк.")
