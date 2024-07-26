import os
import logging
from fastapi import APIRouter, UploadFile, HTTPException
from pdf2image import convert_from_bytes

router = APIRouter()
UPLOAD_DIR = "uploaded_pdfs"
logger = logging.getLogger(__name__)

@router.post("/upload/")
async def upload_pdf(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    contents = await file.read()
    try {
        images = convert_from_bytes(contents)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for idx, image in enumerate(images):
            image_path = os.path.join(UPLOAD_DIR, f"{file.filename}_page_{idx + 1}.png")
            image.save(image_path)
        logger.info(f"Processed {len(images)} pages from {file.filename} and saved to {UPLOAD_DIR}.")
        return {"message": f"Processed {len(images)} pages from the PDF and saved them to {UPLOAD_DIR}."}
    } except (Exception as e) {
        logger.error(f"Failed to process PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    }

