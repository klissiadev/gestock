import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from datetime import date


class PostgresClient:
    def __init__(self):
        load_dotenv()

        self.conninfo = (
            f"host={os.getenv('DB_HOST')} "
            f"port={os.getenv('DB_PORT')} "
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_LLM_USER')} "
            f"password={os.getenv('DB_LLM_PASSWORD')}"
        )

    def _normalize_date(self, rows: list[dict]) -> list[dict]:
        for row in rows:
            for k, v in row.items():
                if isinstance(v, date):
                    row[k] = v.isoformat()
        return rows

    def fetch_all(self, query: str, params: tuple | None = None):
        if not query.strip().lower().startswith("select"):
            raise ValueError("Somente queries SELECT são permitidas.")

        try:
            # conexão aberta e fechada automaticamente
            with psycopg.connect(self.conninfo) as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(query, params or ())
                    result = cur.fetchall()
                    return self._normalize_date(result)

        except Exception as e:
            print(f"Erro na execução da query: {e}")
            return []