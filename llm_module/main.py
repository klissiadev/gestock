from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm_module.routers.llm_router import router as llm_router
from llm_module.services.llm_service import LLMService

llm_service = LLMService()
app = FastAPI()

@app.on_event("startup")
async def startup():
    await llm_service.chatbot.init()

@app.on_event("shutdown")
async def shutdown():
    await llm_service.chatbot.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router, prefix="/llm")