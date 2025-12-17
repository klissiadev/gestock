from fastapi import APIRouter, UploadFile, Depends
from datetime import date

from backend.services.file_service import file_hash_exists, save_file_hash
from backend.utils.file_hash import generate_file_hash_stream

from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.services.log_importacao_service import LogImportacaoService
from backend.utils.file_validation import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db=Depends(get_db)):
    # 1. Valida arquivo
    validate_upload_file(file)

    # 2. Gera hash
    file_hash = generate_file_hash_stream(file.file)

    # 3. Verifica duplicidade (AVISO, não bloqueia)
    is_duplicate = file_hash_exists(db, file_hash)

    # volta ponteiro
    file.file.seek(0)

    # 4. Processa importação
    result = process_import(file, db, import_type=tipo)

    # 5. Salva hash somente se houve inserções
    if result.get("inserted", 0) > 0:
        save_file_hash(db, file.filename, file_hash)

    # 6. Cria log
    log_service = LogImportacaoService(db)

    total_processados = result.get("inserted", 0) + result.get("rejected", 0)

    log_data = {
        "nome_arquivo": file.filename,
        "qntd_registros": total_processados,
        "data_importacao": date.today(),
        "status": "SUCESSO" if not result.get("errors") else "PARCIAL",
        "msg_erro": (
            "Arquivo duplicado importado novamente"
            if is_duplicate
            else None
        ),
        "id_usuario": 1
    }

    log = log_service.criar_log(log_data)

    # 7. Retorno completo
    return {
        "importacao": result,
        "duplicado": is_duplicate,
        "log": log
    }
