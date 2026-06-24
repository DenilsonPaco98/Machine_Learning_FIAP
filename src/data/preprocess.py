"""Pré-processamento de dados (em Português).

Contém a classe `DataPreprocessor` responsável por fit/transform de
features numéricas e categóricas, além de funções auxiliares para
carregar e preparar o dataset bruto.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataPreprocessor:
    """Pré-processador para dados de churn"""
    
    def __init__(self, numerical_features: list, categorical_features: list):
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
        self.scaler = StandardScaler()
        self.encoders = {}
        self.is_fitted = False
        
    def fit(self, X: pd.DataFrame) -> "DataPreprocessor":
        """Ajustar o pré-processador nos dados"""
        # Ajustar o scaler nas características numéricas
        if self.numerical_features:
            self.scaler.fit(X[self.numerical_features])
        
        # Ajustar os codificadores de rótulo nas características categóricas
        for col in self.categorical_features:
            self.encoders[col] = LabelEncoder()
            self.encoders[col].fit(X[col].astype(str))
        
        self.is_fitted = True
        logger.info("Pré-processador ajustado com sucesso")
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transformar dados usando o pré-processador ajustado"""
        if not self.is_fitted:
            raise ValueError("O pré-processador deve ser ajustado antes da transformação")
        
        X_copy = X.copy()
        
        # Escalar características numéricas
        if self.numerical_features:
            X_copy[self.numerical_features] = self.scaler.transform(
                X_copy[self.numerical_features]
            )
        
        # Codificar características categóricas
        for col in self.categorical_features:
            X_copy[col] = self.encoders[col].transform(X_copy[col].astype(str))
        
        return X_copy
        
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Ajustar e transformar dados"""
        return self.fit(X).transform(X)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Carregar e limpar dados de churn da telco.
    
    Args:
        filepath: Caminho para o arquivo CSV
        
    Returns:
        Dataframe limpo
    """
    df = pd.read_csv(filepath)
    logger.info(f"Dados carregados com formato {df.shape}")
    
    # Renomear colunas para minúsculas e substituir espaços por underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Tratar total_charges - converter para numérico, substituindo valores não numéricos por NaN
    if "total_charges" in df.columns:
        df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
        df["total_charges"].fillna(df["total_charges"].median(), inplace=True)
    
    # Remover linhas com valores ausentes na coluna alvo
    if "churn" in df.columns:
        df = df.dropna(subset=["churn"])
    
    logger.info(f"Dados limpos com formato {df.shape}")
    return df


def prepare_data(
    X: pd.DataFrame,
    y: pd.Series,
    numerical_features: list,
    categorical_features: list,
    fit_preprocessor: bool = False,
    preprocessor: DataPreprocessor = None,
) -> tuple:
    """
    Preparar dados para modelagem.
    
    Args:
        X: Dataframe de características
        y: Série alvo
        numerical_features: Lista de nomes de características numéricas
        categorical_features: Lista de nomes de características categóricas
        fit_preprocessor: Se deve ajustar o pré-processador
        preprocessor: Pré-processador existente a ser utilizado
        
    Returns:
        Tupla de (X_processado, y, pré-processador)
    """
    if fit_preprocessor:
        preprocessor = DataPreprocessor(numerical_features, categorical_features)
        X_processed = preprocessor.fit_transform(X)
    else:
        if preprocessor is None:
            raise ValueError("O pré-processador deve ser fornecido se não estiver ajustando")
        X_processed = preprocessor.transform(X)
    
    return X_processed, y, preprocessor
