# import pytest
#
# from library import Library
#
# @pytest.fixture(name='library')
# def library_fixture():
#     library = Library()
#     yield library
#
# @pytest.mark.asyncio
# async def test_add_book (library:Library):
#     book1 = await library.add_book("title3", "author1", "year1")
#     book2 = await library.add_book("title4", "author2", "year2")
#     assert book1['1']['title'] == "title1"
import pytest
from unittest.mock import AsyncMock, MagicMock
from library import Library
from ReadWrite import ReadWrite

@pytest.mark.asyncio
class TestLibrary:

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
    async def test_add_book(self, library, mock_readwrite):
        """Тест на добавление книги в библиотеку"""
        book = await library.add_book("Test Book", "Test Author", 2021)
        assert book['title'] == "Test Book"
        assert book['author'] == "Test Author"
        assert book['year'] == 2021
        assert book['status'] == "в наличии"  # Проверяем, что статус по умолчанию 'в наличии'

    # Тест для отображения книг
    @pytest.mark.asyncio
    async def test_display_books(self, library):
        """Тест на отображение всех книг"""
        await library.add_book("Test Book", "Test Author", 2021)
        books = await library.display_books()
        assert len(books) == 1
        assert books[0]['title'] == "Test Book"

    # Тест для удаления книги
    @pytest.mark.asyncio
    async def test_remove_book(self, library, mock_readwrite):
        """Тест на удаление книги из библиотеки"""
        await library.add_book("Test Book", "Test Author", 2021)
        removed_book = await library.remove_book("1")
        assert removed_book is not None
        assert removed_book['title'] == "Test Book"

    # Тест для поиска книги
    @pytest.mark.asyncio
    async def test_search_books(self, library):
        """Тест на поиск книги по ключевым словам"""
        await library.add_book("Test Book", "Test Author", 2021)
        results = await library.search_books("Test")
        assert len(results) == 1
        assert results[0]['title'] == "Test Book"

    # Тест для поиска книги без результатов
    @pytest.mark.asyncio
    async def test_search_no_results(self, library):
        """Тест на поиск без результатов"""
        await library.add_book("Test Book", "Test Author", 2021)
        results = await library.search_books("Non-existent")
        assert results == []  # Ожидаем пустой список

    # Тест для изменения статуса книги
    @pytest.mark.asyncio
    async def test_change_status(self, library):
        """Тест на изменение статуса книги"""
        await library.add_book("Test Book", "Test Author", 2021)
        updated_book = await library.change_status(1, "Checked Out")
        assert updated_book is not None
        assert updated_book['status'] == "Checked Out"

    # Тест для удаления несуществующей книги
    @pytest.mark.asyncio
    async def test_remove_non_existent_book(self, library):
        """Тест на удаление несуществующей книги"""
        result = await library.remove_book(999)
        assert result is None  # Книга не должна быть найдена
