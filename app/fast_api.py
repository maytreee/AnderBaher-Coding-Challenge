from fastapi import FastAPI, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jinja2 import Template
from typing import List
from pydantic import BaseModel
import os

DATABASE_URL = "sqlite:///./data/my_database.db"

# Ensure the directory exists
os.makedirs(os.path.dirname(DATABASE_URL.split("///")[1]), exist_ok=True)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    author_key = Column(String)
    ebook_access = Column(String)
    publish_year = Column(Integer)

Base.metadata.create_all(bind=engine)

# Define Pydantic model
class BookBase(BaseModel):
    title: str
    author: str
    author_key: str
    ebook_access: str
    publish_year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_books():
    db = next(get_db())
    books = db.query(Book).all()
    with open("./templates/index.html") as f:
        template = Template(f.read())
    return template.render(books=books)

@app.get("/books/create", response_class=HTMLResponse)
async def create_book_form():
    with open("./templates/create.html") as f:
        template = Template(f.read())
    return template.render()

@app.post("/books/", response_class=HTMLResponse)
def create_book(title: str = Form(...), author: str = Form(...), author_key: str = Form(...), ebook_access: str = Form(...), publish_year: int = Form(...), db: Session = Depends(get_db)):
    book = BookCreate(title=title, author=author, author_key=author_key, ebook_access=ebook_access, publish_year=publish_year)
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return RedirectResponse(url="/", status_code=303)

@app.get("/books/{book_id}", response_class=HTMLResponse)
async def read_book(book_id: int):
    db = next(get_db())
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    with open("./templates/detail.html") as f:
        template = Template(f.read())
    return template.render(book=book)

@app.get("/books/{book_id}/update", response_class=HTMLResponse)
async def update_book_form(book_id: int):
    db = next(get_db())
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    with open("./templates/update.html") as f:
        template = Template(f.read())
    return template.render(book=book)

@app.post("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, request: Request, db: Session = Depends(get_db)):
    book_data = await request.json()
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
