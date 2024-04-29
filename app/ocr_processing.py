import pytesseract
import logging
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np
from layoutparser import Detectron2LayoutModel

logger = logging.getLogger(__name__)

def preprocess_for_ocr(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Noise removal with iterative bilateral filter (less blur)
    filtered_image = cv2.bilateralFilter(thresh_image, 9, 75, 75)
    return filtered_image

def process_image_with_tesseract(image):
    try:
        # Preprocess image for better OCR results
        preprocessed_image = preprocess_for_ocr(image)
        # OCR using Tesseract
        text = pytesseract.image_to_string(preprocessed_image, lang='eng')
        return text
    except Exception as e:
        logger.error(f"Error processing image with Tesseract: {e}")
        return None

def process_image_with_layoutparser(image):
    try:
        # Preprocess image
        preprocessed_image = preprocess_for_ocr(image)
        # Initialize LayoutParser model
        model = Detectron2LayoutModel(
            config_path='lp://PubLayNet/config',
            label_map={0: 'Text', 1: 'Title', 2: 'List', 3: 'Table', 4: 'Figure'},
            extra_config=['MODEL.ROI_HEADS.SCORE_THRESH_TEST', 0.5, 'MODEL.DEVICE', 'cuda']
        )
        # Detect layout
        layout = model.detect(preprocessed_image)
        # Extract text blocks
        text_blocks = [pytesseract.image_to_string(block.region_image(preprocessed_image), lang='eng') for block in layout]
        return ' '.join(text_blocks)
    except Exception as e:
        logger.error(f"Error processing image with LayoutParser: {e}")
        return None

