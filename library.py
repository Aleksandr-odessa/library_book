"""Модуль формирования и обработки данных библиотеки"""

import json
from logging import ERROR

from ReadWrite import ReadWrite
from book import Book

class Library:
    """Класс для управления библиотекой книг."""

    __slots__ = ("file_", "books")

    def __init__(self):
        """Инициализация библиотеки, создание экземпляра ReadWrite и словаря для хранения книг."""
        self.file_ = ReadWrite()
        self.books = {}

    async def load_books(self) -> None:
        """Загрузить книги из файла JSON при инициализации.

        Обрабатывает исключения при загрузке, включая отсутствие файла и ошибки декодирования JSON.
        """
        try:
            self.books = await self.file_.read_()
            return self.books
        except FileNotFoundError:
            await self.file_.new_write_()
            self.books = {}
        except json.JSONDecodeError:
            self.books = {}

    async def add_book(self, title: str, author: str, year: str) -> dict:
        """Добавить книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.

        Returns:
            dict: Словарь с данными добавленной книги.
        """
        if not title:
            return {"error": "Введите название книги"}
        if not Library.check_year(year):
            return {"error": "Год введен не верно"}
        if not Library.check_author(author):
            return {"error": "Имя автора не может быть пустым или содержать цифры"}

        book: Book = Book(title, author, year)
        book_id = len(self.books) + 1
        dict_book = book.to_dict()
        self.books[str(book_id)] = dict_book
        await self.file_.write_(self.books)
        return dict_book

    async def display_books(self) -> list:
        """Отобразить все книги в библиотеке.

        Returns:
            list: Список словарей с информацией о книгах.
        """
        return [{"id": id, **book} for id, book in self.books.items()] if self.books else []

    async def remove_book(self, book_id: str) -> dict | None:
        """Удалить книгу из библиотеки по ID.

        Args:
            book_id (str): ID книги для удаления.

        Returns:
            dict | None: Удаленная книга или None, если книга не найдена.
        """
        if book_id in self.books.keys():
            removed_book = self.books.pop(book_id)
            await self.file_.write_(self.books)
            return removed_book
        return None

    async def search_books(self, search_term: str) -> list | None:
        """Искать книги по названию, автору или году издания.

        Args:
            search_term (str): Критерий поиска.

        Returns:
            list | None: Список найденных книг или None, если книги не найдены.
        """
        if not self.books:
            return None
        results = [
            book for book in self.books.values()
            if (search_term in book['title']) or
               (search_term in book['author']) or
               (search_term == str(book['year']))
        ]
        return results

    async def change_status(self, book_id: int, new_status: str) -> None | dict:
        """Изменить статус книги.

        Args:
            book_id (int): ID книги для изменения статуса.
            new_status (str): Новый статус книги.

        Returns:
            None | dict: Обновленная книга или None, если книга не найдена.
        """
        book = self.books.get(str(book_id))
        if not book:
            return None

        book["status"] = new_status
        await self.file_.write_(self.books)
        return book

    @staticmethod
    def check_year(year: str) -> bool:
        """
        Проверяет, является ли заданный год действительным.

        Аргументы:
        year (str): Год, представленный в виде строки.

        Возвращает:
        bool: True, если год является числом и находится в диапазоне от 1500 до 3000 (включительно),
              иначе False.
        """
        if not year.isdigit():
            return False
        if 1500 <= int(year) <= 3000:
            return True

    @staticmethod
    def check_author(author:str) -> bool:
        """
        Проверяет, состоит ли имя автора из букв.

        Аргументы:
        author (str): автор.

        Возвращает:
        bool: True, если автор не является "строкой без цифр",
              иначе False.
        """
        if author and not author.isdigit():
            return True