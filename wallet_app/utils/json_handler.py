import json
import os.path
from typing import Any, Dict, Optional


class JsonHandler:
    """ Класс, отвечающий за сохранения/загрузку Json файлов. """
    default_path: str

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): пусть для сохранения/загрузки файла по умолчанию.
        """
        if os.path.isabs(file_path):
            self.default_path = file_path
        else:
            self.default_path = os.path.join(
                os.path.abspath(''),
                file_path,
            )

    def load_json(self, file_path: Optional[str] = None) -> Optional[Dict]:
        """
        Загрузить Json файл.

        Args:
            file_path (str): путь к файлу.

        Returns:
            Dict или None
        """

        if not file_path:
            file_path = self.default_path

        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return

    def save_json(self, obj: Any, file_path: Optional[str] = None) -> bool:
        """
        Со[ранить объект в Json файл.

        Args:
            obj: объект для сохранения.
            file_path (str): путь к файлу.

        Returns:
            bool: было ли сохранение успешным.
        """

        if not file_path:
            file_path = self.default_path

        with open(file_path, "w") as file:
            try:
                json.dump(obj, file, indent=2)
                return True
            except TypeError:
                return False
