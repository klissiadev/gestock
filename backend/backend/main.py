# backend/main.py
from fastapi import FastAPI
from backend.routers import log_importacao_router  # Importe isso

app = FastAPI()

# Registre a rota
app.include_router(log_importacao_router.router)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}