import logging
import json
import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from pdf2image import convert_from_bytes
from app.config import Config
from app.database import insert_pdf_metadata
from app.ocr_processing import process_image_with_tesseract
from app.routers import pdf, template

app = FastAPI()

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMPLATES_DIR = "templates"
IMAGES_DIR = "generated_images"

# Ensure the directories exist during application startup
for directory in [TEMPLATES_DIR, IMAGES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class OCRRequest(BaseModel):
    template_name: str
    rectangles: List[Dict]

# Include routers
app.include_router(pdf.router, prefix="/pdf", tags=["pdf"])
app.include_router(template.router, prefix="/template", tags=["template"])

def extract_data_from_ocr(ocr_text, rectangles):
    extracted_data = {}
    for rect in rectangles:
        # Assuming rectangles are defined by top-left and bottom-right coordinates
        top_left, bottom_right = rect['top_left'], rect['bottom_right']
        # Extract the text within this rectangle from the OCR results
        # This is a simplified extraction and may need further refinement
        extracted_data[rect['name']] = ocr_text[top_left[1]:bottom_right[1]][top_left[0]:bottom_right[0]]
    return extracted_data

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = UploadFile(...), upload_date: datetime = Depends(datetime.now)):
    logger.info("Received PDF upload request")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    contents = await file.read()

    # Convert PDF to images and save them
    images = convert_from_bytes(contents)
    image_paths = []
    for idx, image in enumerate(images):
        image_path = os.path.join(IMAGES_DIR, f"{file.filename}_page_{idx + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    # Store metadata in the database
    insert_pdf_metadata(file.filename, upload_date)

    return {"message": f"Processed {len(images)} pages from the PDF.", "image_paths": image_paths}

@app.post("/save-template/")
async def save_template(template_name: str, template_data: dict):
    try:
        with open(os.path.join(TEMPLATES_DIR, f"{template_name}.json"), "w") as f:
            json.dump(template_data, f)
        return {"message": "Template saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-template/")
async def get_template(template_name: str):
    try:
        with open(os.path.join(TEMPLATES_DIR, f"{template_name}.json"), "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_ocr/")
async def process_ocr(request: OCRRequest):
    template_name = request.template_name
    rectangles = request.rectangles

    # Retrieve the list of image paths for the uploaded PDF
    # For this example, we'll assume the images are named in a specific format
    # This can be refined based on your actual storage and naming convention
    image_paths = [os.path.join(IMAGES_DIR, f"{template_name}_page_{i + 1}.png") for i in range(len(rectangles))]

    # Process images using OCR
    ocr_results = []
    for image_path in image_paths:
        ocr_text = process_image_with_tesseract(image_path)
        ocr_results.append(ocr_text)

    # Extract data based on OCR results and template data
    all_extracted_data = []
    for ocr_text in ocr_results:
        extracted_data = extract_data_from_ocr(ocr_text, rectangles)
        all_extracted_data.append(extracted_data)

    return {"message": "Data processed successfully!", "extracted_data": all_extracted_data}
