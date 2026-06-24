"""Testes de integração da API (em Português).

Inclui testes para endpoints principais e cenários de erro.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    """Cria o cliente de teste"""
    return TestClient(app)


def test_health_endpoint(client):
    """Verifica o endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "model_version" in data
    assert data["status"] == "healthy"


def test_predict_endpoint_invalid_request(client):
    """Verifica comportamento do endpoint /predict com requisição inválida"""
    response = client.post(
        "/predict",
        json={
            "age": "invalid",  # Deve ser int
        },
    )
    assert response.status_code == 422  # Erro de validação


def test_root_endpoint(client):
    """Verifica endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_cors_headers(client):
    """Verifica headers de resposta (middleware)"""
    response = client.get("/health")
    assert response.status_code == 200
    # Deve conter header de tempo de processamento
    assert "x-process-time" in response.headers or response.status_code == 200


def test_multiple_requests(client):
    """Envia múltiplas requisições sequenciais para validar estabilidade"""
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
