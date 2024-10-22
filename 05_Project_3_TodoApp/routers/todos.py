from http.client import HTTPException
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Path


from Models import Todos, Base  # Ensure Base is imported for metadata
from DataBase import   SessionLocal


router = APIRouter()





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    id : int
    title : str = Field(min_length=3)
    description : str =  Field(min_length=3 , max_length=1000)
    priority : int


@router.get("/",  status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async  def read_todo(db: db_dependency, todo_id : int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not  None:
        return  todo_model
    raise HTTPException(status_code =404 , details = "Todo not Found")

@router.post("/todo" , status_code=status.HTTP_201_CREATED)
async  def create_todo(db: db_dependency , todo_request : TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}" , status_code=status.HTTP_204_NO_CONTENT)
async  def update_todo(db : db_dependency , todo_id : int , todo_request: TodoRequest):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise  HTTPException(status_code= 404 , details = "Todo not found")

    todo_model.title = todo_request.title
    todo_model.descriptipn = todo_request.description
    todo_model.priority = todo_request.priority

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}" , status_code= status.HTTP_204_NO_CONTENT)
async  def delete_todo(db : db_dependency , todo_id: int = Path(gt = 0)):
    todo_id = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404 , detail = "Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()