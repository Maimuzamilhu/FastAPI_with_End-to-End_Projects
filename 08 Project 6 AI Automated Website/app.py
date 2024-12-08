from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, desc
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from fastapi import Request
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///articles.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Only mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Database Model
class ArticleDB(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    preview = Column(String(250))
    author = Column(String(100))
    date = Column(String(100))
    link = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class ArticleBase(BaseModel):
    title: str
    content: str
    preview: Optional[str] = None
    author: str
    date: str
    link: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/upload", response_model=dict)
async def upload_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = ArticleDB(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return {"message": "Article uploaded successfully"}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    articles = db.query(ArticleDB).order_by(desc(ArticleDB.created_at)).limit(3).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/all", response_class=HTMLResponse)
async def all_news(request: Request, db: Session = Depends(get_db)):
    articles = db.query(ArticleDB).order_by(desc(ArticleDB.created_at)).all()
    return templates.TemplateResponse("all.html", {"request": request, "articles": articles})

@app.get("/article/{id}", response_class=HTMLResponse)
async def article(request: Request, id: int, db: Session = Depends(get_db)):
    article = db.query(ArticleDB).filter(ArticleDB.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return templates.TemplateResponse("article.html", {"request": request, "article": article})

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)