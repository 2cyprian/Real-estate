from fastapi.testclient import TestClient
import pytest
from app.main import app

from db.base import Base
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

# Assuming 'app' is your FastAPI application instance
# and 'client' is a fixture from conftest.py that provides a TestClient
# configured with a test database.

def test_create_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@makaziplus.com",
            "password":"makazi1234",
            "first_name": "test",
            "last_name": "makazi",
            "phone_number": "067654321"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data == {"message": "User created successfully"}


def test_login_for_access_token(client: TestClient):
    # First, create a user to log in with
    client.post(
        "/auth/register",
        json={
            "email": "login@makazi.com",
            "password": "makazi1234",
            "first_name": "login",
            "last_name": "user",
            "phone_number": "0987654321"
        },
    )

    response = client.post(
        "/auth/token",
        data={
            "email": "login@makazi.com",  # Changed from "username" to "email"
            "password": "makazi1234"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client: TestClient):
    # First create a user
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@makazi.com",
            "password": "makazi1234",
            "first_name": "test",
            "last_name": "duplicate",
            "phone_number": "1234567890"
        },
    )
    
    # Try to create same user again
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@makazi.com",
            "password": "makazi1234",
            "first_name": "test",
            "last_name": "duplicate",
            "phone_number": "1234567890"
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json().get("detail", "")


def test_login_wrong_password(client: TestClient):
    # Create a user first
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@makazi.com",
            "password": "correct123",
            "first_name": "test",
            "last_name": "wrongpass",
            "phone_number": "0987654321"
        },
    )
    
    # Try to login with wrong password
    response = client.post(
        "/auth/token",
        data={
            "email": "wrongpass@makazi.com",
            "password": "wrongpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json().get("detail", "")


def test_read_users_me_unauthorized(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_users_me(client: TestClient):
    # Register a user
    register_response = client.post(
        "/auth/register",
        json={
            "email": "me@makazi.com",
            "password": "makazi1234",
            "first_name": "test",
            "last_name": "me",
            "phone_number": "1122334455"
        },
    )
    assert register_response.status_code == 201

    # Log in the user to get a token
    login_response = client.post(
        "/auth/token",
        data={
            "email": "me@makazi.com",
            "password": "makazi1234"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Call the /users/me endpoint with the token
    me_response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert me_response.status_code == 200
    assert me_response.json() == {"email": "me@makazi.com"}