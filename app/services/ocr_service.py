import cv2
import numpy as np
from layoutparser import Detectron2LayoutModel
from pytesseract import image_to_string
from paddleocr import PaddleOCR
import cv2
import numpy as np
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def preprocess_image_for_ocr(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV) # Thresholding to enhance contrast
    return thresh

def process_ocr(image_data: bytes) -> dict:
    try:
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        preprocessed_image = preprocess_image_for_ocr(image)
        # Detect layout using LayoutParser
        layout_model = Detectron2LayoutModel('lp://PubLayNet', config={'score_thresh': 0.85})
        layout = layout_model.detect(preprocessed_image)
        # Extract text using Tesseract
        tesseract_text = image_to_string(preprocessed_image, lang='eng')
        # Recognize text using PaddleOCR
        paddle_ocr = PaddleOCR()
        paddle_results = paddle_ocr.ocr(preprocessed_image, cls=True)
        return {'layout': layout, 'tesseract_text': tesseract_text, 'paddle_results': paddle_results}
    except Exception as e:
        logger.error(f'OCR processing failed: {e}')
        raise HTTPException(status_code=500, detail='Failed to process OCR due to server error')

