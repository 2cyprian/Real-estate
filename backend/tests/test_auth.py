import pytest
import time
import random
from fastapi.testclient import TestClient
from app.main import app


# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def client():
    return TestClient(app)


# -------------------------
# Helper functions
# -------------------------
def make_user_payload(suffix: str = ""):
    """Generate a unique user payload with optional suffix."""
    timestamp = int(time.time() * 1000)
    random_digits = ''.join(random.choices('0123456789', k=7))
    return {
        "email": f"user{suffix}{timestamp}@makaziplus.com",
        "password": "SecurePass123!",
        "first_name": f"User{suffix}",
        "last_name": f"Test{suffix}",
        "phone_number": f"067{random_digits}"
    }


def register_user(client: TestClient, user_data: dict):
    return client.post("/auth/register", json=user_data)


def login_user(client: TestClient, email: str, password: str):
    return client.post(
        "/auth/token",
        data={"email": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


# -------------------------
# Tests
# -------------------------
def test_create_user(client: TestClient):
    user = make_user_payload("create")
    response = register_user(client, user)

    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}


def test_register_duplicate_email(client: TestClient):
    user = make_user_payload("dup")
    register_user(client, user)

    # Try to register same email again
    response = register_user(client, user)
    assert response.status_code == 400
    assert "already registered" in response.json().get("detail", "")


def test_login_for_access_token(client: TestClient):
    user = make_user_payload("login")
    register_user(client, user)

    response = login_user(client, user["email"], user["password"])

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    user = make_user_payload("wrongpass")
    register_user(client, user)

    response = login_user(client, user["email"], "WrongPass123!")

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json().get("detail", "")


def test_read_users_me_unauthorized(client: TestClient):
    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_users_me(client: TestClient):
    user = make_user_payload("me")
    register_user(client, user)

    login_response = login_user(client, user["email"], user["password"])
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user["email"]
    assert "id" in data  # user object should include ID
    assert "first_name" in data
