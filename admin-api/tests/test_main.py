from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models, database

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

database.get_db = override_get_db

models.Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message:": "Welcome to the Admin API"}

def test_add_book():
    book_data = {
        "title": "Half a Yellow", 
        "author": "Adichie baby",
        "publisher": "Wiley",
        "category": "Fiction",
        "available": True}
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    assert response.json()["title"] == book_data["title"]

def test_remove_book():
    book_data = {
        "title": "Half a Yellow", 
        "author": "Adichie baby",
        "publisher": "Wiley",
        "category": "Fiction",
        "available": True
    }
    add_response = client.post("/books", json=book_data)
    book_id = add_response.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

def test_remove_nonexistent_book():
    response = client.delete("/books/999")
    assert response.status_code == 404

def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    user_data = {
        "firstname": "Motun", 
        "lastname": "Alayo", 
        "email": "bims.ayo@gmail.com"
        }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["firstname"] == user_data["firstname"]

def test_create_loan():
    loan_data = {
        "user_id": 1,
        "book_id": 1, 
        "borrow_date": "2025-02-20T10:00:00",
        "return_date": "2025-03-20T10:00:00",
        "returned": False,
    }
    
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 201

