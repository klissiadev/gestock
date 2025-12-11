from fastapi import HTTPException
from backend.database.repository import Repository


class ProdutoService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_produto(self, produto: dict):
        ok = self.repo.insert("produtos", produto)
        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao inserir produto.")
        self.repo.commit()
        return {"message": "Produto criado com sucesso"}

    def listar_produtos(self):
        cursor = self.repo.cursor
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()
