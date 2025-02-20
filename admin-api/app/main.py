from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from . import models, database
from .config import config
from shared.models import Book, User, Loan
from datetime import datetime
import requests

app = FastAPI()

FRONTEND_API_URL= config.FRONTEND_API_URL
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/books", status_code=201)
def add_book(book: Book, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    api_url = f"{FRONTEND_API_URL}/books"
    requests.post(api_url, json=db_book.dict())
    return db_book

@app.delete("/books/{book_id}", status_code=204)
def remove_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()

@app.get("/users", response_model=List[User])
def list_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@app.get("/loans")
def list_loans(db: Session = Depends(database.get_db)):
    loans = db.query(models.Loan).join(models.User).join(models.Book).all()
    return [
        {
            "id": loan.id,
            "borrow_date": loan.borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": loan.return_date.strftime("%Y-%m-%d") if loan.return_date else None,
            "returned": loan.returned,
            "user": {
                "id": loan.user.id,
                "firstname": loan.user.firstname,
                "lastname": loan.user.lastname,
                "email": loan.user.email,
            },
            "book": {
                "id": loan.book.id,
                "title": loan.book.title,
                "author": loan.book.author,
            }
        }
        for loan in loans
    ]

@app.post("/loans", status_code=201)
def create_loan(loan_data: dict, db: Session = Depends(database.get_db)):
    if loan_data.get('borrow_date'):
        loan_data['borrow_date'] = datetime.fromisoformat(loan_data['borrow_date'])
    if loan_data.get('return_date'):
        loan_data['return_date'] = datetime.fromisoformat(loan_data['return_date'])
    
    loan = models.Loan(**loan_data)
    db.add(loan)
    
    book = db.query(models.Book).filter(models.Book.id == loan_data['book_id']).first()
    if book:
        book.available = False
    
    db.commit()
    db.refresh(loan)
    return loan

@app.post("/users", status_code=201)
def create_user(data: dict,db: Session = Depends(database.get_db)):
    user = models.User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user