from fastapi import HTTPException
from backend.database.repository import Repository

from backend.database.schemas import IMPORT_SCHEMAS 
from backend.services.validation_service import validate_row 


class MovimentacaoService:

    def __init__(self, conn):
        self.repo = Repository(conn)

    # =========================
    # ENTRADA
    # =========================
    def registrar_entrada(self, dados: dict):
        ok = self.repo.insert(
            "app_core.movimentacoes_entrada",
            dados
        )
        if not ok:
            raise HTTPException(
                status_code=400,
                detail="Erro ao registrar entrada de produto."
            )

        self.repo.commit()
        return {"message": "Entrada registrada com sucesso"}

    def listar_entradas(self):
        sql = """
            SELECT *
            FROM app_core.movimentacoes_entrada
            ORDER BY created_at DESC
        """
        self.repo.cursor.execute(sql)
        return self.repo.cursor.fetchall()

    # =========================
    # SAÍDA
    # =========================
    def registrar_saida(self, dados: dict):
        ok = self.repo.insert(
            "app_core.movimentacoes_saida",
            dados
        )
        if not ok:
            raise HTTPException(
                status_code=400,
                detail="Erro ao registrar saída de produto."
            )

        self.repo.commit()
        return {"message": "Saída registrada com sucesso"}

    def listar_saidas(self):
        sql = """
            SELECT *
            FROM app_core.movimentacoes_saida
            ORDER BY created_at DESC
        """
        self.repo.cursor.execute(sql)
        return self.repo.cursor.fetchall()

    # =========================
    # MOVIMENTAÇÃO INTERNA 
    # =========================
    def registrar_movimentacao_interna(self, dados: dict):

        # VALIDAÇÃO ACONTECE AQUI
        schema = IMPORT_SCHEMAS["movimentacoes_internas"]
        erros = validate_row(dados, schema)

        if erros:
            raise HTTPException(
                status_code=422,
                detail=erros
            )

        ok = self.repo.insert(
            "app_core.movimentacoes_internas",
            dados
        )

        if not ok:
            raise HTTPException(
                status_code=400,
                detail="Erro ao registrar movimentação interna."
            )

        self.repo.commit()
        return {"message": "Movimentação interna registrada com sucesso"}