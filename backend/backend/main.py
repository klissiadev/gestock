from fastapi import FastAPI
from backend.routers.log_importacao_router import router as log_importacao_router

app = FastAPI()

app.include_router(log_importacao_router)

@app.get("/")
def root():
    return {"msg": "API rodando!"}
