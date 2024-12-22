"""Main modul"""
import asyncio

from config import display_book
from library import Library


async def main() -> None:
    """Основная функция, реализующая меню для взаимодействия с библиотекой."""
    library = Library()
    await library.load_books()
    while True:
        choice = await display_menu()
        match choice:
            case '1':
                await add_book(library)
            case '2':
                await remove_book(library)
            case '3':
                await search_book(library)
            case '4':
                await display_all_books(library)
            case '5':
                await change_book_status(library)
            case '6':
                print("Выход из программы.")
                break
            case _:
                print('Сделайте выбор 1-6')

async def display_menu() -> str:
    """Отображает меню и возвращает выбор пользователя."""
    print("\nМеню:")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Искать книгу")
    print("4. Отобразить все книги")
    print("5. Изменить статус книги")
    print("6. Выход")

    return input("Выберите действие (1-6): ")

async def add_book(library: Library) -> None:
    """Добавляет книгу в библиотеку."""
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = input("Введите год издания: ")
    data = await library.add_book(title, author, year)
    try:
        await display_book(data)
        print("успешно добавлена")
    except KeyError:
        print(data["error"])

async def remove_book(library: Library) -> None:
    """Удаляет книгу из библиотеки."""
    book_id = input("Введите ID книги, которую хотите удалить: ")
    data:dict | None = await library.remove_book(book_id)
    if data:
        await display_book(data)
        print("успешно удалена")
    else:
        print("Указанного id не существует. Повнимательнее пожалуйста")

async def search_book(library: Library) -> None:
    """Ищет книги в библиотеке."""
    search_term = input("Введите название книги, автора или год издания для поиска: ")
    results = await library.search_books(search_term)

    if results:
        print("Найденные книги:")
        for data in results:
            print(
            f"Книга: {data['title']} автор: {data['author']} год издания: {data['year']} "
            f"статус: {data['status']}")
    else:
        print("Книги не найдены.")

async def display_all_books(library: Library) -> None:
    """Отображает все книги в библиотеке."""
    results: list = await library.display_books()

    if results:
        for data in results:
            print(
            f" ID:{data['id']} Книга: {data['title']} автор: {data['author']} "
            f"год издания: {data['year']} статус: {data['status']}")
    else:
        print("Книг пока нет")

async def change_book_status(library: Library) -> None:
    """Изменяет статус книги в библиотеке."""
    try:
        book_id = int(input("Введите ID книги для изменения статуса: "))
        new_status = input("Введите новый статус (1 - в наличии, 2 - выдана): ")

        if new_status not in ["1", "2"]:
            print("Такого выбора нет. Сделайте выбор 1 или 2")
            return

        status = "в наличии" if new_status == "1" else "выдана"
        print(f"Вы выбрали ID: {book_id} и статус: {status}")
        data: dict = await library.change_status(book_id, status)
        await display_book(data)
        print("Статус успешно изменен")

    except ValueError:
        print("Некорректный ввод ID. Пожалуйста, введите число.")

if __name__ == "__main__":
    asyncio.run(main())
