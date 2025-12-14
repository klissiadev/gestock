# backend/logging_middleware.py
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.logger import logger  # Importa nossa interface

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests e responses - CORAÇÃO DO SISTEMA"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 1. GERA REQUEST ID - Rastreabilidade
        request_id = str(uuid.uuid4())  # UUID único
        request.state.request_id = request_id  # Armazena no request
        
        # 2. CAPTURA INFORMAÇÕES DO REQUEST
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent")
        
        # 3. LOG DO REQUEST (ENTRADA)
        logger.log_request(
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=client_ip,
            user_agent=user_agent,
            headers=dict(request.headers)
        )
        
        # 4. PROCESSAMENTO DO REQUEST (com medição de tempo)
        start_time = time.time()  # Marca início
        
        try:
            # Chama o próximo middleware/rota
            response = await call_next(request)
            
            # Calcula tempo de processamento
            duration_ms = (time.time() - start_time) * 1000
            
            # 5. LOG DO RESPONSE (SAÍDA - SUCESSO)
            logger.log_response(
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration_ms=duration_ms
            )
            
            # 6. ADICIONA REQUEST_ID AO HEADER DA RESPOSTA
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # 7. LOG DO ERRO (SAÍDA - FALHA)
            duration_ms = (time.time() - start_time) * 1000
            
            logger.log_error(
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                error=e
            )
            
            raise