import os

UPLOAD_DIR = "uploaded_pdfs"

@router.post("/upload/")
async def upload_pdf(file: UploadFile = UploadFile(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    contents = await file.read()
    try:
        images = convert_from_bytes(contents)
        for idx, image in enumerate(images):
            image_path = os.path.join(UPLOAD_DIR, f"{file.filename}_page_{idx + 1}.png")
            image.save(image_path)
        return {"message": f"Processed {len(images)} pages from the PDF and saved them to {UPLOAD_DIR}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
