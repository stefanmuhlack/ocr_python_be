import logging
from PIL import Image
from pytesseract import image_to_string
from layoutparser import LayoutParser
from abc import ABC, abstractmethod

class OCRServiceInterface(ABC):
    @abstractmethod
    def process_image(self, image_path):
        pass

class LayoutParserOCRService(OCRServiceInterface):
    def __init__(self):
        self.layout_parser = LayoutParser()

    def process_image(self, image_path):
        # Load the image from the path
        img = Image.open(image_path)
        # Convert the image to grayscale for better OCR accuracy
        img = img.convert('L')
        # Use LayoutParser to find text blocks
        layout = self.layout_parser.detect(img)
        text_blocks = [image_to_string(block) for block in layout.get_blocks()]
        # Return concatenated OCR results from text blocks
        return ' '.join(text_blocks)
