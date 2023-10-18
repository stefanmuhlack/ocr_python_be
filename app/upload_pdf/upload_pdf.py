@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = UploadFile(...)):
    print("Received PDF upload request")
    if file.filename.endswith(".pdf"):
        contents = await file.read()
        try:
            images = convert_from_bytes(contents)
            # Save metadata to the database
            insert_pdf_metadata(file.filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return {"message": f"Processed {len(images)} pages from the PDF."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
