from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.upload import router as upload_service
from backend.routers.mail_router import router as mail_service
from backend.routers.produto_router import router as produto_router
from backend.routers.movimentacao_router import router as movimentacao_router
from backend.routers import test_db
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_service)
app.include_router(mail_service)
app.include_router(produto_router)
