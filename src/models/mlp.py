"""Implementação do MLP em PyTorch (em Português).

Define `MLPNet` (nn.Module) e `MLPClassifier` (wrapper) para treinar e
inferir com redes neurais feed-forward. Inclui funções para salvar e
carregar o modelo e previsões probabilísticas.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from src.config import RANDOM_STATE, SEED

# Set seeds
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)


class MLPNet(nn.Module):
    """Perceptron Multicamadas para classificação binária."""
    
    def __init__(self, input_size: int, hidden_dims: list, dropout: float = 0.2):
        """
        Inicializa a arquitetura MLP.

        Args:
            input_size: Dimensão das features de entrada
            hidden_dims: Lista com dimensões das camadas ocultas
            dropout: Probabilidade de dropout
        """
        super(MLPNet, self).__init__()
        
        self.layers = nn.ModuleList()
        
        # Input para primeira camada oculta
        self.layers.append(nn.Linear(input_size, hidden_dims[0]))
        
        # Camadas ocultas
        for i in range(len(hidden_dims) - 1):
            self.layers.append(nn.Linear(hidden_dims[i], hidden_dims[i + 1]))
        
        # Camada de saída
        self.layers.append(nn.Linear(hidden_dims[-1], 1))
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Passagem forward do modelo.

        Args:
            x: Tensor de entrada

        Returns:
            Tensor com probabilidades (sigmoid)
        """
        for i, layer in enumerate(self.layers[:-1]):
            x = layer(x)
            x = F.relu(x)
            x = self.dropout(x)
        
        # Camada de saída com sigmoid
        x = self.layers[-1](x)
        x = torch.sigmoid(x)
        
        return x


class MLPClassifier:
    """Wrapper do MLP com utilitários de treino e inferência."""
    
    def __init__(
        self,
        input_size: int,
        hidden_dims: list,
        learning_rate: float = 0.001,
        device: str = None,
    ):
        """
        Inicializa o classificador baseado em MLP.

        Args:
            input_size: Dimensão das features de entrada
            hidden_dims: Lista com dimensões das camadas ocultas
            learning_rate: Taxa de aprendizagem
            device: Dispositivo (cpu/cuda)
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = MLPNet(input_size, hidden_dims).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.BCELoss()
        
    def predict(self, X: torch.Tensor) -> torch.Tensor:
        """
        Realiza previsões (probabilidades) no tensor de entrada.

        Args:
            X: Tensor de entrada

        Returns:
            Tensor com probabilidades previstas
        """
        self.model.eval()
        with torch.no_grad():
            X = X.to(self.device)
            predictions = self.model(X)
        return predictions.cpu()
    
    def predict_proba(self, X: torch.Tensor) -> torch.Tensor:
        """
        Retorna as probabilidades previstas (método sinônimo para predict).

        Args:
            X: Tensor de entrada

        Returns:
            Tensor com probabilidades previstas
        """
        return self.predict(X)
    
    def save(self, filepath: str):
        """Salva os pesos do modelo no caminho informado."""
        torch.save(self.model.state_dict(), filepath)
    
    def load(self, filepath: str):
        """Carrega pesos do modelo a partir do caminho informado."""
        self.model.load_state_dict(torch.load(filepath, map_location=self.device))
