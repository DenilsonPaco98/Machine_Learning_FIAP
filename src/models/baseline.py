"""Modelos baseline (em Português).

Contém implementações simples de referência como `DummyBaseline` e
`LogisticBaseline` para comparação com o modelo principal.
"""

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression

from src.config import RANDOM_STATE
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DummyBaseline:
    """Dummy baseline classifier (em Português)."""
    
    def __init__(self, strategy: str = "most_frequent"):
        """
        Inicializa o classificador dummy.
        
        Args:
            strategy: Estratégia para o classificador dummy
        """
        self.model = DummyClassifier(strategy=strategy)
        logger.info(f"Classificador dummy inicializado com a estratégia: {strategy}")
        
    def fit(self, X, y):
        """Ajusta o modelo."""
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        """Faz previsões."""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Obtém as probabilidades das previsões."""
        return self.model.predict_proba(X)
    
    def score(self, X, y):
        """Obtém a pontuação do modelo."""
        return self.model.score(X, y)


class LogisticBaseline:
    """Logistic Regression baseline (em Português)."""
    
    def __init__(self, max_iter: int = 1000, random_state: int = RANDOM_STATE):
        """
        Inicializa a regressão logística.
        
        Args:
            max_iter: Máximo de iterações
            random_state: Semente aleatória
        """
        self.model = LogisticRegression(
            max_iter=max_iter,
            random_state=random_state,
            verbose=0,
        )
        logger.info("Regressão Logística baseline inicializada")
        
    def fit(self, X, y):
        """Ajusta o modelo."""
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        """Faz previsões."""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Obtém as probabilidades das previsões."""
        proba = self.model.predict_proba(X)
        # Retorna a probabilidade da classe positiva
        return proba[:, 1]
    
    def score(self, X, y):
        """Obtém a pontuação do modelo."""
        return self.model.score(X, y)
