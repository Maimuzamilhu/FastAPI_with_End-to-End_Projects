# uvicorn Books:app --reload

from fastapi import FastAPI , Path , Query , HTTPException
from pydantic import BaseModel , Field
from typing import Optional
from  starlette import  status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date : int
    def __init__(self, id, title, author, description, rating , published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class Book_Request(BaseModel):
    id: Optional[int] = Field(title="Id is not needed")
    title: str = Field(min_length=3,max_length=10)
    author: str = Field(min_length=3,max_length=20)
    description: str = Field(min_length=3,max_length=150)
    rating: int = Field(gt=-1 , lt=5) #greate then :gt and less than :lt
    published_date:int = Field(gt=1999, lt=2031)
    class config:
        json_schema_extra = {
            "Example":{
            "title"  :  "A New Book",
            "Author" :  "Rich Dad Poor Dad",
            "ddescription" : "PUBG PUBG PUBG PUBG PUBG ETC....",
            "Rating" : 5,
            "published_date" : "The Book published on ----"
        }
    }



BOOKS = [
    Book(id=29, title="AGI WILL DESTROY EVERY THING (2050)", author="Muzamil Khalid", description="AI IN THE FUTURE", rating=5 ,published_date=2022),
    Book(id=43, title="AGI WILL DESTROY EVERY THING (2050)", author="Sami Mansoori", description="AI IN THE THE FUTURE", rating=5, published_date=2031),
    Book(id=9, title="AGI WILL DESTROY EVERY THING (2050)", author="Hamza Mansoori", description="AI IN THE FUTURE", rating=5 , published_date=2010),
    Book(id=32, title="AGI WILL DESTROY EVERY THING (2050)", author="Moiz Kamleen", description="AI IN THE FUTURE", rating=5 ,published_date= 2011),
    Book(id=11, title="AGI WILL DESTROY EVERY THING (2050)", author="Rayyan Mansoori", description="AI IN THE FUTURE", rating=5 ,published_date= 2012),
]

# GET endpoint for all books
@app.get("/books" , status_code=status.HTTP_200_OK) #after read_all_books() function is successful then status code will show status of ok
async def read_all_books():
    return BOOKS

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_books_by_raing(book_rating:int = Query(gt=0 , lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def Book_Pubblished_on(publish_date : int = Query(gt=1999, lt=2031)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == publish_date:
             book_to_return.append(book)
        return  book_to_return

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_books(book_id : int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise  HTTPException(status_code=404 , detail="Item Not found")


# POST endpoint for creating a new book
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : Book_Request):
    new_book = Book(**book_request.dict()) #convert the request into Book object
    BOOKS.append(find_book_id(new_book)) #first find book id  then pass new book

@app.put("books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async  def update_book(book : Book_Request):
    book_changes = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            book[i] = book
            book_changes = True
    if not book_changes:
        raise HTTPException(status_code=404 , detail="Item not found")


@app.delete("books/{books_id}", status_code=status.HTTP_204_NO_CONTENT)
async  def update_book(book_id: int = Path(gt=0)):
    book_changes = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changes = True
            break
    if not book_changes:
        raise HTTPException(status_code=404 , detail="Item not found")



# This function is for book id bcz it should be unique
def find_book_id(book: Book):
  """Assigns a unique ID to the book based on the existing books list."""
  if len(BOOKS) == 0:
    book.id = 1
  else:
    book.id = BOOKS[-1].id + 1
  return book