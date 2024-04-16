import pytesseract
import logging
from PIL import Image, ImageFilter, ImageEnhance

logger = logging.getLogger(__name__)

def process_image_with_tesseract(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        
        # Preprocessing steps to enhance image for better OCR accuracy
        img = img.convert('L')  # Convert to grayscale
        img = img.filter(ImageFilter.MedianFilter())  # Apply median filter
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # Increase contrast
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen image
        
        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        logger.error(f"Error processing image with Tesseract: {e}")
        return None
