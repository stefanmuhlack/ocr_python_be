from PyPDF2 import PdfReader
import os
from fastapi import HTTPException, UploadFile
from typing import List
import logging

logger = logging.getLogger(__name__)

def save_pdf(file: UploadFile, target_dir: str) -> str:
    try:
        file_path = os.path.join(target_dir, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        return file_path
    except Exception as e:
        logger.error(f'Failed to save PDF: {e}')
        raise HTTPException(status_code=500, message='Unable to save file due to server error.')

def read_pdf(file_path: str) -> List[str]:
    try:
        reader = PdfReader(file_path)
        text = [page.extract_text() for page in reader.pages]
        return text
    except Exception as e:
        logger.error(f'Failed to read PDF: {e}')
        raise HTTPException(status_code=500, message='Unable to read file due to server error.')

