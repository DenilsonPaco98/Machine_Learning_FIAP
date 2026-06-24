"""Engenharia de features (em Português).

Inclui a classe `FeatureBuilder` para seleção de features, criação de
interações e expansão polinomial, além de filtragem por variância.
"""

"""Feature engineering functions"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class FeatureBuilder:
    """Construtor e seletor de features para modelagem.

    Constrói e seleciona features relevantes usando técnicas estatísticas
    (por exemplo, SelectKBest). Fornece métodos para selecionar e transformar
    conjuntos de features.
    """
    
    def __init__(self, n_features: int = 10):
        self.n_features = n_features
        self.selector = None
        self.feature_names = None
        
    def select_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        k: int = None,
    ) -> pd.DataFrame:
        """
        Seleciona as K melhores features usando SelectKBest.

        Args:
            X: DataFrame de features
            y: Série alvo
            k: Número de features a selecionar

        Returns:
            DataFrame contendo apenas as features selecionadas
        """
        if k is None:
            k = self.n_features
        
        self.selector = SelectKBest(f_classif, k=k)
        X_selected = self.selector.fit_transform(X, y)
        
        # Obtém nomes das features selecionadas
        self.feature_names = X.columns[self.selector.get_support()].tolist()
        
        logger.info(f"Selecionadas {k} features: {self.feature_names}")
        
        return pd.DataFrame(X_selected, columns=self.feature_names, index=X.index)
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforma o DataFrame usando o seletor já ajustado."""
        if self.selector is None:
            raise ValueError("O seletor deve ser ajustado antes da transformação")
        
        X_selected = self.selector.transform(X)
        return pd.DataFrame(X_selected, columns=self.feature_names, index=X.index)


def create_interaction_features(X: pd.DataFrame, feature_pairs: list) -> pd.DataFrame:
    """
    Create interaction features.
    
    Args:
        X: Features dataframe
        feature_pairs: List of tuples (feature1, feature2) for interactions
        
    Returns:
        Dataframe with original and interaction features
    """
    X_copy = X.copy()
    
    for feat1, feat2 in feature_pairs:
        if feat1 in X.columns and feat2 in X.columns:
            interaction_name = f"{feat1}_x_{feat2}"
            X_copy[interaction_name] = X[feat1] * X[feat2]
            logger.info(f"Created interaction feature: {interaction_name}")
    
    return X_copy


def create_polynomial_features(X: pd.DataFrame, features: list, degree: int = 2) -> pd.DataFrame:
    """
    Create polynomial features.
    
    Args:
        X: Features dataframe
        features: List of feature names to create polynomials
        degree: Polynomial degree
        
    Returns:
        Dataframe with original and polynomial features
    """
    X_copy = X.copy()
    
    for feat in features:
        if feat in X.columns:
            for d in range(2, degree + 1):
                poly_name = f"{feat}_pow{d}"
                X_copy[poly_name] = X[feat] ** d
                logger.info(f"Created polynomial feature: {poly_name}")
    
    return X_copy


def remove_low_variance_features(X: pd.DataFrame, threshold: float = 0.01) -> pd.DataFrame:
    """
    Remove features with low variance.
    
    Args:
        X: Features dataframe
        threshold: Variance threshold
        
    Returns:
        Dataframe with low-variance features removed
    """
    variances = X.var()
    features_to_keep = variances[variances > threshold].index.tolist()
    
    removed_features = set(X.columns) - set(features_to_keep)
    if removed_features:
        logger.info(f"Removed {len(removed_features)} low-variance features: {removed_features}")
    
    return X[features_to_keep]


def get_feature_importance(
    X: pd.DataFrame,
    y: pd.Series,
    top_n: int = 10,
) -> dict:
    """
    Get feature importance scores.
    
    Args:
        X: Features dataframe
        y: Target series
        top_n: Number of top features to return
        
    Returns:
        Dictionary with feature importance scores
    """
    selector = SelectKBest(f_classif, k="all")
    selector.fit(X, y)
    
    scores = dict(zip(X.columns, selector.scores_))
    top_features = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    logger.info(f"Top {top_n} features by importance:")
    for feat, score in top_features:
        logger.info(f"  {feat}: {score:.4f}")
    
    return dict(top_features)
