from admin_module.utils.database import get_db_connection
from typing import List, Dict, Any, Tuple, Union
from psycopg import sql
from psycopg.rows import dict_row


class LogFetcher:

    def _execute_select(
        self,
        query: sql.Composable,
        params: list = None
    ) -> List[Dict]:

        try:
            with get_db_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cur:

                    cur.execute(query, params or [])

                    return cur.fetchall()

        except Exception as e:
            print(f"Erro na execução do LogFetcher: {e}")
            return []


    def _query_generator(
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
        search_cols: List[str] = None,
        limit: int = None,
        offset: int = None,
    ) -> Tuple[sql.Composable, List[Any]]:
        params = []

        # SELECT
        if columns:
            cols = []
            for c in columns:
                if "." in c:
                    schema, col = c.split(".", 1)
                    cols.append(sql.Identifier(schema, col))
                else:
                    cols.append(sql.Identifier(c))
            select_clause = sql.SQL(", ").join(cols)
        else:
            select_clause = sql.SQL("*")

        # FROM
        if "." in table:
            schema, tbl = table.split(".", 1)
            table_identifier = sql.Identifier(schema, tbl)
        else:
            table_identifier = sql.Identifier(table)

        # JOIN
        join_clause = sql.SQL("")
        if type_join and join_tables:
            join_parts = []
            for join_table, join_condition in join_tables:
                if "." in join_table:
                    schema, tbl = join_table.split(".", 1)
                    join_identifier = sql.Identifier(schema, tbl)
                else:
                    join_identifier = sql.Identifier(join_table)
                join_parts.append(
                    sql.SQL(" {} {} ON {}").format(
                        sql.SQL(type_join),
                        join_identifier,
                        sql.SQL(join_condition)  # trusted only
                    )
                )
            join_clause = sql.SQL("").join(join_parts)

        # WHERE
        where_parts = []
        if isinstance(conditions, dict):
            for key, val in conditions.items():
                if "." in key:
                    schema, col = key.split(".", 1)
                    identifier = sql.Identifier(schema, col)
                else:
                    identifier = sql.Identifier(key)
                if isinstance(val, (list, tuple)):
                    placeholders = sql.SQL(", ").join(
                        sql.Placeholder() for _ in val
                    )
                    where_parts.append(
                        sql.SQL("{} IN ({})").format(
                            identifier,
                            placeholders
                        )
                    )
                    params.extend(val)

                else:
                    where_parts.append(
                        sql.SQL("{} = {}").format(
                            identifier,
                            sql.Placeholder()
                        )
                    )
                    params.append(val)

        elif isinstance(conditions, str) and value is not None:
            identifier = sql.Identifier(conditions)
            where_parts.append(
                sql.SQL("{} = {}").format(
                    identifier,
                    sql.Placeholder()
                )
            )
            params.append(value)

        # SEARCH
        if search_term and search_cols:
            search_parts = []
            for col in search_cols:
                identifier = sql.Identifier(col)
                search_parts.append(
                    sql.SQL("unaccent({}) ILIKE {}").format(
                        identifier,
                        sql.Placeholder()
                    )
                )
                params.append(f"%{search_term}%")
            where_parts.append(
                sql.SQL("(") +
                sql.SQL(" OR ").join(search_parts) +
                sql.SQL(")")
            )
        where_clause = (
            sql.SQL(" WHERE ") + sql.SQL(" AND ").join(where_parts)
        ) if where_parts else sql.SQL("")

        # ORDER
        order_clause = sql.SQL("")
        if order_by:
            cols = []
            for col in order_by.split(","):
                if "." in col:
                    schema, c = col.split(".", 1)
                    cols.append(sql.Identifier(schema, c))
                else:
                    cols.append(sql.Identifier(col))
            direction_sql = sql.SQL("DESC") if direction == "DESC" else sql.SQL("ASC")
            order_clause = sql.SQL(
                " ORDER BY {} {}"
            ).format(
                sql.SQL(", ").join(cols),
                direction_sql
            )

        # LIMIT OFFSET
        limit_clause = sql.SQL("")
        offset_clause = sql.SQL("")
        if limit is not None:
            limit_clause = sql.SQL(" LIMIT {}").format(sql.Literal(limit))
        if offset is not None:
            offset_clause = sql.SQL(" OFFSET {}").format(sql.Literal(offset))

        # FINAL
        query = sql.SQL(
            "SELECT {} FROM {}{}{}{}{}"
        ).format(
            select_clause,
            table_identifier,
            join_clause,
            where_clause,
            order_clause,
            limit_clause + offset_clause
        )
        return query, params


    def __fetch_all(self, **kwargs):
        query, params = self._query_generator(**kwargs)
        return self._execute_select(query, params)


    def fetch_log_import(
        self,
        limit=50,
        offset=0,
        search=None
    ):

        return self.__fetch_all(
            table="app_logs.importacao",
            type_join="INNER JOIN",
            join_tables=[("app.usuario","app.usuario.id = app_logs.importacao.id_usuario")],
            columns=[
                "app_logs.importacao.id",
                "app_logs.importacao.nome_arquivo",
                "app_logs.importacao.quantidade",
                "app_logs.importacao.status",
                "app_logs.importacao.mensagem",
                "app_logs.importacao.created_at",
                "app.usuario.nome"
            ],
            search_term=search,
            search_cols=["nome_arquivo", "mensagem"],
            order_by="app_logs.importacao.created_at",
            direction="DESC",
            limit=limit,
            offset=offset
        )
