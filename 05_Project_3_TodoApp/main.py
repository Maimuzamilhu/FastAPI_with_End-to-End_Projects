from fastapi import  FastAPI
import  Models
from  DataBase import  engine



app = FastAPI()

Models.Base.metadata.create_all(bind=engine)