"""Aplicação FastAPI (em Português).

Define endpoints públicos como `/`, `/health` e `/predict`. No evento
`startup` carrega o modelo treinado e o preprocessor para servir previsões.
"""

import os
import pickle
import torch
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.base import BaseHTTPMiddleware

from src import __version__
from src.api.schemas import PredictionRequest, PredictionResponse, HealthResponse
from src.api.middlewares import log_request_middleware
from src.config import MODELS_DIR, PROCESSED_DATA_DIR
from src.models.mlp import MLPClassifier
from src.data.preprocess import DataPreprocessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="API para predição de churn de clientes",
    version=__version__,
)

# Add middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_middleware)

# Global variables for model
model = None
preprocessor = None
feature_columns = None
device = "cuda" if torch.cuda.is_available() else "cpu"


@app.on_event("startup")
async def load_model():
    """Carrega o modelo e artefatos na inicialização da aplicação."""
    global model, preprocessor, feature_columns
    
    try:
        logger.info("Carregando modelo...")
        
        # Load preprocessor
        preprocessor_path = PROCESSED_DATA_DIR / "preprocessor.pkl"
        if preprocessor_path.exists():
            with open(preprocessor_path, "rb") as f:
                preprocessor = pickle.load(f)
            logger.info("Pré-processador carregado")
        
        # Load feature columns
        columns_path = PROCESSED_DATA_DIR / "feature_columns.pkl"
        if columns_path.exists():
            with open(columns_path, "rb") as f:
                feature_columns = pickle.load(f)
            logger.info(f"Colunas de features carregadas: {len(feature_columns)} features")
        
        # Load MLP model
        model_path = MODELS_DIR / "mlp_model.pth"
        if model_path.exists():
            # Initialize classifier
            input_size = len(feature_columns) if feature_columns else 20
            hidden_dims = [128, 64, 32]
            model = MLPClassifier(
                input_size=input_size,
                hidden_dims=hidden_dims,
                device=device,
            )
            model.load(str(model_path))
            logger.info("Modelo MLP carregado")
        else:
            logger.warning("Arquivo de modelo não encontrado, executando em modo de demonstração")
            
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {str(e)}")
        raise


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de verificação de integridade da API."""
    return HealthResponse(
        status="healthy",
        model_version=__version__,
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Realiza predição de churn a partir da requisição enviada."""
    try:
        if model is None or preprocessor is None:
            raise HTTPException(
                status_code=503,
                detail="Modelo não carregado. Verifique se os arquivos do modelo existem.",
            )
        
        # Convert request to dataframe
        request_data = request.dict()
        X = pd.DataFrame([request_data])
        
        # Preprocess
        X_processed = preprocessor.transform(X)
        
        # Select features
        if feature_columns:
            X_processed = X_processed[feature_columns]
        
        # Convert to tensor
        X_tensor = torch.FloatTensor(X_processed.values)
        
        # Predict
        with torch.no_grad():
            prob = model.predict_proba(X_tensor).item()
            pred = int(prob > 0.5)
        
        logger.info(f"Predição realizada: {pred} (prob: {prob:.4f})")
        
        return PredictionResponse(
            prediction=pred,
            probability=round(prob, 4),
            model_version=__version__,
        )
        
    except Exception as e:
        logger.error(f"Erro na predição: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Endpoint root com metadados da API."""
    return {
        "message": "Churn Prediction API",
        "version": __version__,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
