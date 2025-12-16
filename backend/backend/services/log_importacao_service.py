from fastapi import HTTPException
from backend.database.repository import Repository

class LogImportacaoService:
    def __init__(self, conn):
        self.repo = Repository(conn)

    def criar_log(self, log_data: dict):
        try:
            new_id = self.repo.insert_returning(
                "LogImportacao",
                log_data,
                "id_log_importacao"
            )

            if not new_id:
                raise HTTPException(
                    status_code=400,
                    detail="Erro ao criar log de importação"
                )

            self.repo.commit()

            # Busca o log recém-criado
            log = self.repo.fetch_one(
                "LogImportacao",
                "id_log_importacao",
                new_id
            )

            return log

        except Exception as e:
            self.repo.conn.rollback()
            import traceback
            traceback.print_exc()
            raise


    def listar_logs(self):
        try:
            return self.repo.fetch_all("LogImportacao")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def buscar_por_id(self, log_id: int):
        try:
            log = self.repo.fetch_one("LogImportacao", "id_log_importacao", log_id)
            if not log:
                raise HTTPException(status_code=404, detail="Log não encontrado")
            return log
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def atualizar_log(self, log_id: int, dados_atualizacao: dict):
        try:
            ok = self.repo.update("LogImportacao", "id_log_importacao", log_id, dados_atualizacao)
            if not ok:
                raise HTTPException(status_code=400, detail="Erro ao atualizar log")
            self.repo.commit()
            return {"message": "Log atualizado com sucesso"}
        except Exception as e:
            self.repo.conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def deletar_log(self, log_id: int):
        try:
            ok = self.repo.delete("LogImportacao", "id_log_importacao", log_id)
            if not ok:
                raise HTTPException(status_code=400, detail="Erro ao deletar log")
            self.repo.commit()
            return {"message": "Log deletado com sucesso"}
        except Exception as e:
            self.repo.conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))