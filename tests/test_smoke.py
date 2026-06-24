from fastapi.testclient import TestClient
from src.api.app import app


def test_app_starts():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data and "version" in data
"""Testes de smoke (em Português).

Verifica que a API inicia corretamente e que o endpoint /health responde.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    """Cria o cliente de teste"""
    return TestClient(app)


def test_api_startup(client):
    """Verifica se a API inicializa e responde no endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Verifica o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_health_endpoint_returns_json(client):
    """Garante que o endpoint /health retorne JSON válido"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_version" in data
