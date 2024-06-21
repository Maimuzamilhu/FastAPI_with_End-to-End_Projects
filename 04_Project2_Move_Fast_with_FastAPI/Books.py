#uvicorn Books:app --reload

from fastapi import  FastAPI , Body

app = FastAPI()

class book:
    id :int
    title:str
    aurthor:str
    description:str
    rating:int

    def __init__(self , id, title, aurthor , description , rating):
        self.id = id
        self.title = title
        self.aurthor = aurthor
        self.description = description
        self.rating = rating


BOOKS = [
    book(29 , "AGI WILL DESTROY EVERY THING(2050)" , "Muzamil khalid" , "AI IN THE FUTURE" , 5),
    book(43, "AGI WILL DESTROY EVERY THING(2050)", "SAMI MANSOORI", "AI IN THE FUTURE", 5),
    book( 9, "AGI WILL DESTROY EVERY THING(2050)", "HAMZA MANSOORI", "AI IN THE FUTURE", 5),
    book(32, "AGI WILL DESTROY EVERY THING(2050)", "MOIZ KAMLEEN", "AI IN THE FUTURE", 5),
    book(11, "AGI WILL DESTROY EVERY THING(2050)", "RAYYAN MANSOORI", "AI IN THE FUTURE", 5),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)