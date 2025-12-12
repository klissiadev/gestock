# camada padrão de acesso ao banco de dados
from fastapi import HTTPException

class Repository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    # -----------------------------
    # INSERT SIMPLES (sem retorno)
    # -----------------------------
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

    # -------------------------------------------------
    # INSERT COM RETURNING (para pegar cod_produto etc.)
    # -------------------------------------------------
    def insert_returning(self, table, data: dict, returning: str):
        try:
            cols = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())

            sql = f"""
                INSERT INTO {table} ({cols})
                VALUES ({placeholders})
                RETURNING {returning}
            """
            self.cursor.execute(sql, values)
            new_id = self.cursor.fetchone()[0]
            return new_id

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -----------------------------
    # SELECT ONE (por ID)
    # -----------------------------
    def fetch_one(self, table, key, value):
        try:
            sql = f"SELECT * FROM {table} WHERE {key} = %s"
            self.cursor.execute(sql, (value,))
            return self.cursor.fetchone()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -----------------------------
    # SELECT ALL (listar tudo)
    # -----------------------------
    def fetch_all(self, table):
        try:
            sql = f"SELECT * FROM {table}"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, table, key, value, data: dict):
        try:
            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {key} = %s"

            values = list(data.values())
            values.append(value)

            self.cursor.execute(sql, tuple(values))
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete(self, table, key, value):
        try:
            sql = f"DELETE FROM {table} WHERE {key} = %s"
            self.cursor.execute(sql, (value,))
            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # -----------------------------
    # COMMIT e CLOSE
    # -----------------------------
    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")

    def close(self):
        self.cursor.close()
