"""Middlewares da API (em Português).

Inclui uma middleware para logar tempo de resposta e headers relevantes
para monitoramento leve de performance por requisição.
"""

import time
from fastapi import Request
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def log_request_middleware(request: Request, call_next):
    """Registra detalhes da requisição e latência."""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Latência: {process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response
