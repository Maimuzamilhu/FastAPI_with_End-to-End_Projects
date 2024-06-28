#uvicorn Books:app --reload

from fastapi import  FastAPI # Body
from  pydantic import  BaseModel , Field


app = FastAPI()

class book:
    id :int
    title:str = Field(min_length=3)
    aurthor:str = Field(min_length=1)
    description:str = Field(min_length=1 , max_length=100)
    rating:int= Field(gt=-1 , lt=5)

    def __init__(self , id, title, aurthor , description , rating):
        self.id = id
        self.title = title
        self.aurthor = aurthor
        self.description = description
        self.rating = rating

#Pydantic
class BookRequest(BaseModel):
    id: int
    title: str
    aurthor: str
    description: str
    rating: int


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
async def create_book(book_request: BookRequest):
    new_book = BOOKS(**book_request.dict())
    BOOKS.append(book_request)
