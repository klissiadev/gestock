# camada padrão de acesso ao banco de dados
from fastapi import HTTPException
from typing import Optional, List, Dict, Any, Tuple, Union
import re
from psycopg2.extras import RealDictCursor, execute_values


class Repository:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(cursor_factory=RealDictCursor)
    # =================================================
    # MÉTODOS AUXILIARES
    # =================================================

    def _quote_identifier(self, identifier: str) -> str:
        """
        Formata identificadores SQL no padrão:
        - "Tabela".coluna
        - "Tabela".coluna AS alias
        - "Tabela"
        """
        # Usuario.nome AS nome_usuario
        if " AS " in identifier.upper():
            left, alias = identifier.split(" AS ", 1)
            return f"{self._quote_identifier(left)} AS {alias}"

        # 2. Trata tabela.coluna
        if "." in identifier:
            table, col = identifier.split(".", 1)
            return f"\"{table}\".{col}"

        # 3. Trata identificador simples (tabela)
        return f"\"{identifier}\""


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

    
    def _build_conditions(self, conditions: Union[Dict, str], value: Any = None) -> Tuple[List[str], List[Any]]:
        """
        Faz a mesma coisa que o _build_where_clause, a diferença que nao tem WHERE!!!!
        Não apaguei porque to meio cansada pra mexer numa função que meu cerebro nao entendeu 100% e quebrar alguma coisa
        Então tem essa variação não muito charmosa
        """
        parts = []
        values = []

        # Modo string
        if isinstance(conditions, str) and value is not None:
            parts.append(f"{self._quote_identifier(conditions)} = %s")
            values.append(value)

        # Modo Dict
        elif isinstance(conditions, dict):
            for key, val in conditions.items():
                if isinstance(val, (list, tuple)) and val:
                    # IN query
                    placeholders = ", ".join(["%s"] * len(val))
                    parts.append(f"{self._quote_identifier(key)} IN ({placeholders})")
                    values.extend(val)
                else:
                    # Igualdade simples
                    parts.append(f"{self._quote_identifier(key)} = %s")
                    values.append(val)
        
        return parts, values

    def _build_search_clause(
            self,
            term: str,
            cols: List[str]   
    ) -> Tuple[Optional[str], List[Any]]:
        """
        Monta a query para buscar um 'term' em uma lista de colunas determinadas
        Retorna uma tupla (sql_string, lista_valores).
        """
        # Se vazio
        if not term or not cols:
            return None, []
        
        clauses = [f"{self._quote_identifier(c)} ILIKE %s" for c in cols]

        if not clauses:
            return None, []

        sql_part = f"({' OR '.join(clauses)})"
        wildcard = f"%{term}%"
        values = [wildcard] * len(cols)

        return sql_part, values
        
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
        type_join: str = None,
        join_tables: List[Tuple[str, str]] = None,
        conditions: Union[Dict[str, Any], str, None] = None,
        value: Any = None,
        order_by: str = None,
        direction: str = None,
        columns: List[str] = None,
        search_term: str = None,
        search_cols: List[str] = None
    ) -> List[Dict]:
        try:
            # 1. Monta SELECT em col_Q
            table_q = self._quote_identifier(table)
            col_q = ", ".join(self._quote_identifier(c) for c in columns) if columns else "*"
            
            # 2. Monta o JOIN
            join_sql = ""
            if type_join and join_tables:
                for join_table, join_condition in join_tables:
                    join_table_q = self._quote_identifier(join_table)
                    join_sql += f" {type_join} {join_table_q} ON {join_condition}"

            # 3. Filtros exatos (como o categoria)
            where_parts, query_values = self._build_conditions(conditions, value)

            # 4. filtro de busca
            search_part, search_values = self._build_search_clause(search_term, search_cols)

            # 5. Unifica tudo
            if search_part:
                where_parts.append(search_part)    
                query_values.extend(search_values)  
            
            # 6. Constrói o WHERE final
            where_sql = (" WHERE " + " AND ".join(where_parts)) if where_parts else ""

            # 7. Monta ORDER BY
            order_sql = ""
            if order_by:
                order_q = ", ".join(self._quote_identifier(c.strip()) for c in order_by.split(","))
                order_sql = f" ORDER BY {order_q} {direction}"

            # 8. Executa
            sql = f"SELECT {col_q} FROM {table_q}{join_sql}{where_sql}{order_sql}"
            print(sql)
            self.cursor.execute(sql, query_values)
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


    # bulk insert para a otimização de importação
    def bulk_insert(self, table: str, rows: list[dict]):
        if not rows:
            return {"success": 0, "failed": []}

        try:
            # quote da tabela
            table_q = self._quote_identifier(table)

            # quote das colunas
            columns = list(rows[0].keys())
            cols_q = ", ".join(self._quote_identifier(col) for col in columns)

            # valores
            values = [
                tuple(row[col] for col in columns)
                for row in rows
            ]

            sql = f"""
                INSERT INTO {table_q} ({cols_q})
                VALUES %s
            """

            execute_values(self.cursor, sql, values)
            return {"success": len(rows), "failed": []}

        except Exception as e:
            self.conn.rollback()
            return {
                "success": 0,
                "failed": [
                    {"index": i, "error": str(e)}
                    for i in range(len(rows))
                ]
            }