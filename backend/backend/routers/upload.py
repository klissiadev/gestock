
from backend.services.log_importacao_service import LogImportacaoService
from datetime import datetime

@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db = Depends(get_db)):
    validate_upload_file(file)
    
    # Processa a importação
    result = process_import(file, db, import_type=tipo)
    
    # Cria log da importação (você precisa obter o id_usuario de alguma forma)
    log_service = LogImportacaoService(db)
    log_data = {
        "nome_arquivo": file.filename,
        "qntd_registros": result.get("registros_processados", 0),
        "data_importacao": date.today(),
        "status": "SUCESSO" if not result.get("erros") else "PARCIAL",
        "msg_erro": result.get("erro_geral"),
        "id_usuario": 1  # Substitua pelo ID real do usuário
    }
    
    log_service.criar_log(log_data)
    log_service.repo.commit()
    
    return result