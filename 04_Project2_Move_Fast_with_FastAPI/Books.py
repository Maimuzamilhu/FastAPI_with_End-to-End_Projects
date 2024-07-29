# uvicorn Books:app --reload

from fastapi import FastAPI
from pydantic import BaseModel , Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class Book_Request(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3,max_length=10)
    author: str = Field(min_length=3,max_length=20)
    description: str = Field(min_length=3,max_length=150)
    rating: int = Field(gt=-1 , lt=5) #greate then :gt and less than :lt



BOOKS = [
    Book(id=29, title="AGI WILL DESTROY EVERY THING (2050)", author="Muzamil Khalid", description="AI IN THE FUTURE", rating=5),
    Book(id=43, title="AGI WILL DESTROY EVERY THING (2050)", author="Sami Mansoori", description="AI IN THE THE FUTURE", rating=5),
    Book(id=9, title="AGI WILL DESTROY EVERY THING (2050)", author="Hamza Mansoori", description="AI IN THE FUTURE", rating=5),
    Book(id=32, title="AGI WILL DESTROY EVERY THING (2050)", author="Moiz Kamleen", description="AI IN THE FUTURE", rating=5),
    Book(id=11, title="AGI WILL DESTROY EVERY THING (2050)", author="Rayyan Mansoori", description="AI IN THE FUTURE", rating=5),
]

# GET endpoint for all books
@app.get("/books")
async def read_all_books():
    return BOOKS

# POST endpoint for creating a new book
@app.post("/create-book")
async def create_book(book_request : Book_Request):
    new_book = Book(**book_request.dict()) #convert the request into Book object
    BOOKS.append(find_book_id(new_book)) #first find book id  then pass new book

# This function is for book id bcz it should be unique
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book