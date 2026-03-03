import os
import asyncio
import uvicorn
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from request_module.routes.requisicoes import router as req_router
from request_module.utils.env_loader import load_env_from_root

load_env_from_root()

app = FastAPI(title="Sandbox de Teste - Gestock")

@app.on_event("startup")
async def startup():
    pool = AsyncConnectionPool(
        conninfo=os.getenv("DATABASE_URL"),
        kwargs={"autocommit": True, "row_factory": dict_row},
        open=False
    )
    await pool.open()
    app.state.db_pool = pool
    print("🚀 Pool de teste conectado!")

app.include_router(req_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)