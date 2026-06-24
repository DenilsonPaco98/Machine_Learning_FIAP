"""Utilities de logging (em Português).

Fornece a função `setup_logger()` para configurar logging com handlers
para arquivo e console. Evita o uso de print() no código e centraliza
a configuração de logs do projeto.
"""

import logging
import sys
from pathlib import Path

from src.config import LOG_FILE, LOG_FORMAT, LOG_LEVEL


def setup_logger(name: str) -> logging.Logger:
    """
    Configura o logger com manipuladores de arquivo e console.
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        Instância do logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Evita manipuladores duplicados
    if logger.handlers:
        return logger
    
    # Manipulador de arquivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Manipulador de console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Formato
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adiciona manipuladores
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
