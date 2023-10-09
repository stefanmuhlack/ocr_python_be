from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from pdf2image import convert_from_bytes
from app.routers import pdf, template  # Ensure this import is correct
import logging


app = FastAPI()

class Config:
    HD_SCREEN_SIZE = (1920, 1080)
    POPPLER_PATH = r"C:\Program Files\Poppler R23.08.0-0\poppler-23.08.0\Library\bin"  # This should be made configurable

class OCRRequest(BaseModel):
    template_name: str
    rectangles: List[Dict]

# Include routers
app.include_router(pdf.router, prefix="/pdf", tags=["pdf"])
app.include_router(template.router, prefix="/template", tags=["template"])

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = UploadFile(...)):
    print("Received PDF upload request")
    if file.filename.endswith(".pdf"):
        contents = await file.read()
        try:
            images = convert_from_bytes(contents)
            # You can save these images or process them further
            # For now, let's just return the number of pages processed
            return {"message": f"Processed {len(images)} pages from the PDF."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")



@app.post("/save-template/")
async def save_template(template_name: str, template_data: dict):
    try:
        with open(f"templates/{template_name}.json", "w") as f:
            json.dump(template_data, f)
        return {"message": "Template saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-template/")
async def get_template(template_name: str):
    try:
        with open(f"templates/{template_name}.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(pdf.router, prefix="/pdf", tags=["pdf"])
app.include_router(template.router, prefix="/template", tags=["template"])


@app.post("/process_ocr/")  # This is the URL path for the new route
async def process_ocr(request: OCRRequest):
    template_name = request.template_name
    rectangles = request.rectangles

    # Process the data, for example, save it to a file
    # You can use the rectangles and template_name here

    return {"message": "Data processed successfully!"}


