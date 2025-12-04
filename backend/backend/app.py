from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# 1. IMPORTAÇÕES DO LOGGING
from backend.logging_config import setup_logging, get_logger
from backend.logging_middleware import LoggingMiddleware
from backend.logger import logger as app_logger

# 2. CONFIGURA LOGGING (uma única vez)
setup_logging()  # ⬅CHAVE: Configura todo o sistema
app_logger_instance = get_logger()

app = FastAPI(
    title="Backend API",
    description="API com sistema de logging",
    version="1.0.0"
)

# 3. ADICIONA MIDDLEWARE DE LOGGING
app.add_middleware(LoggingMiddleware)  # ⬅ CHAVE: Ativa logging automático

# 4. EXCEPTION HANDLERS (com logging)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções não tratadas"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Log do erro (usando nossa interface)
    app_logger.log_error(
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        error=exc
    )
    
    # Retorna resposta padronizada com request_id
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        },
        headers={"X-Request-ID": request_id}
    )

# 5. ROTAS (com logging contextual)
@app.get("/")
async def read_root(request: Request):
    """Endpoint raiz - EXEMPLO DE LOG EM ROTA"""
    app_logger.log_info("Endpoint root acessado", {
        "request_id": request.state.request_id,  # Contexto do request
        "endpoint": "/"
    })
    return {"message": "Backend API com logging"}

# 6. EVENTOS DE STARTUP/SHUTDOWN
@app.on_event("startup")
async def startup_event():
    app_logger.log_info("Aplicação iniciada", {
        "event": "startup",
        "app_name": "backend"
    })

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.log_info("Aplicação encerrada", {
        "event": "shutdown",
        "app_name": "backend"
    })