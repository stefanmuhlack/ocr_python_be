from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from ..services.pdf_service import save_pdf, read_pdf
from ..security.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    try:
        file_path = await save_pdf(file, './uploads')
        return {'status': 'success', 'message': 'PDF uploaded successfully', 'path': file_path}
    except Exception as e:
        logger.error(f'Failed to upload PDF: {e}')
        raise HTTPException(status_code=500, detail='Unable to upload PDF due to server error')

@router.get("/get-pdf-text")
async def get_pdf_text(file_path: str):
    try:
        text = read_pdf(file_path)
        return {'status': 'success', 'text': text}
    except Exception as e:
        logger.error(f'Failed to read PDF: {e}')
        raise HTTPException(status_code=500, detail='Unable to retrieve text from PDF due to server error')

