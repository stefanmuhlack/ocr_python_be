import logging
import os
from fastapi import FastAPI, Depends
from services.ocr_service import OCRService
from services.pdf_service import PDFService

app = FastAPI()

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include OCR and PDF service routers
app.include_router(OCRService.router, prefix="/ocr", tags=["OCR Operations"])
app.include_router(PDFService.router, prefix="/pdf", tags=["PDF Management"])

# Setup directory constants for file storage
TEMPLATES_DIR = "templates"
IMAGES_DIR = "generated_images"

# Ensure directories exist
for directory in [TEMPLATES_DIR, IMAGES_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(directory):
        os.makedirs(directory)

# OCR Request Model
class OCRRequest(BaseModel):
    template_name: str
    rectangles: list

# Include routers
app.include_router(PDFService.router, prefix="/pdf", tags=["pdf"])
app.include_router(OCRService.router, prefix="/template", tags=["template"])

# Separate OCR and PDF handling in respective services for better modularity
