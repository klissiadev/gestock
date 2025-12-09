#camada padrão de acesso ao banco de dados
from fastapi import HTTPException

class Repository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insert(self, table, data: dict):
        try:
            cols = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())

            sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            return True

        except Exception as e:
            return False, str(e)

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")

    def close(self):
        self.cursor.close()
