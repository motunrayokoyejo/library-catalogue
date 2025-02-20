from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    publisher = Column(String(255))
    category = Column(String(255)) 
    available = Column(Boolean)
    loans = relationship("Loan", back_populates="book")

    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "category": self.category,
            "available": self.available
        }

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255))
    lastname = Column(String(255))  
    email = Column(String(255), unique=True, index=True)
    loans = relationship("Loan", back_populates="user") 

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

    