import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.fast_api import app, get_db, Base, Book

DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_book(client):
    response = client.post("/books/", data={
        "title": "Test Book",
        "author": "Test Author",
        "author_key": "test_key",
        "ebook_access": "free",
        "publish_year": 2022
    })
    assert response.status_code == 200

def test_read_books(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Test Book" in response.text

def test_read_book(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert "Test Book" in response.text

def test_delete_book(client):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    response = client.get("/books/1")
    assert response.status_code == 404

def test_create_second_book(client):
    response = client.post("/books/", data={
        "title": "Another Test Book",
        "author": "Another Test Author",
        "author_key": "another_test_key",
        "ebook_access": "free",
        "publish_year": 2023
    })
    assert response.status_code == 200

def test_read_second_book(client):
    response = client.get("/books/2")
    assert response.status_code == 200
    assert "Another Test Book" in response.text

def test_update_second_book(client):
    response = client.post("/books/2", json={
        "title": "Updated Another Book",
        "author": "Updated Another Author",
        "author_key": "updated_another_key",
        "ebook_access": "free",
        "publish_year": 2023
    })
    assert response.status_code == 200

def test_delete_second_book(client):
    response = client.delete("/books/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    response = client.get("/books/2")
    assert response.status_code == 404
