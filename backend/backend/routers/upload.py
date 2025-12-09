from fastapi import APIRouter, UploadFile, Depends
from backend.database.base import get_db
from backend.services.import_service import process_import
from backend.utils.file_validation import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/{tipo}")
def upload_file(tipo: str, file: UploadFile, db=Depends(get_db)):
    validate_upload_file(file)
    result = process_import(file, db, import_type=tipo)
    return result
