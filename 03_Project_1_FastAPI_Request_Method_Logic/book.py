# to run this type uvicorn book:app --reload
# CRUD operations

from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#path parameter
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


#Query Parameters
@app.get("/books/")
async  def read_category_by_query(category:str):
    book_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            book_to_return.append(book)
    return  book_to_return

#path and query
@app.get("/books/{book_aurthor}")
async  def read_aurthor_category_by_query(book_aurthor : str , category : str):
    book_to_return = []
    for book in BOOKS:
        if book.get("aurthor").casefold() == book_aurthor.casefold() and \
                book.get("category").casefold() == category.casefold():
           book_to_return.append(book)
    return book_to_return

#Post Method for that we have to import Body and get dosnt have body
@app.post("/books/create_body")
async def create_body(new_book=Body()):
    BOOKS.append(new_book)

#Put Method we used this to update
