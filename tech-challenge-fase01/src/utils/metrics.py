"""Funções utilitárias para cálculo de métricas (em Português).

Inclui funções como `calculate_metrics` e helpers para matrizes de confusão.
Usado para avaliar modelos em diferentes estágios do pipeline.
"""

from typing import Tuple

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
)


def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray = None,
) -> dict:
    """
    Calcular métricas de classificação.
    
    Args:
        y_true: Rótulos verdadeiros
        y_pred: Rótulos previstos
        y_proba: Probabilidades previstas (para ROC-AUC)
        
    Returns:
        Dicionário com métricas
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    
    if y_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
    
    return metrics


def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Obter valores da matriz de confusão.
    
    Args:
        y_true: Rótulos verdadeiros
        y_pred: Rótulos previstos
        
    Returns:
        Tupla de (tn, fp, fn, tp)
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp
