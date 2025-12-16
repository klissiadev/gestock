# camada padrão de acesso ao banco de dados
from fastapi import HTTPException
from typing import Optional, List, Dict, Any, Tuple, Union
import re
from psycopg2.extras import RealDictCursor


class Repository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(cursor_factory=RealDictCursor)
    # =================================================
    # MÉTODOS AUXILIARES
    # =================================================

    def _quote_identifier(self, identifier: str) -> str:
        """Adiciona aspas duplas ao identificador se necessário"""
        if identifier.startswith('"') and identifier.endswith('"'):
            return identifier
        if re.search(r'[A-Z]', identifier) or not re.match(r'^[a-z_][a-z0-9_]*$', identifier):
            return f'"{identifier}"'
        return identifier

    def _build_where_clause(
        self,
        conditions: Union[Dict[str, Any], str, None],
        value: Any = None
    ) -> Tuple[str, List[Any]]:
        """
        Constrói cláusula WHERE.
        Suporta:
          - modo antigo: key, value
          - modo novo: dict
        """
        if isinstance(conditions, str):
            if value is None:
                return "", []
            return f" WHERE {self._quote_identifier(conditions)} = %s", [value]

        if isinstance(conditions, dict):
            if not conditions:
                return "", []

            parts = []
            values = []
            for key, val in conditions.items():
                if isinstance(val, (list, tuple)):
                    placeholders = ", ".join(["%s"] * len(val))
                    parts.append(f"{self._quote_identifier(key)} IN ({placeholders})")
                    values.extend(val)
                else:
                    parts.append(f"{self._quote_identifier(key)} = %s")
                    values.append(val)

            return " WHERE " + " AND ".join(parts), values

        return "", []

    # =================================================
    # INSERT
    # =================================================

    def insert(self, table: str, data: dict) -> bool:
        try:
            table_q = self._quote_identifier(table)
            cols = ", ".join(self._quote_identifier(k) for k in data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())

            sql = f"INSERT INTO {table_q} ({cols}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            return True

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao inserir: {str(e)}")

    def insert_returning(self, table: str, data: dict, returning: str) -> Any:
        try:
            table_q = self._quote_identifier(table)
            cols = ", ".join(self._quote_identifier(k) for k in data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            returning_q = self._quote_identifier(returning)
            values = tuple(data.values())

            sql = f"""
                INSERT INTO {table_q} ({cols})
                VALUES ({placeholders})
                RETURNING {returning_q}
            """
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            return result[returning] if result else None

        except Exception as e:
            self.conn.rollback()
            raise

    # =================================================
    # SELECT
    # =================================================

    def fetch_one(
        self,
        table: str,
        key_or_conditions: Union[str, Dict[str, Any]],
        value: Any = None
    ) -> Optional[Dict]:
        try:
            table_q = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(key_or_conditions, value)
            sql = f"SELECT * FROM {table_q}{where_clause} LIMIT 1"
            self.cursor.execute(sql, values)
            row = self.cursor.fetchone()
            return dict(row) if row else None

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar: {str(e)}")

    def fetch_all(
        self,
        table: str,
        conditions: Union[Dict[str, Any], str, None] = None,
        value: Any = None,
        order_by: str = None
    ) -> List[Dict]:
        try:
            table_q = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(conditions, value)
            sql = f"SELECT * FROM {table_q}{where_clause}"

            if order_by:
                order_q = ", ".join(self._quote_identifier(c.strip()) for c in order_by.split(","))
                sql += f" ORDER BY {order_q}"

            self.cursor.execute(sql, values)
            return [dict(row) for row in self.cursor.fetchall()]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar: {str(e)}")

    # =================================================
    # UPDATE
    # =================================================

    def update(
        self,
        table: str,
        key_or_conditions: Union[str, Dict[str, Any]],
        value_or_data: Any,
        data: dict = None
    ) -> int:
        try:
            table_q = self._quote_identifier(table)

            if data is not None:
                conditions = {key_or_conditions: value_or_data}
                update_data = data
            else:
                conditions = key_or_conditions
                update_data = value_or_data

            if not update_data:
                raise ValueError("Nenhum dado para atualizar")

            set_clause = ", ".join(f"{self._quote_identifier(k)} = %s" for k in update_data.keys())
            where_clause, where_values = self._build_where_clause(conditions)
            values = list(update_data.values()) + where_values

            sql = f"UPDATE {table_q} SET {set_clause}{where_clause}"
            self.cursor.execute(sql, values)
            return self.cursor.rowcount

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")

    # =================================================
    # DELETE
    # =================================================

    def delete(
        self,
        table: str,
        key_or_conditions: Union[str, Dict[str, Any]],
        value: Any = None
    ) -> int:
        try:
            table_q = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(key_or_conditions, value)
            sql = f"DELETE FROM {table_q}{where_clause}"
            self.cursor.execute(sql, values)
            return self.cursor.rowcount

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")

    # =================================================
    # QUERY CUSTOMIZADA
    # =================================================

    def execute_query(self, sql: str, params: Tuple = None) -> List[Dict]:
        try:
            self.cursor.execute(sql, params or ())
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na query: {str(e)}")

    # =================================================
    # TRANSAÇÃO
    # =================================================

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")

    def rollback(self):
        try:
            self.conn.rollback()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao reverter: {str(e)}")

    def close(self):
        try:
            self.cursor.close()
        except:
            pass
