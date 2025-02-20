from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    category: str
    available: bool = True

class User(BaseModel):
    id: Optional[int] = None
    firstname: str
    lastname: str
    email: str

class Loan(BaseModel):
    book_id: int
    user_id: int
    borrow_date: datetime = datetime.now()
    return_date: date 
    returned: bool = False

    __all__ = ["Book", "User", "Loan"]