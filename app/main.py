import logging
import json
import os
from datetime import datetime
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from pdf2image import convert_from_bytes

# Config and database imports
from app.config import Config
from app.database import insert_pdf_metadata

# Separate services
from services.ocr_service import OCRService
from services.pdf_service import PDFService

app = FastAPI()

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory constants
TEMPLATES_DIR = "templates"
IMAGES_DIR = "generated_images"

# Ensure directories exist
for directory in [TEMPLATES_DIR, IMAGES_DIR]:
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
