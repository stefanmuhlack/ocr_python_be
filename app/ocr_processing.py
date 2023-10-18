import pytesseract
from PIL import Image

def process_image_with_tesseract(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Add Paddle processing and other OCR functions...
