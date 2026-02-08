from admin_module.utils.database import get_db_connection
from typing import List, Dict, Any, Tuple, Union
from psycopg import sql
from psycopg.rows import dict_row


class LogFetcher:
    # Faz SELECT

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
        extra_params: dict[str, Any] | None = None,
    ) -> list[dict]:

        columns_sql = ", ".join(columns) if columns else "*"

        query = f"SELECT {columns_sql} FROM {table}"

        where_clauses = []
        params = {}

        # conditions
        if conditions:
            for i, (col, value) in enumerate(conditions.items()):
                param_name = f"cond_{i}"
                where_clauses.append(f"{col} = %({param_name})s")
                params[param_name] = value


        # search
        if search_term and search_cols:
            search_parts = []

            for i, col in enumerate(search_cols):
                param_name = f"search_{i}"
                search_parts.append(f"{col} ILIKE %({param_name})s")
                params[param_name] = f"%{search_term}%"

            where_clauses.append("(" + " OR ".join(search_parts) + ")")

        if extra_where:
            where_clauses.extend(extra_where)

        if extra_params:
            params.update(extra_params)

        # apply WHERE
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)


        # order
        if order_by:
            direction = direction.upper()
            if direction not in ("ASC", "DESC"):
                direction = "ASC"

            query += f" ORDER BY {order_by} {direction}"


        # execute
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query, params)
                return cur.fetchall()


    def _refresh_log(self, table: str):
        with get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {table}")

    def get_import_log(
        self,
        direction: str = "DESC",
        order_by: str = "registrado_em",
        search_term: str | None = None,
        status: str | None = None,
        periodo: tuple[str, str] | None = None,
        apenas_erro: bool = False,
    ) -> list[dict]:
        
        COLUNAS_VALIDAS = ["id", "nome_arquivo", "qntd_registros", "status", "msg_erro", "registrado_em", "usuario"]
        SEARCH_COLS = ["nome_arquivo", "usuario", "msg_erro"]

        if order_by not in COLUNAS_VALIDAS:
            order_by = "registrado_em"

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
                extra_where.append("registrado_em >= %(data_inicio)s")
                extra_params["data_inicio"] = data_inicio
            if data_fim:
                extra_where.append("registrado_em <= %(data_fim)s")
                extra_params["data_fim"] = data_fim

        # Antes do fetch atualiza a tabela
        self._refresh_log("app_logs.logs_import")

        result = self._fetch_all(
            table="app_logs.logs_import",
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