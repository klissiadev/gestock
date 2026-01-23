#backend\backend\services\log_importacao_service.py
from fastapi import HTTPException
from backend.database.repository import Repository

class LogImportacaoService:
    TABLE_NAME = "app_logs.importacoes"
    SCHEMA = "app_logs"

    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_log(self, log_data: dict):
        try:
            new_id = self.repo.insert_returning(
                self.TABLE_NAME,
                log_data,
                "id"
            )

            if not new_id:
                raise HTTPException(
                    status_code=400,
                    detail="Erro ao criar log de importação"
                )

            self.repo.commit()

            log = self.repo.fetch_one(
                table="importacoes",
                key_or_conditions="id",
                value=new_id,
                schema=self.SCHEMA
                )

            return log

        except Exception:
            self.repo.conn.rollback()
            raise

    def listar_logs(self):
        return self.repo.fetch_all(self.TABLE_NAME)

    def buscar_por_id(self, log_id: int):
        log = self.repo.fetch_one(self.TABLE_NAME, "id", log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log não encontrado")
        return log

    def atualizar_log(self, log_id: int, dados_atualizacao: dict):
        ok = self.repo.update(self.TABLE_NAME, "id", log_id, dados_atualizacao)
        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao atualizar log")
        self.repo.commit()
        return {"message": "Log atualizado com sucesso"}

    def deletar_log(self, log_id: int):
        ok = self.repo.delete(self.TABLE_NAME, "id", log_id)
        if not ok:
            raise HTTPException(status_code=400, detail="Erro ao deletar log")
        self.repo.commit()
        return {"message": "Log deletado com sucesso"}