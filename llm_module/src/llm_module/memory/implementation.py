# Nome da tabela: app_ai.message
# Nome de indice: idx_message_session_id

import uuid
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from llm_module.memory.chat_message_histories import PostgresChatMessageHistory
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conninfo = (
            f"host={os.getenv('DB_HOST')} "
            f"port={os.getenv('DB_PORT')} "
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_LLM_USER')} "
            f"password={os.getenv('DB_LLM_PASSWORD')}"
        )

table_name = "messages"
session_id = str("fc56a261-d4b1-4993-8914-5a8fd4ec0805")  # Using a fixed session ID for testing
connection = psycopg.connect(conninfo)

# Initialize the chat history manager
chat_history = PostgresChatMessageHistory(
    table_name,
    session_id,
    sync_connection=connection,
)

# Add messages to the chat history
print(chat_history.get_messages()[-1].content)  # Output: meow