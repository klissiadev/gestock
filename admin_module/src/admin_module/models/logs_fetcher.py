
from admin_module.utils.database import get_db_connection
from typing import List, Dict, Any, Tuple, Union
from psycopg import sql
from psycopg.rows import dict_row

# Logs suportados
# -> Importação
# -> Conversas da LLM
# -> Requisição (NÃO IMPLEMENTADOs)


class LogFetcher:
    def _fetch_all(
        self,
        table: str,
        columns: list[str] | None = None,
        conditions: dict[str, Any] | None = None,
        order_by: str | None = None,
        direction: str = "ASC",
        search_term: str | None = None,
        search_cols: list[str] | None = None,
        extra_where: list[str] | None = None,
        extra_params: dict[str, Any] | None = None
    ) -> list[dict]:

        if columns:
            cols_query = sql.SQL(", ").join(map(sql.Identifier, columns))
        else:
            cols_query = sql.SQL("*")

        query_base = sql.SQL("SELECT {cols} FROM {table}").format(
            cols=cols_query,
            table=sql.Identifier(*table.split('.'))
        )

        where_clauses = []
        params = {}

        if conditions:
            for i, (col, value) in enumerate(conditions.items()):
                param_name = f"cond_{i}"
                where_clauses.append(sql.SQL("{col} = %({param})s").format(
                    col=sql.Identifier(col),
                    param=sql.Literal(param_name)
                ))
                params[param_name] = value

        if search_term and search_cols:
            search_parts = []
            for i, col in enumerate(search_cols):
                param_name = f"search_{i}"
                search_parts.append(sql.SQL("{col} ILIKE %({param})s").format(
                    col=sql.Identifier(col),
                    param=sql.Literal(param_name)
                ))
                params[param_name] = f"%{search_term}%"

            where_clauses.append(sql.SQL("({parts})").format(
                parts=sql.SQL(" OR ").join(search_parts)
            ))

        if extra_where:
            for clause in extra_where:
                where_clauses.append(sql.SQL(clause))

        if extra_params:
            params.update(extra_params)

        full_query = query_base
        if where_clauses:
            full_query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(where_clauses)

        if order_by:
            dir_sql = sql.SQL("DESC") if direction.upper() == "DESC" else sql.SQL("ASC")
            full_query += sql.SQL(" ORDER BY {col} {direction}").format(
                col=sql.Identifier(order_by),
                direction=dir_sql
            )

        # 6. Execução
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(full_query, params)
                return cur.fetchall()

    # Atualiza a tabela sempre que faz consulta
    def _refresh_log(self, table: str):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {table}")

    # Buscar log de importacao
    def get_import_log(
        self,
        direction: str = "DESC",
        order_by: str = "created_at",
        search_term: str | None = None,
        status: str | None = None,
        periodo: tuple[str, str] | None = None,
        apenas_erro: bool = False
    ) -> list[dict]:

        COLUNAS_VALIDAS = [
            "id",
            "nome_arquivo",
            "qntd_registros",
            "status",
            "msg_erro",
            "created_at",
            "responsavel_por"
        ]

        SEARCH_COLS = ["nome_arquivo", "msg_erro"]

        if order_by not in COLUNAS_VALIDAS:
            order_by = "created_at"

        conditions = {}

        if status:
            conditions["status"] = status

        if apenas_erro:
            conditions["status"] = "ERRO"

        extra_where = []
        extra_params = {}

        if periodo:
            data_inicio, data_fim = periodo

            if data_inicio:
                extra_where.append("created_at >= %(data_inicio)s")
                extra_params["data_inicio"] = data_inicio

            if data_fim:
                extra_where.append("created_at <= %(data_fim)s")
                extra_params["data_fim"] = data_fim

        result = self._fetch_all(
            table="app_logs.mv_imports",
            columns=COLUNAS_VALIDAS,
            conditions=conditions,
            order_by=order_by,
            direction=direction,
            search_term=search_term,
            search_cols=SEARCH_COLS,
            extra_where=extra_where,
            extra_params=extra_params,
        )


        return result
    
    
    # Conversas da LLM
    def get_llm_log(
        self,
        period: tuple[str, str] = None,
        user_name: str = None,
    ) -> list[dict]: 
        
        extra_where = []
        extra_params = {}
        COLUNAS = ["id", "session_id", "user_message", "bot_response", "created_at"]

        if period:
            data_inicio, data_fim = period
            if data_inicio:
                extra_where.append("created_at >= %(start)s")
                extra_params["start"] = data_inicio
            if data_fim:
                extra_where.append("created_at < (%(end)s::date + interval '1 day')")
                extra_params["end"] = data_fim

        # self._refresh_log("app_ai.conversation_logs")
        
        return self._fetch_all(
            table="app_ai.conversation_logs",
            columns=COLUNAS,
            extra_where=extra_where,
            extra_params=extra_params,
            order_by="created_at",
            direction="DESC"
        )
    
    # Tabela de usuarios
    def get_usuarios_data(
            self,
            search_term: str | None = None,
            order_by: str = "created_at",
            direction: str = "DESC"
    ):
        
        COLUNAS = ["id", "nome", "papel", "email"]
        SEARCH_COLS = ["nome", "email"]
        
        return self._fetch_all(
            table="app_core.usuarios",
            columns=COLUNAS,
            search_term=search_term,
            search_cols=SEARCH_COLS,
            order_by=order_by,
            direction=direction
        )
        