from fastapi import FastAPI, HTTPException, Depends, Query, Request, status
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError 
from . import models, database
from datetime import datetime, timedelta
from shared.models import Book, User
import requests
from .config import config


app = FastAPI()

BACKEND_API_URL = config.BACKEND_API_URL

print(f"Loaded FRONTEND_API_URL: {BACKEND_API_URL}") 
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/books", response_model=List[Book])
def list_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).filter(models.Book.available == True).all()

@app.post("/books", status_code=201)
def add_book(book: Book, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.dict())
    print(book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/filter", response_model=List[Book])
def filter_books(publisher: Optional[str] = Query(None), category: Optional[str] = Query(None), db: Session = Depends(database.get_db)):
    query = db.query(models.Book).filter(models.Book.available == True)
    if publisher:
        query = query.filter(models.Book.publisher == publisher)
    if category:
        query = query.filter(models.Book.category == category)
    return query.all()

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/users", status_code=201)
def enroll_user(user: User, db: Session = Depends(database.get_db)):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        api_url = f"{BACKEND_API_URL}/users" 
        requests.post(api_url, json=db_user.dict())

        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}"
        )

@app.post("/loans", status_code=201)
async def borrow_book(request: Request, db: Session = Depends(database.get_db)):
    data = await request.json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    days = data.get('days')

    if not all([book_id, user_id, days]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or not book.available:
        raise HTTPException(status_code=400, detail="Book not available")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    borrow_date = datetime.now()
    
    return_date = datetime.now().date() + timedelta(days=days)

    loan = models.Loan(book_id=book_id, user_id=user_id, borrow_date=borrow_date, return_date=return_date)
    db.add(loan)
    book.available = False
    db.commit()
    db.refresh(loan)
    api_url = f"{BACKEND_API_URL}/loans"
    try:
        response = requests.post(api_url, json=loan.dict())
        if response.status_code != 201:
            print(f"Warning: Backend API returned status code {response.status_code}")
    except Exception as e:
        print(f"Error posting to backend: {str(e)}")
    return loan