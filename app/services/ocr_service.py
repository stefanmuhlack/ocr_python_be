import logging
from PIL import Image
from pytesseract import image_to_string

class OCRService:
    @staticmethod
    def process_image(image_path):
        # Load the image from the path
        img = Image.open(image_path)
        # Convert the image to grayscale for better OCR accuracy
        img = img.convert('L')
        # Return the OCR result
        return image_to_string(img)
