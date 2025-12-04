# app/routes/upload.py
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.base import SessionLocal
from utils.file_validation import validate_upload_file
from services.parser_service import process_and_insert

router = APIRouter(prefix="/upload", tags=["upload"])

# conexão com o PostgreSQL por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# recebe o arquivo enviado pelo usuário
@router.post("/", summary="Upload e processamento de CSV/XLSX")
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="Arquivo não enviado.")

    # Validação básica (extensão, tamanho)
    validate_upload_file(file)

    # processa e insere
    result = process_and_insert(file, db)
    return result
