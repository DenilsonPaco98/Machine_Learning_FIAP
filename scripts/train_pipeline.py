"""Pipeline de treinamento completo (em Português).

Script que orquestra carregamento de dados, pré-processamento, seleção
de features, treino de baselines e MLP, avaliação final e salvamento de
artefatos (modelo, preprocessor). Integração com MLflow incluída.
"""

import os
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import mlflow
import mlflow.pytorch

from src.config import (
    SEED,
    RANDOM_STATE,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    DATASET_NAME,
    TARGET_COLUMN,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    DROP_FEATURES,
    HIDDEN_DIMS,
    BATCH_SIZE,
    LEARNING_RATE,
    EPOCHS,
    EARLY_STOPPING_PATIENCE,
    WEIGHT_DECAY,
    MLFLOW_TRACKING_URI,
    EXPERIMENT_NAME,
)
from src.data.preprocess import load_data, DataPreprocessor
from src.data.splitter import split_train_test, split_train_val
from src.features.build_features import get_feature_importance
from src.models.mlp import MLPClassifier
from src.models.baseline import DummyBaseline, LogisticBaseline
from src.models.trainer import Trainer
from src.utils.logger import setup_logger
from src.utils.metrics import calculate_metrics

# Setup logger
logger = setup_logger(__name__)

# Set random seeds
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)


