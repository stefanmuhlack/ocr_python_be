from PyPDF2 import PdfReader
import os
from fastapi import HTTPException, UploadFile
from typing import List
import logging

logger = logging.getLogger(__name__)

def save_pdf(file: UploadFile, target_dir: str) -> str:
    """Save the uploaded PDF file to the target directory."""
    try:
        file_path = os.path.join(target_dir, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        return file_path
    except OSError as e:
        logger.error(f'OS error: {e}')
        raise HTTPException(status_code=500, detail='OS error occurred while saving the file.')
    except Exception as e:
        logger.error(f'Failed to save PDF: {e}')
        raise HTTPException(status_code=500, detail='Unable to save file due to server error.')

def read_pdf(file_path: str) -> List[str]:
    """Read the text content from the PDF file."""
    try:
        reader = PdfReader(file_path)
        text = [page.extract_text() for page in reader.pages]
        return text
    except Exception as e:
        logger.error(f'Failed to read PDF: {e}')
        raise HTTPException(status_code=500, detail='Unable to read file due to server error.')

    try:
        reader = PdfReader(file_path)
        text = [page.extract_text() for page in reader.pages]
        return text
    except Exception as e:
        logger.error(f'Failed to read PDF: {e}')
        raise HTTPException(status_code=500, message='Unable to read file due to server error.')

