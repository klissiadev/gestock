
from admin_module.pydantic.logs_model import UserFetchRequest

class UserService:
    def __init__(self, db_pool):
        self.db_pool = db_pool # Recebe uma pool de conexões já configurada e pronta para uso
    
    def delete_user(self, user_id: str):
        """Deleta um usuário do banco de dados com base no ID fornecido."""
        with self.db_pool.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE app_core.usuarios SET ativo = false WHERE id = %s", (user_id,))
                linhas_afetadas = cur.rowcount
            conn.commit()
        return linhas_afetadas > 0
        
    
    def fetch_all_users():
        """Busca os usuarios dentro do banco de dados.
        Retorna: dicionario com eles """
        with self.db_pool.get_db_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                data = cur.execute("SELECT nome, papel, email, created_at FROM app_core.usuarios WHERE ativo = %s", (True)).fetchall()
                return data
    
    def fetch_user_by_filter(filter: UserFetchRequest):
         """Busca os usuarios dentro do banco de dados.
         Retorna: dicionario com eles """
         with self.db_pool.get_db_connection() as conn:
             with conn.cursor(row_factory=dict_row) as cur:
                 query = "SELECT nome, papel, email, created_at FROM app_core.usuarios WHERE ativo = %s"
                 params = [True]

                 if filter.nome:
                     query += " AND nome ILIKE %s"
                     params.append(f"%{filter.nome}%")

                 if filter.email:
                     query += " AND email ILIKE %s"
                     params.append(f"%{filter.email}%")

                 data = cur.execute(query, tuple(params)).fetchall()
                 return data
             
            