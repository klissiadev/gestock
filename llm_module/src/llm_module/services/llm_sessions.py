from typing import List, Dict
from uuid import uuid4, UUID
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class LLMSessionService:
    def __init__(self, connection_pool):
        self.pool = connection_pool

    async def create_session(self, user_id: UUID) -> str:
        """Cria uma nova sessão vinculada a um usuário."""
        session_id = str(uuid4())
        query = """
            INSERT INTO app_ai.conversation_sessions (
                id_usuario, session_id, created_at, updated_at, title
            )
            VALUES (%s, %s, NOW(), NOW(), 'Nova Conversa')
        """
        async with self.pool.connection() as conn:
            await conn.execute(query, (user_id, session_id))
        return session_id


    async def list_sessions(self, user_id: UUID) -> List[Dict]:
        """Lista todas as sessões de um usuário específico."""
        query = """
            SELECT session_id, title, updated_at
            FROM app_ai.conversation_sessions
            WHERE id_usuario = %s
            ORDER BY updated_at DESC 
        """
        async with self.pool.connection() as conn:
            cursor = await conn.execute(query, (user_id,))
            rows = await cursor.fetchall()

        return [
            {
                "session_id": str(r["session_id"]),
                "title": r["title"] or "Nova Conversa",
                "updated_at": r["updated_at"],
            }
            for r in rows
        ]


    async def get_session_messages(self, session_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Recupera o histórico de mensagens formatado para o frontend."""
        query = """
            SELECT id, user_message, bot_response, created_at
            FROM app_ai.conversation_logs
            WHERE session_id = %s
            ORDER BY created_at ASC
            LIMIT %s OFFSET %s
        """
        async with self.pool.connection() as conn:
            cursor = await conn.execute(query, (session_id, limit, offset))
            rows = await cursor.fetchall()

        messages = []
        for row in rows:
            # 💡 Mantemos a lógica de ID único para User e Assistant
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


    async def is_owner(self, session_id: str, user_id: UUID) -> bool:
        """Verifica se a sessão pertence ao usuário informado."""
        query = """
            SELECT 1 FROM app_ai.conversation_sessions
            WHERE session_id = %s AND id_usuario = %s
        """
        async with self.pool.connection() as conn:
            cursor = await conn.execute(query, (session_id, user_id))
            return await cursor.fetchone() is not None


    async def update_session_title(self, session_id: str, title: str):
        """Atualiza o título da sessão (ex: gerado pela LLM)."""
        query = "UPDATE app_ai.conversation_sessions SET title = %s, updated_at = NOW() WHERE session_id = %s::uuid"
        async with self.pool.connection() as conn:
            await conn.execute(query, (title, session_id))


    async def touch_session(self, session_id: str):
        """Atualiza apenas o timestamp de atividade da sessão."""
        query = "UPDATE app_ai.conversation_sessions SET updated_at = NOW() WHERE session_id = %s"
        async with self.pool.connection() as conn:
            await conn.execute(query, (session_id,))


    async def ensure_session(self, session_id: str | None, user_id: UUID) -> str:
        """Garante uma sessão válida, criando uma nova se necessário."""
        if not session_id:
            return await self.create_session(user_id)

        if not await self.is_owner(session_id, user_id):
            raise HTTPException(status_code=404, detail="Sessão não encontrada ou acesso negado")

        return session_id


    async def get_session_title(self, session_id: str) -> str:
        """Busca o título atual de uma sessão."""
        query = "SELECT title FROM app_ai.conversation_sessions WHERE session_id = %s::uuid"
        async with self.pool.connection() as conn:
            cursor = await conn.execute(query, (session_id,))
            row = await cursor.fetchone()
            return row["title"] if row else "Nova Conversa"