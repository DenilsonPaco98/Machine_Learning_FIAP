"""Módulo de configuração do projeto (em Português).

Contém constantes e caminhos usados por toda a aplicação, incluindo
parâmetros de treinamento, seeds, diretórios e listas de features.

Este arquivo é a fonte única de verdade para configurações.
"""

"""Configurações globais do projeto"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Reproducibility
SEED = 42
RANDOM_STATE = 42

# Data
DATASET_NAME = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
TARGET_COLUMN = "Churn"
TEST_SIZE = 0.2
VAL_SIZE = 0.1

# Model hyperparameters
HIDDEN_DIMS = [128, 64, 32]
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 100
EARLY_STOPPING_PATIENCE = 10
WEIGHT_DECAY = 1e-5

# API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 4

# MLflow
MLFLOW_TRACKING_URI = str(MLRUNS_DIR)
EXPERIMENT_NAME = "churn_prediction"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

# Features
NUMERICAL_FEATURES = [
    "age",
    "tenure",
    "monthly_charges",
    "total_charges",
]

CATEGORICAL_FEATURES = [
    "gender",
    "partner",
    "dependents",
    "phone_service",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
]

DROP_FEATURES = ["customer_id"]

# Metrics
METRICS_TO_TRACK = ["accuracy", "precision", "recall", "f1", "roc_auc"]
