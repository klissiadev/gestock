#backend\backend\routers\upload.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from datetime import date
from uuid import UUID

from backend.services.file_service import file_hash_exists, save_file_hash
from backend.utils.file_hash import generate_file_hash_stream
from typing import Annotated
from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.services.log_importacao_service import LogImportacaoService
from backend.services.event_service import EventService
from backend.services.stock_event_service import StockEventService
from backend.services.notification_service import NotificationService
from backend.database.repository import Repository
from backend.utils.file_validation import validate_upload_file
from backend.database.schemas import NotificationEventCreate


from auth_module.utils.security import require_role
from auth_module.models.User import UserPublic

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/{tipo}")
def upload_file(tipo: str, 
                file: UploadFile, 
                user: Annotated[UserPublic, Depends(require_role(["gestor"]))],
                db=Depends(get_db)
            ):
    tipo = tipo.lower().strip()

    print(f"id do usr: {user.id}")

    # 1. Validação do arquivo
    validate_upload_file(file)

    # 2. Geração do hash
    file_hash = generate_file_hash_stream(file.file)

    # 3. Reposiciona ponteiro
    file.file.seek(0)

    log_service = LogImportacaoService(db)

    # DUPLICADO
    if file_hash_exists(db, file_hash):
        log_service.criar_log({
            "nome_arquivo": file.filename,
            "qntd_registros": 0,
            "status": "ERRO",
            "msg_erro": "Arquivo já importado anteriormente",
            "user_id": UUID(f'{user.id}')
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
        "user_id": UUID(f'{user.id}')
    })

    event_service = EventService(db)

    event = NotificationEventCreate(
        type="SUCCESS",
        context={
            "state": "IMPORT_SUCCESS",
            "data": {
                "file_name": file.filename,
                "inserted": result.get("inserted", 0),
                "rejected": result.get("rejected", 0)
            }
        },
        reference={
            "id": log["id"],
            "type": "IMPORT"
        }
    )

    event_id = event_service.criar_evento(event, user.id)

    # verifica ruptura após importação
    stock_service = StockEventService(
        Repository(db),
        event_service
    )

    stock_service.check_stock_events(user.id)

    # gera notificações
    notification_service = NotificationService(db)
    notification_service.processar_evento_para_todos(event_id)

    print(log)
    
    # 8. Retorno
    return {
        "importacao": result,
        "duplicado": False,
        "log": log
    }