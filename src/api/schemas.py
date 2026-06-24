"""Schemas Pydantic para API (em Português).

Define modelos de requisição e resposta utilizados pela API REST, como
`PredictionRequest`, `PredictionResponse` e `HealthResponse`.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    """Esquema de requisição para o endpoint de predição.

    Contém os campos esperados pela API para solicitar uma previsão de churn.
    """
    
    age: int = Field(..., ge=0, le=150, description="Idade do cliente")
    tenure: int = Field(..., ge=0, le=72, description="Meses como cliente")
    monthly_charges: float = Field(..., gt=0, description="Cobrança mensal")
    total_charges: float = Field(..., ge=0, description="Cobrança total")
    gender: str = Field(..., description="Gênero: Male/Female")
    partner: str = Field(..., description="Parceiro: Yes/No")
    dependents: str = Field(..., description="Dependentes: Yes/No")
    phone_service: str = Field(..., description="Serviço de telefone: Yes/No")
    internet_service: str = Field(..., description="Internet: DSL/Fiber optic/No")
    online_security: str = Field(..., description="Online security: Yes/No/No internet service")
    online_backup: str = Field(..., description="Online backup: Yes/No/No internet service")
    device_protection: str = Field(..., description="Proteção de dispositivo: Yes/No/No internet service")
    tech_support: str = Field(..., description="Suporte técnico: Yes/No/No internet service")
    streaming_tv: str = Field(..., description="Streaming TV: Yes/No/No internet service")
    streaming_movies: str = Field(..., description="Streaming Movies: Yes/No/No internet service")
    contract: str = Field(..., description="Tipo de contrato")
    paperless_billing: str = Field(..., description="Fatura sem papel: Yes/No")
    payment_method: str = Field(..., description="Método de pagamento")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Esquema de resposta do endpoint de predição.

    Retorna a classe prevista, probabilidade e versão do modelo.
    """

    prediction: int = Field(..., description="Classe prevista (0 ou 1)")
    probability: float = Field(..., ge=0, le=1, description="Probabilidade de churn")
    model_version: str = Field(..., description="Versão do modelo")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1,
                "probability": 0.75,
                "model_version": "0.1.0",
            }
        }


class HealthResponse(BaseModel):
    """Esquema de resposta para verificação de saúde da API."""

    status: str = Field(..., description="Status de saúde")
    model_version: str = Field(..., description="Versão do modelo")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_version": "0.1.0",
            }
        }
