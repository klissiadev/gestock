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
    # upload_file: FastAPI UploadFile
    filename = upload_file.filename
    if not has_allowed_extension(filename):
        raise HTTPException(status_code=400, detail="Extensão inválida. Somente .csv e .xlsx são aceitos.")

    # Verifica tamanho do conteúdo de forma segura:
    # Alguns frameworks não disponibilizam tamanho direto; vamos ler até max_size+1 bytes
    upload_file.file.seek(0)
    content = upload_file.file.read(max_size_bytes + 1)
    size = len(content)
    upload_file.file.seek(0)  # reset para que outro leitor possa ler do início

    if size > max_size_bytes:
        raise HTTPException(status_code=413, detail=f"Arquivo muito grande (máx {max_size_bytes} bytes).")

    # opcional: checar mime-type se estiver disponível
    mime = getattr(upload_file, "content_type", None)
    if mime and mime not in ALLOWED_MIME_TYPES:
        # nem sempre confiável, então não bloqueamos somente por mime, mas avisamos/logamos
        # mas podemos bloquear se quiser: raise HTTPException(...)
        pass

    return True
