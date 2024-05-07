from enum import Enum
import sys
from typing import Optional, TextIO


class MenuOptions(Enum):
    ShowBalance = "1"
    AddEntry = "2"
    EditEntry = "3"
    FindEntry = "4"
    DisplayEntries = "5"
    Save = "6"
    SaveAs = "7"
    LoadDefault = "8"
    LoadSelected = "9"
    New = "10"
    Quit = "q"


class MainMenu:
    """ Класс, представляющий меню для взаимодействия с пользователем. """
    @staticmethod
    def print_main_menu(truncated: bool = False) -> None:
        """
        Показать главное меню пользователю.

        Args:
             truncated (bool): Показать сокращенную версию меню.
        """

        print("Выберите действие:")
        if truncated:
            print("1) Загрузить кошелёк")
            print("2) Загрузить кошелёк (выбор файла)")
            print("3) Новый кошелёк")
        else:
            print("1) Показать баланс")
            print("2) Добавить запись")
            print("3) Редактировать запись")
            print("4) Найти запись")
            print("\n5) Показать все записи")
            print("\n6) Сохранить кошелёк")
            print("7) Сохранить кошелёк как...")
            print("8) Загрузить кошелёк")
            print("9) Загрузить кошелёк (выбор файла)")
            print("10) Новый кошелёк")
        print("\nq - Выход")

    @staticmethod
    def get_user_menu_choice(
        truncated: bool = False,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> MenuOptions:
        """
        Запросить выбор действия в меню у пользователя.

        Args:
             truncated (bool): выполнить запрос для сокращенного меню.
             input_stream (Optional[TextIO]): поток ввода данных.

        Returns:
            MenuOptions
        """

        MainMenu.print_main_menu(truncated)
        choice = None
        while not choice:
            try:
                choice = input_stream.readline().rstrip('\n')
                if truncated and choice.isnumeric():
                    choice = str(int(choice) + 7)
                choice = MenuOptions(choice)
            except ValueError:
                sys.stdout
                print("Неверный выбор.\n")
                choice = None
                MainMenu.print_main_menu(truncated)
        return choice

    @staticmethod
    def print_message(message: str) -> None:
        """
        Показать сообщение пользователю.

        Args:
             message (str): сообщение для отображения.
        """

        print(message+"\n")

    @staticmethod
    def get_filepath(
        loading: bool = False,
        input_stream: Optional[TextIO] = sys.stdin,
    ) -> str:
        """
        Запросить у пользователя путь для сохранения/загрузки файла.

        Args:
            loading (bool): отобразить запрос для загрузки.
            input_stream (Optional[TextIO]): поток ввода данных.
        Return:
            str
        """

        if loading:
            print("Введите путь и имя файла для загрузки.")
        else:
            print("Введите путь и имя файла для сохранения.")
        print("(пустой ввод - использование значения по умолчанию)")
        return input_stream.readline().rstrip('\n')
