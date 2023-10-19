import pytesseract
import logging
from PIL import Image

logger = logging.getLogger(__name__)

def process_image_with_tesseract(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        logger.error(f"Error processing image with Tesseract: {e}")
        return None
# Add Paddle processing and other OCR functions...
# Path: app/ocr_processing.py
