from fastapi import APIRouter, UploadFile, HTTPException
from pdf2image import convert_from_bytes

router = APIRouter()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = UploadFile(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    contents = await file.read()
    try:
        images = convert_from_bytes(contents)
        return {"message": f"Processed {len(images)} pages from the PDF."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

