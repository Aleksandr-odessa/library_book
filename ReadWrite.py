import json
from config import file_books
import aiofiles

class ReadWrite:
    """Класс для чтения и записи данных в файл JSON."""

    __slots__ = ("file_books", "file_keys")

    def __init__(self):
        """Инициализация с указанием пути к файлу."""
        self.file_books = file_books

    async def write_(self, dict_data: dict) -> None:
        """Записать данные в JSON файл.

        Args:
            dict_data (dict): Данные для записи.
        """
        json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)
        async with aiofiles.open(self.file_books, "w") as file:
            await file.write(json_data)

    async def read_(self) -> dict|None:
        """Считать данные из JSON файла.

        Returns:
            dict: Данные, считанные из файла.
        """
        async with aiofiles.open(self.file_books) as file:
            return json.loads(await file.read())

    async def new_write_(self) -> None:
        """Создать новый пустой файл для записи."""
        async with aiofiles.open(self.file_books, "w") as file:
            await file.write('')

