#backend\backend\routers\upload.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from datetime import date

from backend.services.file_service import file_hash_exists, save_file_hash
from backend.utils.file_hash import generate_file_hash_stream

from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.services.log_importacao_service import LogImportacaoService
from backend.services.event_service import EventService
from backend.utils.file_validation import validate_upload_file
from backend.services.event_processor import EventProcessor


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db=Depends(get_db)):
    tipo = tipo.lower().strip()

    # 1. Validação do arquivo
    validate_upload_file(file)

    # 2. Geração do hash
    file_hash = generate_file_hash_stream(file.file)

    # 3. Reposiciona ponteiro
    file.file.seek(0)

    log_service = LogImportacaoService(db)
    event_service = EventService(db)

    # DUPLICADO
    if file_hash_exists(db, file_hash):
        log_service.criar_log({
            "nome_arquivo": file.filename,
            "qntd_registros": 0,
            "status": "ERRO",
            "msg_erro": "Arquivo já importado anteriormente",
            "usuario_id": 1
        })

        raise HTTPException(
            status_code=409,
            detail="Arquivo duplicado. Este arquivo já foi importado."
        )

    # IMPORTAÇÃO
    result = process_import(file, db, import_type=tipo)

    # 6. Salva hash somente se houver inserções
    if result.get("inserted", 0) > 0:
        save_file_hash(db, file.filename, file_hash)

     # 7. Log de sucesso ou parcial
    total_processados = result.get("inserted", 0) + result.get("rejected", 0)

    log = log_service.criar_log({
        "nome_arquivo": file.filename,
        "qntd_registros": total_processados,
        "status": "SUCESSO" if not result.get("errors") else "ERRO",
        "msg_erro": None if not result.get("errors") else "Importação com erros",
        "usuario_id": 1
    })

        
    event_id = event_service.criar_evento({
        "type": "SUCCESS",
        "context": {
            "state": "IMPORT_SUCCESS",
            "data": {
                "file_name": file.filename,
            },
        },
        "reference": {
            "id": log["id"],
            "type": "IMPORT",
        },
        "user_id": 1,
    })

    processor = EventProcessor(db)
    processor.processar_evento(event_id)
    
    # 8. Retorno
    return {
        "importacao": result,
        "duplicado": False,
        "log": log
    }