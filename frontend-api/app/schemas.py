from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    is_available: bool = True

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True

class BorrowedBookCreate(BaseModel):
    book_id: int
    days: int

class BorrowedBook(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrow_date: date
    return_date: date
    
    class Config:
        from_attributes = True