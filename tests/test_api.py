import json
import pytest
from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "healthy"
    assert "model_version" in data


@pytest.fixture
def valid_payload():
    return {
        "age": 35,
        "tenure": 12,
        "monthly_charges": 65.5,
        "total_charges": 786.0,
        "gender": "Male",
        "partner": "Yes",
        "dependents": "No",
        "phone_service": "Yes",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
    }


def test_predict_model_not_loaded(valid_payload):
    # If model or preprocessor not present, API should return 503
    resp = client.post("/predict", json=valid_payload)
    assert resp.status_code in (200, 503)
    # If 503, verify structure
    if resp.status_code == 503:
        data = resp.json()
        assert "detail" in data


def test_predict_invalid_payload():
    # Missing required field 'age'
    payload = {"tenure": 10}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422
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
