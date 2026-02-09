
from typing import List, Dict
from uuid import uuid4
from datetime import datetime

from llm_module.services.llm_service import LLMService


class LLMSessionService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def create_session(self) -> str:
        await self.llm_service.chatbot.init()
        session_id = str(uuid4())

        query = """
            INSERT INTO app_ai.conversation_sessions (
                session_id, created_at, updated_at
            )
            VALUES (%s, NOW(), NOW())
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            await conn.execute(query, (session_id,))

        return session_id

    async def session_exists(self, session_id: str) -> bool:
        await self.llm_service.chatbot.init()

        query = """
            SELECT 1
            FROM app_ai.conversation_sessions
            WHERE session_id = %s
            LIMIT 1
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id,))
            return await cursor.fetchone() is not None

    async def list_sessions(self) -> List[Dict]:
        await self.llm_service.chatbot.init()

        query = """
            SELECT session_id, title, updated_at
            FROM app_ai.conversation_sessions
            ORDER BY updated_at DESC
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query)
            rows = await cursor.fetchall()

        return [
            {
                "session_id": str(r["session_id"]),
                "title": r["title"] or f"Sessão {str(r['session_id'])[:8]}",
                "updated_at": r["updated_at"],
            }
            for r in rows
        ]

    async def touch_session(self, session_id: str):
        query = """
            UPDATE app_ai.conversation_sessions
            SET updated_at = NOW()
            WHERE session_id = %s
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            await conn.execute(query, (session_id,))

    async def get_session_messages(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:

        query = """
            SELECT id, user_message, bot_response, created_at
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
    

    
    async def ensure_session(self, session_id: str | None) -> str:
        """
        Garante que sempre exista uma sessão válida.
        - Cria se vier None
        - Cria se não existir no banco
        """

        if not session_id:
            return await self.create_session()

        exists = await self.session_exists(session_id)

        if not exists:
            return await self.create_session()

        return session_id
