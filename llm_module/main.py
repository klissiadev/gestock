from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm_module.routers.llm_router import router as llm_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router, prefix="/llm")