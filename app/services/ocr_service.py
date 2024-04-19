import logging
from PIL import Image
from pytesseract import image_to_string
from abc import ABC, abstractmethod

class OCRServiceInterface(ABC):
    @abstractmethod
    def process_image(self, image_path):
        pass

class TesseractOCRService(OCRServiceInterface):
    def process_image(self, image_path):
        # Load the image from the path
        img = Image.open(image_path)
        # Convert the image to grayscale for better OCR accuracy
        img = img.convert('L')
        # Return the OCR result
        return image_to_string(img)
