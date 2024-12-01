file_books = "library.json"


async def display_book(data):
    print(f"Книга: {data['title']}\nАвтор: {data['author']}\nГод издания: {data['year']}\nСтатус: {data['status']}")