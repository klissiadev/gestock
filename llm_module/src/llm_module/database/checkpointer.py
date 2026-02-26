#database/checkpointer.py
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

class CheckpointerFactory:
    @staticmethod
    async def create(pool):
        """
        Recebe o pool de conexões e prepara o checkpointer do LangGraph.
        """
        checkpointer = AsyncPostgresSaver(pool)
        async with pool.connection() as conn:
            setup_saver = AsyncPostgresSaver(conn)
            await setup_saver.setup()
            
        return checkpointer