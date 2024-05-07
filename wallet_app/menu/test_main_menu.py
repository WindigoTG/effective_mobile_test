from io import StringIO
import unittest
import sys
sys.path.append("..")

from wallet_app.menu.main_menu import MainMenu, MenuOptions


class TestMainMenu(unittest.TestCase):
    def test_get_user_menu_choice(self):
        option = MainMenu.get_user_menu_choice(input_stream=StringIO("6"))
        expected = MenuOptions("6")
        self.assertEqual(option, expected)

    def test_get_user_menu_choice_with_incorrect_inputs(self):
        option = MainMenu.get_user_menu_choice(
            input_stream=StringIO("g\nr\n4"),
        )
        expected = MenuOptions("4")
        self.assertEqual(option, expected)

    def test_get_user_menu_choice_truncated(self):
        option = MainMenu.get_user_menu_choice(
            truncated=True,
            input_stream=StringIO("2"),
        )
        expected = MenuOptions("9")
        self.assertEqual(option, expected)

    def test_get_filepath(self):
        path = "data/wallet.json"
        received_path = MainMenu.get_filepath(input_stream=StringIO(path))
        self.assertEqual(received_path, path)
