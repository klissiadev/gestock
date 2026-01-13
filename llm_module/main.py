from fastapi import FastAPI
from llm_module.routers.llm_router import router as llm_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="LLM Module API",
        version="1.0.0",
        description="API para interação com LLM"
    )

    app.include_router(llm_router)

    return app


app = create_app()