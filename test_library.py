"""  Модуль тестирования приложения"""
from unittest.mock import AsyncMock, MagicMock
import pytest
from library import Library
from ReadWrite import ReadWrite

@pytest.mark.asyncio
class TestLibrary:
    """
    Тестовый класс для проверки функциональности класса Library.

    Этот класс использует pytest для асинхронного тестирования методов
    класса Library. В тестах предполагается использование мок-объектов
    для имитации поведения зависимостей, таких как ReadWrite.

    Методы в этом классе тестируют различные аспекты работы
    класса Library, включая его методы, обработку ошибок и взаимодействие
    с внешними системами.
     """

    @pytest.fixture
    def mock_readwrite(self):
        """Фикстура для мокирования класса ReadWrite"""
        mock_rw = MagicMock(spec=ReadWrite)
        mock_rw.read_ = AsyncMock(return_value={})  # Симуляция пустого файла (пустой словарь)
        mock_rw.write_ = AsyncMock()
        mock_rw.new_write_ = AsyncMock()
        return mock_rw

    @pytest.fixture
    def library(self, mock_readwrite):
        """Фикстура для инициализации библиотеки с замоканным ReadWrite"""
        library = Library()
        library.file_ = mock_readwrite
        return library

    # Тест для загрузки пустой библиотеки
    @pytest.mark.asyncio
    async def test_load_books_empty_file(self, library, mock_readwrite):
        """Тест на загрузку книг из пустого файла"""
        await library.load_books()
        mock_readwrite.read_.assert_called_once()  # Убедимся, что метод read_ был вызван
        assert library.books == {}  # Ожидаем пустой словарь

    # Тест для добавления книги
    @pytest.mark.asyncio
    async def test_add_book(self, library):
        """Тест на добавление книги в библиотеку"""
        book = await library.add_book("Test Book", "Test Author", "2021")
        assert book['title'] == "Test Book"
        assert book['author'] == "Test Author"
        assert book['year'] == "2021"
        assert book['status'] == "в наличии"  # Проверяем, что статус по умолчанию 'в наличии'

    # Тест для добавления книги (автор как число). Негативный сценарий
    @pytest.mark.asyncio
    async def test_add_book_error_author(self, library):
        """Тест на добавление книги в библиотеку"""
        book = await library.add_book("Test Book", "12345", "2021")
        assert book['error'] == "Имя автора не может быть пустым или содержать цифры"

    # Тест для добавления книги (пустой поле названия книги). Негативный сценарий
    @pytest.mark.asyncio
    async def test_add_book_error_author(self, library):
        """Тест на добавление книги в библиотеку"""
        book = await library.add_book("", "Test Author","2021")
        assert book['error'] == "Введите название книги"

    # Тест для добавления книги (неверный год). Негативный сценарий
    @pytest.mark.asyncio
    async def test_add_book_error_author(self, library):
        """Тест на добавление книги в библиотеку"""
        book = await library.add_book("Test Book", "Test Author", "23569")
        assert book['error'] == "Год введен не верно"

    # Тест для отображения книг
    @pytest.mark.asyncio
    async def test_display_books(self, library):
        """Тест на отображение всех книг"""
        await library.add_book("Test Book", "Test Author", "2021")
        books = await library.display_books()
        assert len(books) == 1
        assert books[0]['title'] == "Test Book"

    # Тест для удаления книги
    @pytest.mark.asyncio
    async def test_remove_book(self, library):
        """Тест на удаление книги из библиотеки"""
        await library.add_book("Test Book", "Test Author", "2021")
        removed_book = await library.remove_book("1")
        assert removed_book is not None
        assert removed_book['title'] == "Test Book"

    # Тест для поиска книги
    @pytest.mark.asyncio
    async def test_search_books(self, library):
        """Тест на поиск книги по ключевым словам"""
        await library.add_book("Test Book", "Test Author", "2021")
        results = await library.search_books("Test")
        assert len(results) == 1
        assert results[0]['title'] == "Test Book"

    # Тест для поиска книги без результатов
    @pytest.mark.asyncio
    async def test_search_no_results(self, library):
        """Тест на поиск без результатов"""
        await library.add_book("Test Book", "Test Author", "2021")
        results = await library.search_books("Non-existent")
        assert results == []  # Ожидаем пустой список

    # Тест для изменения статуса книги
    @pytest.mark.asyncio
    async def test_change_status(self, library):
        """Тест на изменение статуса книги"""
        await library.add_book("Test Book", "Test Author", "2021")
        updated_book = await library.change_status(1, "Checked Out")
        assert updated_book is not None
        assert updated_book['status'] == "Checked Out"

    # Тест для удаления несуществующей книги
    @pytest.mark.asyncio
    async def test_remove_non_existent_book(self, library):
        """Тест на удаление несуществующей книги"""
        result = await library.remove_book("999")
        assert result is None  # Книга не должна быть найдена
