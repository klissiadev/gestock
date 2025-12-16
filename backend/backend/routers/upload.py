from fastapi import APIRouter, UploadFile, Depends, HTTPException
from datetime import date

from backend.services.file_service import file_hash_exists, save_file_hash
from backend.utils.file_hash import generate_file_hash_stream

from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.services.log_importacao_service import LogImportacaoService
from backend.utils.file_validation import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/produtos")
def upload_produtos(file: UploadFile, db=Depends(get_db)):
    return upload_file("produtos", file, db)

# recebe um arquivo de movimentacoes
@router.post("/movimentacoes")
def upload_movimentacoes(file: UploadFile, db=Depends(get_db)):
    return upload_file("movimentacoes", file, db)

@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db=Depends(get_db)):
    # Valida o arquivo
    validate_upload_file(file)

    # gera hash em streaming
    file_hash = generate_file_hash_stream(file.file)

    # verifica duplicidade
    if file_hash_exists(db, file_hash):
        raise HTTPException(
            status_code=409,
            detail="Arquivo duplicado. Este arquivo já foi importado."
        )
    
    # volta o ponteiro
    file.file.seek(0)

    # Processa a importação
    result = process_import(file, db, import_type=tipo)

    # salva hash somente se sucesso
    if not result.get("errors"):
        save_file_hash(db, file.filename, file_hash)

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

    # cria o log e RECEBE o log criado
    log = log_service.criar_log(log_data)

    return log