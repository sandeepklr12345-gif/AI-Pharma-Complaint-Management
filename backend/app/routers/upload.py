from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas import UploadResponse
from app.services.text_extraction import extract_text

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_complaint_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        text, file_type = extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text:
        raise HTTPException(status_code=422, detail="No extractable text found in file")

    return UploadResponse(text=text, file_type=file_type)
