# backend/logging_config.py --- Configuração do Sistema de Logging
import logging
import logging.config
import json
from datetime import datetime
from pathlib import Path
import sys

class JSONFormatter(logging.Formatter):
    """Formata logs em JSON"""
    
    def format(self, record: logging.LogRecord) -> str:

        # Cria um dicionário com as informações do log
         # Data/hora em UTC
         # INFO, ERROR, WARNING
         # Nome do logger (ex: "backend")
         # Mensagem do log
         # Módulo onde ocorreu
         # Função onde ocorreu
         # Linha do código

        log_object = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if hasattr(record, 'extra_fields'):
            log_object.update(record.extra_fields)
        
        # Adiciona informações de exceção se houver
        if record.exc_info:
            log_object['exception'] = self.formatException(record.exc_info)
        
        # Converte para JSON string
        return json.dumps(log_object, ensure_ascii=False)

def setup_logging():
    """Configura o sistema de logging"""
    
    # Cria diretório de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True) 
    
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False, # Não desativa loggers existentes
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        # 4. HANDLERS - Onde os logs serão enviados
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": "logs/app.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "json",
                "filename": "logs/error.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf8",
            }
        },
        # 5. LOGGERS - Quem emite os logs
        "loggers": {
            "": {  # Root logger
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "backend": {
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "watchfiles": {
                "level": "WARNING",  # Muda de INFO para WARNING
                "handlers": ["console", "file"],
                "propagate": False
            },
        }
    }
    
    # 6. Aplica a configuração
    logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str = "backend") -> logging.Logger:
    """Retorna um logger configurado"""
    return logging.getLogger(name)