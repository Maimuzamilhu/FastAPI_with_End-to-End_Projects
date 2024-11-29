"""from fastapi import FastAPI
import  Models
from DataBase import engine, SessionLocal
from  routers import  Auth , todos , admin

app = FastAPI()

@app.get("/healthy")
def health_check():
    return { "status" : "healthy"}

Models.Base.metadata.create_all(bind=engine)
app.include_router(Auth.router)
app.include_router(todos.router)
app.include_router(admin.router)"""