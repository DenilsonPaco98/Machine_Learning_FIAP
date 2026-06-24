"""Testes de validação de schemas (em Português).

Verifica regras de validação dos modelos Pydantic usados pela API.
"""

import pytest
from pydantic import ValidationError

from src.api.schemas import PredictionRequest, PredictionResponse, HealthResponse


def test_health_response_valid():
    """Valida objeto HealthResponse válido"""
    response = HealthResponse(status="healthy", model_version="0.1.0")
    assert response.status == "healthy"
    assert response.model_version == "0.1.0"


def test_prediction_response_valid():
    """Valida objeto PredictionResponse válido"""
    response = PredictionResponse(
        prediction=1,
        probability=0.75,
        model_version="0.1.0",
    )
    assert response.prediction == 1
    assert response.probability == 0.75


def test_prediction_response_probability_bounds():
    """Valida limites da probabilidade em PredictionResponse"""
    # Válido
    PredictionResponse(prediction=0, probability=0.0, model_version="0.1.0")
    PredictionResponse(prediction=1, probability=1.0, model_version="0.1.0")
    
    # Inválido
    with pytest.raises(ValidationError):
        PredictionResponse(prediction=0, probability=-0.1, model_version="0.1.0")
    
    with pytest.raises(ValidationError):
        PredictionResponse(prediction=0, probability=1.1, model_version="0.1.0")


def test_prediction_request_valid():
    """Valida objeto PredictionRequest de exemplo"""
    request = PredictionRequest(
        age=35,
        tenure=12,
        monthly_charges=65.5,
        total_charges=786.0,
        gender="Male",
        partner="Yes",
        dependents="No",
        phone_service="Yes",
        internet_service="Fiber optic",
        online_security="No",
        online_backup="No",
        device_protection="No",
        tech_support="No",
        streaming_tv="No",
        streaming_movies="No",
        contract="Month-to-month",
        paperless_billing="Yes",
        payment_method="Electronic check",
    )
    assert request.age == 35
    assert request.tenure == 12


def test_prediction_request_age_bounds():
    """Test PredictionRequest age bounds"""
    # Valid
    PredictionRequest(
        age=0,
        tenure=0,
        monthly_charges=1.0,
        total_charges=0.0,
        gender="Male",
        partner="Yes",
        dependents="No",
        phone_service="Yes",
        internet_service="DSL",
        online_security="No",
        online_backup="No",
        device_protection="No",
        tech_support="No",
        streaming_tv="No",
        streaming_movies="No",
        contract="Month-to-month",
        paperless_billing="Yes",
        payment_method="Electronic check",
    )
    
    # Invalid - age too high
    with pytest.raises(ValidationError):
        PredictionRequest(
            age=151,
            tenure=0,
            monthly_charges=1.0,
            total_charges=0.0,
            gender="Male",
            partner="Yes",
            dependents="No",
            phone_service="Yes",
            internet_service="DSL",
            online_security="No",
            online_backup="No",
            device_protection="No",
            tech_support="No",
            streaming_tv="No",
            streaming_movies="No",
            contract="Month-to-month",
            paperless_billing="Yes",
            payment_method="Electronic check",
        )


def test_prediction_request_charges_positive():
    """Test PredictionRequest charges must be positive"""
    # Invalid - monthly charges zero
    with pytest.raises(ValidationError):
        PredictionRequest(
            age=35,
            tenure=12,
            monthly_charges=0.0,
            total_charges=0.0,
            gender="Male",
            partner="Yes",
            dependents="No",
            phone_service="Yes",
            internet_service="DSL",
            online_security="No",
            online_backup="No",
            device_protection="No",
            tech_support="No",
            streaming_tv="No",
            streaming_movies="No",
            contract="Month-to-month",
            paperless_billing="Yes",
            payment_method="Electronic check",
        )
