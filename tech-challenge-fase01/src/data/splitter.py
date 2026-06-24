"""Funções para divisão de dados (em Português).

Fornece utilitários para splits estratificados de treino/val/test e para
criação de folds estratificados para cross-validation.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold

from src.config import RANDOM_STATE, TEST_SIZE, VAL_SIZE
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple:
    """
    Divide os dados em conjuntos de treino e teste.
    
    Args:
        X: Dataframe de características
        y: Série alvo
        test_size: Proporção do conjunto de teste
        random_state: Semente aleatória
        
    Returns:
        Tupla de (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    
    logger.info(
        f"Divisão Treino/Teste: {len(X_train)}/{len(X_test)} "
        f"(proporção: {len(X_train)/(len(X_train)+len(X_test)):.2%})"
    )
    
    return X_train, X_test, y_train, y_test


def split_train_val(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    val_size: float = VAL_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple:
    """
    Divide os dados de treino em conjuntos de treino e validação.
    
    Args:
        X_train: Características de treino
        y_train: Alvo de treino
        val_size: Proporção do conjunto de validação
        random_state: Semente aleatória
        
    Returns:
        Tupla de (X_train, X_val, y_train, y_val)
    """
    X_train, X_val, y_train, y_val = train_test_split(
        X_train,
        y_train,
        test_size=val_size,
        random_state=random_state,
        stratify=y_train,
    )
    
    logger.info(
        f"Divisão Treino/Validação: {len(X_train)}/{len(X_val)} "
        f"(proporção: {len(X_train)/(len(X_train)+len(X_val)):.2%})"
    )
    
    return X_train, X_val, y_train, y_val


def create_stratified_folds(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    random_state: int = RANDOM_STATE,
) -> list:
    """
    Cria divisões estratificadas para k-folds.
    
    Args:
        X: Dataframe de características
        y: Série alvo
        n_splits: Número de folds
        random_state: Semente aleatória
        
    Returns:
        Lista de tuplas (índices_treino, índices_teste)
    """
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    folds = []
    
    for train_idx, test_idx in skf.split(X, y):
        folds.append((train_idx, test_idx))
    
    logger.info(f"Criados {n_splits} folds estratificados para cross-validation")
    
    return folds
