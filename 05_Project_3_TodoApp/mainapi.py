from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import  Models
from Models import Todos, Base  # Ensure Base is imported for metadata
from DataBase import engine, SessionLocal

app = FastAPI()


Models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()