def main():
    """Pipeline de treinamento principal (em Português).

    Orquestra o carregamento de dados, pré-processamento, seleção de
    features, treino de modelos baseline e MLP, avaliação e salvamento
    de artefatos. Integra com o MLflow para rastreamento de experiências.
    """
    
    # Set MLflow tracking
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    logger.info("=" * 80)
    logger.info("INICIANDO O PIPELINE DE TREINAMENTO DE CHURN PREDICTION")
    logger.info("=" * 80)
    
    # 1. Load data
    logger.info("\n1. CARREGANDO DADOS")
    logger.info("-" * 80)
    
    data_path = RAW_DATA_DIR / DATASET_NAME
    
    if not data_path.exists():
        logger.error(f"Conjunto de dados não encontrado em {data_path}")
        logger.info("Por favor, baixe o conjunto de dados Telco Customer Churn em:")
        logger.info("https://www.kaggle.com/blastchar/telco-customer-churn")
        logger.info(f"E coloque-o em: {data_path}")
        raise FileNotFoundError(f"Conjunto de dados não encontrado: {data_path}")
    
    df = load_data(str(data_path))
    logger.info(f"Formato do conjunto de dados: {df.shape}")
    logger.info(f"Colunas: {df.columns.tolist()}")
    
    # 2. Prepare features and target
    logger.info("\n2. PREPARANDO FEATURES E TARGET")
    logger.info("-" * 80)
    
    # Drop unnecessary columns
    columns_to_drop = [col for col in DROP_FEATURES if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        logger.info(f"Colunas removidas: {columns_to_drop}")
    
    # Convert target to binary
    if TARGET_COLUMN in df.columns:
        y = (df[TARGET_COLUMN] == "Yes").astype(int)
        X = df.drop(columns=[TARGET_COLUMN])
    else:
        raise ValueError(f"Coluna alvo '{TARGET_COLUMN}' não encontrada no conjunto de dados")
    
    # Filter features that exist in data
    numerical_features = [f for f in NUMERICAL_FEATURES if f in X.columns]
    categorical_features = [f for f in CATEGORICAL_FEATURES if f in X.columns]
    
    logger.info(f"Features numéricas ({len(numerical_features)}): {numerical_features}")
    logger.info(f"Features categóricas ({len(categorical_features)}): {categorical_features}")
    logger.info(f"Distribuição da variável alvo:\n{y.value_counts()}")
    
    # 3. Train-test split
    logger.info("\n3. DIVIDINDO OS DADOS")
    logger.info("-" * 80)
    
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    X_train, X_val, y_train, y_val = split_train_val(X_train, y_train)
    
    logger.info(f"Conjunto de treino: {X_train.shape}")
    logger.info(f"Conjunto de validação: {X_val.shape}")
    logger.info(f"Conjunto de teste: {X_test.shape}")
    
    # 4. Preprocessing
    logger.info("\n4. PRÉ-PROCESSANDO OS DADOS")
    logger.info("-" * 80)
    
    preprocessor = DataPreprocessor(numerical_features, categorical_features)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_val_processed = preprocessor.transform(X_val)
    X_test_processed = preprocessor.transform(X_test)
    
    logger.info(f"Formato do conjunto de treino após pré-processamento: {X_train_processed.shape}")
    
    # Save preprocessor
    with open(PROCESSED_DATA_DIR / "preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)
    logger.info("Pré-processador salvo")
    
    # 5. Feature importance
    logger.info("\n5. Analisando a Importância das Features")
    logger.info("-" * 80)
    
    feature_importance = get_feature_importance(X_train_processed, y_train, top_n=10)
    feature_columns = list(feature_importance.keys())
    
    # Save feature columns
    with open(PROCESSED_DATA_DIR / "feature_columns.pkl", "wb") as f:
        pickle.dump(feature_columns, f)
    logger.info(f"Top features salvas: {feature_columns}")
    
    # Select top features
    X_train_feat = X_train_processed[feature_columns]
    X_val_feat = X_val_processed[feature_columns]
    X_test_feat = X_test_processed[feature_columns]
    
    # 6. Train baseline models
    logger.info("\n6. TREINANDO MODELOS BASELINE")
    logger.info("-" * 80)
    
    with mlflow.start_run(run_name="baseline_dummy"):
        dummy = DummyBaseline(strategy="most_frequent")
        dummy.fit(X_train_feat, y_train)
        
        y_pred_dummy = dummy.predict(X_test_feat)
        metrics_dummy = calculate_metrics(y_test, y_pred_dummy)
        
        logger.info(f"Classificador Dummy - Acurácia: {metrics_dummy['accuracy']:.4f}")
        
        mlflow.log_metrics({"dummy_" + k: v for k, v in metrics_dummy.items()})
    
    with mlflow.start_run(run_name="baseline_logistic"):
        logistic = LogisticBaseline()
        logistic.fit(X_train_feat, y_train)
        
        y_pred_lr = logistic.predict(X_test_feat)
        y_proba_lr = logistic.predict_proba(X_test_feat)
        metrics_lr = calculate_metrics(y_test, y_pred_lr, y_proba_lr)
        
        logger.info(f"Regressão Logística - Acurácia: {metrics_lr['accuracy']:.4f}")
        logger.info(f"Regressão Logística - ROC-AUC: {metrics_lr.get('roc_auc', 'N/A'):.4f}")
        
        mlflow.log_metrics({"lr_" + k: v for k, v in metrics_lr.items()})
    
    # 7. Train MLP model
    logger.info("\n7. TREINANDO O MODELO MLP")
    logger.info("-" * 80)
    
    with mlflow.start_run(run_name="mlp_model"):
        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train_feat.values)
        y_train_tensor = torch.FloatTensor(y_train.values)
        X_val_tensor = torch.FloatTensor(X_val_feat.values)
        y_val_tensor = torch.FloatTensor(y_val.values)
        X_test_tensor = torch.FloatTensor(X_test_feat.values)
        y_test_tensor = torch.FloatTensor(y_test.values)
        
        # Create data loaders
        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
        
        train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
        
        # Initialize model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Usando dispositivo: {device}")
        
        input_size = X_train_feat.shape[1]
        classifier = MLPClassifier(
            input_size=input_size,
            hidden_dims=HIDDEN_DIMS,
            learning_rate=LEARNING_RATE,
            device=device,
        )
        
        # Log hyperparameters
        mlflow.log_params({
            "input_size": input_size,
            "hidden_dims": str(HIDDEN_DIMS),
            "batch_size": BATCH_SIZE,
            "learning_rate": LEARNING_RATE,
            "epochs": EPOCHS,
            "early_stopping_patience": EARLY_STOPPING_PATIENCE,
            "weight_decay": WEIGHT_DECAY,
        })
        
        # Train
        trainer = Trainer(
            model=classifier.model,
            optimizer=classifier.optimizer,
            criterion=classifier.criterion,
            device=device,
            early_stopping_patience=EARLY_STOPPING_PATIENCE,
        )
        
        trainer.fit(train_loader, val_loader, epochs=EPOCHS)
        
        # Log training history
        for epoch, loss in enumerate(trainer.history["train_loss"]):
            mlflow.log_metric("train_loss", loss, step=epoch)
            mlflow.log_metric("val_loss", trainer.history["val_loss"][epoch], step=epoch)
        
        # Evaluate on test set
        logger.info("\n8. AVALIANDO O MODELO NO CONJUNTO DE TESTE")
        logger.info("-" * 80)
        
        classifier.model.eval()
        with torch.no_grad():
            y_pred_proba = classifier.predict_proba(X_test_tensor).numpy().flatten()
            y_pred = (y_pred_proba > 0.5).astype(int)
        
        metrics_mlp = calculate_metrics(y_test.values, y_pred, y_pred_proba)
        
        logger.info(f"MLP - Acurácia: {metrics_mlp['accuracy']:.4f}")
        logger.info(f"MLP - Precisão: {metrics_mlp['precision']:.4f}")
        logger.info(f"MLP - Revocação: {metrics_mlp['recall']:.4f}")
        logger.info(f"MLP - F1: {metrics_mlp['f1']:.4f}")
        logger.info(f"MLP - ROC-AUC: {metrics_mlp.get('roc_auc', 'N/A'):.4f}")
        
        mlflow.log_metrics({
            "test_accuracy": metrics_mlp["accuracy"],
            "test_precision": metrics_mlp["precision"],
            "test_recall": metrics_mlp["recall"],
            "test_f1": metrics_mlp["f1"],
            "test_roc_auc": metrics_mlp.get("roc_auc", 0.0),
        })
        
        # Save model
        logger.info("\n9. SALVANDO O MODELO")
        logger.info("-" * 80)
        
        model_path = MODELS_DIR / "mlp_model.pth"
        classifier.save(str(model_path))
        logger.info(f"Modelo salvo em {model_path}")
        
        mlflow.pytorch.log_model(classifier.model, "model")
    
    logger.info("\n" + "=" * 80)
    logger.info("PIPELINE DE TREINAMENTO COMPLETADA COM SUCESSO")
    logger.info("=" * 80)
    logger.info(f"Modelo salvo em: {MODELS_DIR / 'mlp_model.pth'}")
    logger.info(f"Pré-processador salvo em: {PROCESSED_DATA_DIR / 'preprocessor.pkl'}")
    logger.info(f"Rastreamento MLflow em: {MLFLOW_TRACKING_URI}")
    logger.info("\nExecute 'mlflow ui' para visualizar experiências")
    logger.info("Execute 'make run-api' para iniciar o servidor da API")


if __name__ == "__main__":
    main()
