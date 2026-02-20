# src/llm_module/audit/logger.py
import logging

logger = logging.getLogger(__name__)

class AuditLogger:
    def __init__(self, pool):
        self.pool = pool

    async def save_conversation(self, session_id: str, user_input: str, bot_output: str):
        """Salva a interação no banco de dados para fins de auditoria e histórico."""
        query = """
            INSERT INTO app_ai.conversation_logs (session_id, user_message, bot_response)
            VALUES (%s, %s, %s)
        """
        try:
            async with self.pool.connection() as conn:
                await conn.execute(query, (session_id, user_input, bot_output))
        except Exception as e:
            logger.error(f"Falha ao gravar auditoria para sessão {session_id}: {e}", exc_info=True)