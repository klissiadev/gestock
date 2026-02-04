from typing import List, Dict
from uuid import uuid4

from llm_module.services.llm_service import LLMService


class LLMSessionService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    # -------------------------
    # LISTAR SESSÕES
    # -------------------------
    async def list_sessions(self) -> List[Dict]:
        await self.llm_service.chatbot.init()

        query = """
            SELECT
                session_id,
                MAX(created_at) AS last_message
            FROM app_ai.conversation_logs
            GROUP BY session_id
            ORDER BY last_message DESC
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query)
            rows = await cursor.fetchall()

        return [
            {
                "session_id": row["session_id"],
                "last_message": row["last_message"],
            }
            for row in rows
        ]

    # -------------------------
    # VERIFICAR EXISTÊNCIA
    # -------------------------
    async def session_exists(self, session_id: str) -> bool:
        await self.llm_service.chatbot.init()

        query = """
            SELECT 1
            FROM app_ai.conversation_logs
            WHERE session_id = %s
            LIMIT 1
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id,))
            row = await cursor.fetchone()

        return row is not None

    # -------------------------
    # CRIAR SESSÃO
    # -------------------------
    def create_session(self) -> str:
        # Apenas gera UUID.
        # Sessão será criada quando houver primeira mensagem.
        return str(uuid4())


    # -------------------------
    # OBTER MENSAGENS DA SESSÃO
    # -------------------------
    async def get_session_messages(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:

        await self.llm_service.chatbot.init()

        query = """
            SELECT
                id,
                user_message,
                bot_response,
                created_at
            FROM app_ai.conversation_logs
            WHERE session_id = %s
            ORDER BY created_at ASC
            LIMIT %s OFFSET %s
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id, limit, offset))
            rows = await cursor.fetchall()

        messages = []

        for row in rows:

            messages.append({
                "id": f"{row['id']}-user",
                "role": "user",
                "content": row["user_message"],
                "created_at": row["created_at"]
            })

            messages.append({
                "id": f"{row['id']}-assistant",
                "role": "assistant",
                "content": row["bot_response"],
                "created_at": row["created_at"]
            })

        return messages