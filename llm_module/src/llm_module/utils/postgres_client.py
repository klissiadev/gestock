import os
from dotenv import load_dotenv
import psycopg
from datetime import date


class PostgresClient:
    def __init__(self):
        """
        Inicializa a conexão síncrona com o Postgres usando psycopg.
        """
        load_dotenv()

        self.conninfo = (
            f"host={os.getenv('DB_HOST')} "
            f"port={os.getenv('DB_PORT')} "
            f"dbname={os.getenv('DB_NAME')} "
            f"user={os.getenv('DB_LLM_USER')} "
            f"password={os.getenv('DB_LLM_PASSWORD')}"
        )

        try:
            self.conn = psycopg.connect(self.conninfo)
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar no Postgres: {e}")
        
    def _normalize_date(self, rows: list[dict]) -> list[dict]:
        for row in rows:
            for k, v in row.items():
                if isinstance(v, date):
                    row[k] = v.isoformat()
        return rows

    def fetch_all(self, query: str, params: tuple = ()):
        """
        Executa uma query de SELECT e retorna todos os registros.
        """
        with self.conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(query, params)
            # Processo de normalizacao aqui
            result = cur.fetchall()
            return self._normalize_date(result)

    def close(self):
        """
        Fecha a conexão com o banco.
        """
        self.conn.close()

