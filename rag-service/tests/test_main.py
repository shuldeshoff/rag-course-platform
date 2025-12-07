"""
Tests for main API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data

def test_ask_without_auth():
    response = client.post("/ask", json={
        "user_id": 1,
        "course_id": 1,
        "question": "Test question"
    })
    assert response.status_code == 403  # No auth

def test_ask_with_invalid_token():
    response = client.post(
        "/ask",
        json={"user_id": 1, "course_id": 1, "question": "Test"},
        headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401

