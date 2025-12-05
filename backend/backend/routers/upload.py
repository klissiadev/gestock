from fastapi import APIRouter, UploadFile, Depends, HTTPException
from backend.database.base import get_db
from backend.utils.file_validation import validate_upload_file
from backend.services.parser_service import process_and_insert

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/", summary="Upload e processamento CSV/XLSX")
def upload_file(file: UploadFile, db = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="Arquivo não enviado.")

    validate_upload_file(file)

    result = process_and_insert(file, db)
    return result