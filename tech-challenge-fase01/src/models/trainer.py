"""Loop de treinamento e utilitários (em Português).

Define `EarlyStopping` para parada antecipada baseada em perda de
validação e `Trainer` para gerir epochs, otimização, avaliação e logging
do processo de treino.
"""

import torch
import numpy as np
from typing import Tuple

from src.utils.logger import setup_logger
from src.utils.metrics import calculate_metrics

logger = setup_logger(__name__)


class EarlyStopping:
    """Early stopping callback (em Português)."""
    
    def __init__(self, patience: int = 10, min_delta: float = 0.0):
        """
        Inicializa a parada antecipada.
        
        Args:
            patience: Número de epochs sem melhoria para esperar
            min_delta: Mudança mínima para qualificar como melhoria
        """
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.stop = False
        
    def __call__(self, val_loss: float):
        """Verifica se o treinamento deve parar"""
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.stop = True
                logger.info(f"Parada antecipada acionada após {self.counter} epochs")


class Trainer:
    """Trainer para redes neurais (em Português)."""
    
    def __init__(
        self,
        model,
        optimizer,
        criterion,
        device: str = "cpu",
        early_stopping_patience: int = 10,
    ):
        """
        Inicializa o trainer.
        
        Args:
            model: Modelo PyTorch
            optimizer: Otimizador
            criterion: Função de perda
            device: Dispositivo a ser utilizado
            early_stopping_patience: Paciência para parada antecipada
        """
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.early_stopping = EarlyStopping(patience=early_stopping_patience)
        self.history = {
            "train_loss": [],
            "val_loss": [],
            "train_acc": [],
            "val_acc": [],
        }
        
    def train_epoch(self, train_loader) -> float:
        """Treina por uma epoch"""
        self.model.train()
        total_loss = 0.0
        
        for X_batch, y_batch in train_loader:
            X_batch = X_batch.to(self.device)
            y_batch = y_batch.to(self.device)
            
            self.optimizer.zero_grad()
            
            # Passagem para frente
            outputs = self.model(X_batch)
            loss = self.criterion(outputs.squeeze(), y_batch.float())
            
            # Passagem para trás
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def evaluate(self, val_loader) -> Tuple[float, float]:
        """Avalia no conjunto de validação"""
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_targets = []
        
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch = X_batch.to(self.device)
                y_batch = y_batch.to(self.device)
                
                outputs = self.model(X_batch)
                loss = self.criterion(outputs.squeeze(), y_batch.float())
                
                total_loss += loss.item()
                
                # Armazena as predições
                preds = (outputs.squeeze() > 0.5).cpu().numpy().astype(int)
                all_preds.extend(preds)
                all_targets.extend(y_batch.cpu().numpy())
        
        val_loss = total_loss / len(val_loader)
        val_acc = np.mean(np.array(all_preds) == np.array(all_targets))
        
        return val_loss, val_acc
    
    def fit(
        self,
        train_loader,
        val_loader,
        epochs: int = 100,
    ):
        """
        Treina o modelo.
        
        Args:
            train_loader: Data loader para os dados de treino
            val_loader: Data loader para os dados de validação
            epochs: Número de epochs
        """
        logger.info(f"Iniciando o treinamento por {epochs} epochs")
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_loss, val_acc = self.evaluate(val_loader)
            
            self.history["train_loss"].append(train_loss)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)
            
            if (epoch + 1) % 10 == 0:
                logger.info(
                    f"Epoch {epoch+1}/{epochs} - "
                    f"Loss Treino: {train_loss:.4f}, "
                    f"Loss Validação: {val_loss:.4f}, "
                    f"Acc Validação: {val_acc:.4f}"
                )
            
            # Parada antecipada
            self.early_stopping(val_loss)
            if self.early_stopping.stop:
                logger.info(f"Treinamento parado na epoch {epoch+1}")
                break
        
        logger.info("Treinamento concluído")
