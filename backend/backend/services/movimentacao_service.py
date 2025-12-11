from fastapi import HTTPException
from backend.database.repository import Repository


class MovimentacaoService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    def registrar_movimentacao(self, mov: dict):
        ok = self.repo.insert("movimentacoes", mov)
        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao inserir movimentação.")
        self.repo.commit()
        return {"message": "Movimentação registrada com sucesso"}

    def listar_movimentacoes(self):
        cursor = self.repo.cursor
        cursor.execute("SELECT * FROM movimentacoes ORDER BY data DESC")
        return cursor.fetchall()
