#app.py
import os
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from backend.utils.env_loader import load_env_from_root
# =========================
# IMPORTS DOS ROUTERS
# =========================
from backend.routers.upload import router as upload_service
from backend.routers.mail_router import router as mail_service
from backend.routers.produto_router import router as produto_router
from backend.routers.movimentacao_router import router as movimentacao_router
from backend.routers.views_router import router as view_router
from backend.routers.event_router import router as event_router
from backend.routers.notification_router import router as notification_router
from backend.routers.analytics_router import router as analytics_router

# =========================
# IMPORTS DE LOGGING
# =========================
from backend.logging_config import setup_logging, get_logger
from backend.logging_middleware import LoggingMiddleware
from backend.logger import logger as app_logger

# =========================
# IMPORTS DE LLM
# =========================
from llm_module.routers.llm_router import router as llm_router

# =========================
# IMPORTS DO MODULO ADMIN
# =========================
from admin_module.routers.health_router import router as health_router
from admin_module.routers.status_router import router as status_router
from admin_module.routers.logs_router import router as logs_router

# =========================
# IMPORT DO MODULO AUTH
# =========================
from auth_module.routers.user_router import router as auth_router
from auth_module.routers.recovery_router import router as recovery_router

# =========================
# CONFIGURA LOGGING (1x)
# =========================
setup_logging()
app_logger_instance = get_logger()


# =========================
# CRIA UM POOL GLOBAL DE CONEXOES COM O BANCO DE DADOS
# =========================
load_env_from_root()
async def check_conn(conn):
    await conn.execute("SELECT 1")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # =========================
    # 1. INICIALIZAÇÃO (STARTUP)
    # =========================
    pool = AsyncConnectionPool(
        conninfo=os.getenv("DATABASE_URL"),
        check=check_conn,
        min_size=0, 
        max_size=30,
        timeout=5.0,
        kwargs={
            "autocommit": True,
            "row_factory": dict_row, # 💡 ESSENCIAL: Faz o banco retornar dicionários
        },
        open=False
    )
    await pool.open()
    app.state.db_pool = pool

    # Inicializa os serviços de LLM uma única vez
    from llm_module.services.llm_service import LLMService
    from llm_module.services.llm_sessions import LLMSessionService
    llm_service = LLMService(pool)
    session_service = LLMSessionService(pool)

    app.state.llm_service = llm_service
    app.state.session_service = session_service

    yield # O app roda aqui

    # =========================
    # 2. ENCERRAMENTO (SHUTDOWN)
    # =========================
    await llm_service.close() 
    await pool.close()


# =========================
# CRIA A APLICAÇÃO
# =========================
app = FastAPI(
    title="API Geral do Gestock",
    description="API com sistema de logging",
    version="2.0.0",
    lifespan=lifespan
)

# =========================
# MIDDLEWARES
# =========================
# Logging automático
app.add_middleware(LoggingMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000", 
        "http://localhost:3000", 
        "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)



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

@app.on_event("startup")
def print_routes():
    for route in app.routes:
        print(f"Rota encontrada: {route.path}")

# =========================
# DEPENDENCIA
# Ideal é proteger todos os routers com get_current_user!!
# =========================
from auth_module.utils.security import get_current_user

# =========================
# REGISTRO DOS ROUTERS
# =========================
app.include_router(upload_service)
app.include_router(mail_service)
app.include_router(produto_router)
app.include_router(view_router)
app.include_router(movimentacao_router)
app.include_router(event_router)
app.include_router(notification_router)
app.include_router(llm_router)
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])

app.include_router(health_router, dependencies=[Depends(get_current_user)], tags=["Módulo de Administração"])
app.include_router(status_router, dependencies=[Depends(get_current_user)], tags=["Módulo de Administração"])
app.include_router(logs_router, dependencies=[Depends(get_current_user)], tags=["Módulo de Administração"])

app.include_router(auth_router)
app.include_router(recovery_router)
