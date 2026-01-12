import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.database.connection import get_db
from src.models.user import User
from src.models.task import Task
from src.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
from src.database.connection import Base
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_task():
    # First, register a user and get a token
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "taskuser@example.com",
            "password": "testpassword",
            "name": "Task User"
        }
    )
    assert signup_response.status_code == 200

    # Login to get token
    login_response = client.post(
        "/auth/signin",
        json={
            "email": "taskuser@example.com",
            "password": "testpassword"
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["token"]

    # Create a task with the token
    response = client.post(
        "/todos",
        json={
            "title": "Test Task",
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["is_completed"] == False

def test_get_tasks():
    # First, register a user and get a token
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "gettasks@example.com",
            "password": "testpassword",
            "name": "Get Tasks User"
        }
    )
    assert signup_response.status_code == 200

    # Login to get token
    login_response = client.post(
        "/auth/signin",
        json={
            "email": "gettasks@example.com",
            "password": "testpassword"
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["token"]

    # Get tasks (should be empty initially)
    response = client.get(
        "/todos",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []
    assert data["total_count"] == 0