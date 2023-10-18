import pytesseract
from PIL import Image

def process_image_with_tesseract(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        print(f"Error processing image with Tesseract: {e}")
        return None
# Add Paddle processing and other OCR functions...
