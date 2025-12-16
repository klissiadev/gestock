from fastapi import HTTPException
import os

# lista de extensões permitidas
ALLOWED_EXTENSIONS = {"csv", "xlsx"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # alguns navegadores podem usar: application/vnd.ms-excel for .xls
}

def has_allowed_extension(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def validate_upload_file(upload_file, max_size_bytes: int = 5 * 1024 * 1024):

    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="Arquivo inválido.")

    # verifica extensão
    filename = upload_file.filename
    if not has_allowed_extension(filename):
        raise HTTPException(status_code=400, detail="Extensão inválida. Somente .csv e .xlsx são aceitos.")
    
    # leitura do arquivo
    upload_file.file.seek(0) # inicio do arquivo
    content = upload_file.file.read(max_size_bytes + 1) # limite de leitura
    size = len(content) # tamanho do que foi lido
    upload_file.file.seek(0)  # reset para que outro leitor possa ler do início

    # verifica se o arquivo está vazio
    if size == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    # rejeita se passar do limite
    if size > max_size_bytes:
        raise HTTPException(status_code=413, detail=f"Arquivo muito grande (máx {max_size_bytes} bytes).")

    # opcional: checar mime-type se estiver disponível
    mime = getattr(upload_file, "content_type", None)
    if mime and mime not in ALLOWED_MIME_TYPES:
        # nem sempre confiável, então não bloqueamos somente por mime, mas avisamos/logamos
        # mas podemos bloquear se quiser: raise HTTPException(...)
        pass

    return True
