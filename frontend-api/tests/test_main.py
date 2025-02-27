from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models, database
import pytest
import uuid

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

@pytest.fixture(autouse=True)
def setup_function():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Frontend API"}

def test_add_book():
    book_data = {
        "title": "Purple Hibiscus",
        "author": "Chimamanda Adichie",
        "publisher": "Algonquin Books",
        "category": "Fiction",
        "available": True
    }
    response = client.post("/books", json=book_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["title"] == book_data["title"]

def test_list_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book():
    book_data = {
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "publisher": "Penguin Books",
        "category": "Classic",
        "available": True
    }
    add_response = client.post("/books", json=book_data)
    book_id = add_response.json()["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]

def test_filter_books():
    response = client.get("/books/filter", params={"publisher": "Penguin Books"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    user_data = {
        "firstname": "motunrayo",
        "lastname": "koye",
        "email": "motune@koye.com"
    }
    response = client.post("/users", json=user_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["firstname"] == user_data["firstname"]

def test_create_loan():
    book_data = {
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "publisher": "Heinemann",
        "category": "Fiction",
        "available": True
    }
    book_response = client.post("/books", json=book_data)
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    user_data = {
        "firstname": "Koyejo",
        "lastname": "Catalog",
        "email": f"motune+{uuid.uuid4().hex}@koyejo.com"
    }
    user_response = client.post("/users", json=user_data)
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    loan_data = {
        "user_id": user_id,
        "book_id": book_id,
        "days": 7
    }
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 201

