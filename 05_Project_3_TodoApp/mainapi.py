
from fastapi import FastAPI
import  Models
from DataBase import engine, SessionLocal
from  routers import  Auth , todos

app = FastAPI()


Models.Base.metadata.create_all(bind=engine)
app.include_router(Auth.router)
app.include_router(todos.router)
