from typing import List, Dict
from uuid import uuid4, UUID
from datetime import datetime
from fastapi import HTTPException

from llm_module.services.llm_service import LLMService


class LLMSessionService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def create_session(self, id: UUID) -> str:
        """
        Recebe o id do usuario e cria uma sessão pra ele
        """
        await self.llm_service.ensure_init()
        session_id = str(uuid4())

        query = """
            INSERT INTO app_ai.conversation_sessions (
                id_usuario, session_id, created_at, updated_at
            )
            VALUES (%s, %s, NOW(), NOW())
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            await conn.execute(query, (id, session_id,))

        return session_id

    async def session_exists(self, session_id: str) -> bool:
        """
        Verifica se a sessão existe com base no ID de sessão
        """
        await self.llm_service.ensure_init()
        query = """
            SELECT 1
            FROM app_ai.conversation_sessions
            WHERE session_id = %s
            LIMIT 1
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id,))
            return await cursor.fetchone() is not None

    async def list_sessions(self, id: UUID) -> List[Dict]:
        """cl
        Lista as sessões vinculadas a um id de usuario especifico
        """
        await self.llm_service.ensure_init()
        query = """
            SELECT session_id, title, updated_at
            FROM app_ai.conversation_sessions
            WHERE id_usuario = %s
            ORDER BY updated_at DESC 
        """

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (id, ))
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
        await self.llm_service.ensure_init()
        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            await conn.execute(query, (session_id,))

    async def get_session_messages(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        await self.llm_service.ensure_init()
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
    
    async def ensure_session(self, session_id: str | None, user_id: UUID) -> str:
        """
        Garante que a sessão seja válida E pertença ao usuário.
        """
        await self.llm_service.ensure_init()
        # Se session_id é None: cria uma nova
        if not session_id:
            return await self.create_session(user_id)

        # se é um dono valido
        is_valid_owner = await self.is_owner(session_id, user_id)

        if not is_valid_owner:
            raise HTTPException(status_code=404, detail="Acesso proibido")

        return session_id

    
    async def get_session_title(self, session_id: str) -> str | None:
        await self.llm_service.ensure_init()
        query = "SELECT title FROM app_ai.conversation_sessions WHERE session_id = %s::uuid"

        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id,))
            row = await cursor.fetchone()

        if row:
            return row["title"]

        return None
    
    async def update_session_title(self, session_id: str, title: str):
        await self.llm_service.ensure_init()
        query = "UPDATE app_ai.conversation_sessions SET title = %s WHERE session_id = %s::uuid"
        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            await conn.execute(query, (title, session_id))
    
    async def is_owner(self, session_id: str, user_id: UUID) -> bool:
        await self.llm_service.ensure_init()
        query = """
                SELECT 1
                FROM app_ai.conversation_sessions
                WHERE session_id = %s AND id_usuario = %s
                LIMIT 1
                """ 
        
        async with self.llm_service.chatbot.memory_pool.connection() as conn:
            cursor = await conn.execute(query, (session_id, user_id))
            return await cursor.fetchone() is not None