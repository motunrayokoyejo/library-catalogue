from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    author = Column(String(100))
    publisher = Column(String(100)) 
    category = Column(String(100))  
    available = Column(Boolean)
    loans = relationship("Loan", back_populates="book")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    loans = relationship("Loan", back_populates="user") 

    def dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id")) 
    user_id = Column(Integer, ForeignKey("users.id"))
    borrow_date = Column(DateTime)
    return_date = Column(Date)
    returned = Column(Boolean, default=False)
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans") 

    def dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "returned": self.returned
        }