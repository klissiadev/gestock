import os

class Config:
    """Centraliza as configurações do ambiente."""
    SYSTEM_PROMPT_LOCATION = os.getenv("SYSTEM_PROMPT_LOCATION")
    MAX_INPUT_SIZE = int(os.getenv("MAX_INPUT_LENGTH", "4000"))
    
    # Adicione ?sslmode=require ao final da URL
    DB_URI = (
        f"postgres://{os.getenv('DB_LLM_USER')}:{os.getenv('DB_LLM_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        f"?sslmode=require&channel_binding=require"
    )