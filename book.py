class Book:
    __slots__ = ("title", "author", "year", "status")


    def __init__(self, title, author, year):
        self.title:str = title
        self.author:str = author
        self.year:str = year
        self.status:str = "в наличии"


    def to_dict(self) -> dict:
        return {"title":self.title, "author":self.author, "year":self.year, "status":self.status}