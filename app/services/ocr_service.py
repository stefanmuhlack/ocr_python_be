import cv2
import numpy as np
from layoutparser import Detectron2LayoutModel
from fastapi import HTTPException
import pytesseract
from paddleocr import PaddleOCR
import logging

logger = logging.getLogger(__name__)

def perform_ocr(image_path: str) -> dict:
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise HTTPException(status_code=400, detail='Image not found or unreadable')
        # Preprocess the image for better OCR accuracy
        preprocessed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        preprocessed_image = cv2.threshold(preprocessed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Initialize OCR models
        layout_model = Detectron2LayoutModel(config_path='lp://PubLayNet/config', label_map={0: 'Text', 1: 'Title', 2: 'List', 3: 'Table', 4: 'Figure'}, extra_config=['MODEL.ROI_HEADS.SCORE_THRESH_TEST', 0.5, 'MODEL.DEVICE', 'cuda'])
        layout = layout_model.detect(preprocessed_image)
        # Perform OCR with Tesseract
        tesseract_text = pytesseract.image_to_string(preprocessed_image, config='--psm 6')
        # Perform OCR with PaddleOCR
        paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')
        paddle_results = paddle_ocr.ocr(preprocessed_image, cls=True)
        results = {'layout': layout, 'tesseract_text': tesseract_text, 'paddle_results': paddle_results}
        return results
    except HTTPException as e:
        logger.error(f'OCR service error: {e.detail}')
        raise
    except Exception as e:
        logger.error(f'Unexpected error in OCR service: {str(e)}')
        raise HTTPException(status_code=500, detail='Internal server error during OCR processing')

