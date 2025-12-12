# camada padrão de acesso ao banco de dados
from fastapi import HTTPException
from typing import Optional, List, Dict, Any, Tuple, Union


class Repository:
    
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
    
    # -----------------------------
    # MÉTODOS AUXILIARES
    # -----------------------------
    
    def _quote_identifier(self, identifier: str) -> str:
        """Adiciona aspas duplas ao identificador se necessário"""
        # Se já tem aspas, mantém
        if identifier.startswith('"') and identifier.endswith('"'):
            return identifier
        
        # Se tem letras maiúsculas ou caracteres especiais, adiciona aspas
        import re
        if re.search(r'[A-Z]', identifier) or not re.match(r'^[a-z_][a-z0-9_]*$', identifier):
            return f'"{identifier}"'
        
        return identifier
    
    def _build_where_clause(self, conditions: Union[Dict[str, Any], str, None], 
                           value: Any = None) -> Tuple[str, List[Any]]:
        """Constrói cláusula WHERE (compatibilidade com versões antigas e novas)"""
        # Se conditions for string (modo antigo: key, value)
        if isinstance(conditions, str):
            if value is None:
                return "", []
            return f" WHERE {self._quote_identifier(conditions)} = %s", [value]
        
        # Se conditions for dict (modo novo)
        if isinstance(conditions, dict):
            if not conditions:
                return "", []
            
            where_parts = []
            values = []
            
            for key, val in conditions.items():
                if isinstance(val, (list, tuple)):
                    # Para condições IN
                    placeholders = ", ".join(["%s"] * len(val))
                    where_parts.append(f"{self._quote_identifier(key)} IN ({placeholders})")
                    values.extend(val)
                else:
                    # Para condições =
                    where_parts.append(f"{self._quote_identifier(key)} = %s")
                    values.append(val)
            
            return " WHERE " + " AND ".join(where_parts), values
        
        # Se conditions for None
        return "", []
    
    # -----------------------------
    # INSERT SIMPLES (sem retorno)
    # -----------------------------
    
    def insert(self, table: str, data: dict) -> bool:
        """Insere um registro e retorna True/False"""
        try:
            table_quoted = self._quote_identifier(table)
            cols = ", ".join([self._quote_identifier(k) for k in data.keys()])
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())
            
            sql = f"INSERT INTO {table_quoted} ({cols}) VALUES ({placeholders})"
            self.cursor.execute(sql, values)
            return True
            
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao inserir: {str(e)}")
    
    # -------------------------------------------------
    # INSERT COM RETURNING (para pegar cod_produto etc.)
    # -------------------------------------------------
    
    def insert_returning(self, table: str, data: dict, returning: str) -> Any:
        """Insere um registro e retorna o valor da coluna especificada"""
        try:
            table_quoted = self._quote_identifier(table)
            cols = ", ".join([self._quote_identifier(k) for k in data.keys()])
            placeholders = ", ".join(["%s"] * len(data))
            returning_quoted = self._quote_identifier(returning)
            values = tuple(data.values())
            
            sql = f"""
                INSERT INTO {table_quoted} ({cols})
                VALUES ({placeholders})
                RETURNING {returning_quoted}
            """
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            return result[0] if result else None  # Retorna primeiro valor
            
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao inserir: {str(e)}")
    
    # -----------------------------
    # SELECT ONE (compatível com versões antigas e novas)
    # -----------------------------
    
    def fetch_one(self, table: str, key_or_conditions: Union[str, Dict[str, Any]], 
                  value: Any = None) -> Optional[Dict]:
        """
        Busca um registro.
        
        Modo antigo (compatibilidade):
            fetch_one("tabela", "id", 1)
        
        Modo novo:
            fetch_one("tabela", {"id": 1, "ativo": True})
        """
        try:
            table_quoted = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(key_or_conditions, value)
            
            sql = f"SELECT * FROM {table_quoted}{where_clause} LIMIT 1"
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            return dict(result) if result else None
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar: {str(e)}")
    
    # -----------------------------
    # SELECT ALL (compatível com versões antigas e novas)
    # -----------------------------
    
    def fetch_all(self, table: str, conditions: Union[Dict[str, Any], str, None] = None, 
                  value: Any = None, order_by: str = None) -> List[Dict]:
        """
        Busca todos os registros.
        
        Modo antigo (compatibilidade):
            fetch_all("tabela", "ativo", True)
        
        Modo novo:
            fetch_all("tabela", {"ativo": True})
            fetch_all("tabela", order_by="nome")
        """
        try:
            table_quoted = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(conditions, value)
            
            sql = f"SELECT * FROM {table_quoted}{where_clause}"
            
            if order_by:
                order_by_quoted = ", ".join([self._quote_identifier(col.strip()) 
                                           for col in order_by.split(",")])
                sql += f" ORDER BY {order_by_quoted}"
            
            self.cursor.execute(sql, values)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar: {str(e)}")
    
    # -----------------------------
    # UPDATE (compatível com versões antigas e novas)
    # -----------------------------
    
    def update(self, table: str, key_or_conditions: Union[str, Dict[str, Any]], 
               value_or_data: Any, data: dict = None) -> int:
        """
        Atualiza registros.
        
        Modo antigo (compatibilidade):
            update("tabela", "id", 1, {"nome": "Novo Nome"})
        
        Modo novo:
            update("tabela", {"id": 1}, {"nome": "Novo Nome"})
        """
        try:
            table_quoted = self._quote_identifier(table)
            
            # Determinar se é modo antigo ou novo
            if data is not None:
                # Modo antigo: key_or_conditions é string, value_or_data é o valor
                conditions = {key_or_conditions: value_or_data}
                update_data = data
            else:
                # Modo novo: key_or_conditions é dict, value_or_data é o data
                conditions = key_or_conditions if isinstance(key_or_conditions, dict) else {}
                update_data = value_or_data if isinstance(value_or_data, dict) else {}
            
            # Parte SET
            set_parts = [f"{self._quote_identifier(k)} = %s" for k in update_data.keys()]
            set_clause = ", ".join(set_parts) if set_parts else ""
            
            # Parte WHERE
            where_clause, where_values = self._build_where_clause(conditions)
            
            # Valores combinados (SET primeiro, WHERE depois)
            values = list(update_data.values()) + where_values
            
            if not set_clause:
                raise ValueError("Nenhum dado fornecido para atualização")
            
            sql = f"UPDATE {table_quoted} SET {set_clause}{where_clause}"
            self.cursor.execute(sql, values)
            return self.cursor.rowcount
            
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")
    
    # -----------------------------
    # DELETE (compatível com versões antigas e novas)
    # -----------------------------
    
    def delete(self, table: str, key_or_conditions: Union[str, Dict[str, Any]], 
               value: Any = None) -> int:
        """
        Remove registros.
        
        Modo antigo (compatibilidade):
            delete("tabela", "id", 1)
        
        Modo novo:
            delete("tabela", {"id": 1})
        """
        try:
            table_quoted = self._quote_identifier(table)
            where_clause, values = self._build_where_clause(key_or_conditions, value)
            
            sql = f"DELETE FROM {table_quoted}{where_clause}"
            self.cursor.execute(sql, values)
            return self.cursor.rowcount
            
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")
    
    # -----------------------------
    # EXECUTAR QUERY PERSONALIZADA
    # -----------------------------
    
    def execute_query(self, sql: str, params: Tuple = None) -> List[Dict]:
        """Executa uma query SQL personalizada"""
        try:
            self.cursor.execute(sql, params or ())
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na query: {str(e)}")
    
    # -----------------------------
    # COMMIT, ROLLBACK e CLOSE
    # -----------------------------
    
    def commit(self):
        """Confirma a transação"""
        try:
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao gravar no banco: {str(e)}")
    
    def rollback(self):
        """Reverte a transação"""
        try:
            self.conn.rollback()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao reverter: {str(e)}")
    
    def close(self):
        """Fecha cursor e conexão"""
        try:
            self.cursor.close()
        except:
            pass