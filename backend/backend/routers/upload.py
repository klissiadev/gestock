from fastapi import APIRouter, UploadFile, Depends
from datetime import date

from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.services.log_importacao_service import LogImportacaoService
from backend.utils.file_validation import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db=Depends(get_db)):
    # Valida o arquivo
    validate_upload_file(file)

    # Processa a importação
    result = process_import(file, db, import_type=tipo)

    # Cria log da importação
    log_service = LogImportacaoService(db)

    log_data = {
        "nome_arquivo": file.filename,
        "qntd_registros": result.get("registros_processados", 0),
        "data_importacao": date.today(),
        "status": "SUCESSO" if not result.get("erros") else "PARCIAL",
        "msg_erro": result.get("erro_geral"),
        "id_usuario": 1  # TODO: substituir pelo usuário autenticado
    }

    # 🔹 cria o log e RECEBE o log criado
    log = log_service.criar_log(log_data)

    return log