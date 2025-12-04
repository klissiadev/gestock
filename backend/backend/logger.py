# backend/logger.py
import logging
from typing import Any, Dict, Optional
import time
import traceback

class AppLogger:
    """Logger principal da aplicação - NOSSA INTERFACE"""
    
    def __init__(self, logger_name: str = "backend"):
        # Obtém o logger configurado no logging_config.py
        self.logger = logging.getLogger(logger_name)
    
    # MÉTODO 1: Log de Requests (entrada)
    def log_request(
        self,
        request_id: str,        
        method: str,           
        url: str,              
        client_ip: str,       
        user_agent: Optional[str] = None,  
        headers: Optional[Dict] = None    
    ):
        """Log de entrada de request - CHAMADO PELO MIDDLEWARE"""
        # Cria dicionário com informações estruturadas
        extra_fields = {
            "request_id": request_id,
            "event_type": "request",  # Tipo de evento
            "method": method,
            "url": url,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "headers": self._sanitize_headers(headers) if headers else None
        }
        
        # Envia para o sistema de logging
        self.logger.info(
            f"Request recebido: {method} {url}",  
            extra={'extra_fields': extra_fields}   
        )
    
    # MÉTODO 2: Log de Responses (saída)
    def log_response(
        self,
        request_id: str,
        method: str,
        url: str,
        status_code: int,      
        duration_ms: float     
    ):
        """Log de saída de response - CHAMADO PELO MIDDLEWARE"""
        extra_fields = {
            "request_id": request_id,
            "event_type": "response",
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 2) 
        }
        
        # Define nível baseado no status code
        log_level = logging.INFO if status_code < 400 else logging.WARNING
        
        self.logger.log(
            log_level,
            f"Response enviado: {method} {url} - {status_code} ({duration_ms}ms)",
            extra={'extra_fields': extra_fields}
        )
    
    # MÉTODO 3: Log de Erros
    def log_error(
        self,
        request_id: str,
        method: str,
        url: str,
        error: Exception,      # Objeto da exceção
        status_code: int = 500
    ):
        """Log detalhado de erros - CHAMADO PELO EXCEPTION HANDLER"""
        extra_fields = {
            "request_id": request_id,
            "event_type": "error",
            "method": method,
            "url": url,
            "status_code": status_code,
            "error_type": type(error).__name__,  
            "error_message": str(error)         
        }
        
        # exc_info=True captura o traceback completo
        self.logger.error(
            f"Erro: {method} {url} - {type(error).__name__}",
            extra={'extra_fields': extra_fields},
            exc_info=True
        )
    
    # MÉTODO 4: Log de Informações (uso geral)
    def log_info(self, message: str, extra_data: Dict = None):
        """Log de informações gerais - USADO NAS ROTAS"""
        extra_fields = extra_data if extra_data else {}
        self.logger.info(
            message,
            extra={'extra_fields': extra_fields}
        )
    
    # MÉTODO 5: Log de Alertas
    def log_warning(self, message: str, extra_data: Dict = None):
        """Log de alertas - USADO NAS ROTAS"""
        extra_fields = extra_data if extra_data else {}
        self.logger.warning(
            message,
            extra={'extra_fields': extra_fields}
        )
    
    # MÉTODO PRIVADO: Proteção de dados sensíveis
    def _sanitize_headers(self, headers: Dict) -> Dict:
        """Remove informações sensíveis dos headers - SEGURANÇA"""
        sensitive_keys = ['authorization', 'cookie', 'api-key', 'token', 'senha', 'password']
        sanitized = {}
        for key, value in headers.items():
            # Verifica se a chave contém informação sensível
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = '***REDACTED***'  # Mascara o valor
            else:
                sanitized[key] = value
        return sanitized

# Instância global do logger - USADA EM TODA APLICAÇÃO
logger = AppLogger()