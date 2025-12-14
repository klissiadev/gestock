from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# =========================
# IMPORTS DOS ROUTERS
# =========================
from backend.routers.upload import router as upload_service
from backend.routers.mail_router import router as mail_service
from backend.routers.produto_router import router as produto_router
from backend.routers.movimentacao_router import router as movimentacao_router

# =========================
# IMPORTS DE LOGGING
# =========================
from backend.logging_config import setup_logging, get_logger
from backend.logging_middleware import LoggingMiddleware
from backend.logger import logger as app_logger

# =========================
# CONFIGURA LOGGING (1x)
# =========================
setup_logging()
app_logger_instance = get_logger()

# =========================
# CRIA A APLICAÇÃO
# =========================
app = FastAPI(
    title="Backend API",
    description="API com sistema de logging",
    version="1.0.0"
)

# =========================
# MIDDLEWARES
# =========================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging automático
app.add_middleware(LoggingMiddleware)

# =========================
# EXCEPTION HANDLER GLOBAL
# =========================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")

    app_logger.log_error(
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        error=exc
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        },
        headers={"X-Request-ID": request_id}
    )

# =========================
# ROTAS BÁSICAS
# =========================
@app.get("/")
async def read_root(request: Request):
    app_logger.log_info(
        "Endpoint root acessado",
        {
            "request_id": request.state.request_id,
            "endpoint": "/"
        }
    )
    return {"message": "Backend API com logging"}

# =========================
# REGISTRO DOS ROUTERS
# =========================
app.include_router(upload_service)
app.include_router(mail_service)
app.include_router(produto_router)
app.include_router(movimentacao_router)

# =========================
# EVENTOS DE CICLO DE VIDA
# =========================
@app.on_event("startup")
async def startup_event():
    app_logger.log_info(
        "Aplicação iniciada",
        {
            "event": "startup",
            "app_name": "backend"
        }
    )

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.log_info(
        "Aplicação encerrada",
        {
            "event": "shutdown",
            "app_name": "backend"
        }
    )
