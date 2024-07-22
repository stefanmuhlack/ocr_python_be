import logging
from .ocr_processing import preprocess_for_ocr, process_image_with_tesseract, process_image_with_layoutparser, process_image_with_paddleocr
from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.ocr_tesseract = True
        self.ocr_layoutparser = True
        self.ocr_paddleocr = PaddleOCR()

    def process_image(self, image_data, methods=['tesseract', 'layoutparser', 'paddleocr']):
        """Process image using specified OCR methods."""
        try:
            preprocessed_image = preprocess_for_ocr(image_data)
            results = {}
            if 'tesseract' in methods:
                results['tesseract'] = process_image_with_tesseract(preprocessed_image)
            if 'layoutparser' in methods:
                results['layoutparser'] = process_image_with_layoutparser(preprocessed_image)
            if 'paddleocr' in methods:
                results['paddleocr'] = self.ocr_paddleocr.ocr(preprocessed_image)
            return results
        except Exception as e:
            logger.error(f'OCR processing failed: {e}')
            raise HTTPException(status_code=500, detail='Failed to process OCR due to server error')

    def preprocess(self, file):
        """Add preprocessing steps here."""
        # Add your preprocessing steps here
        return file

    except Exception as e:
        logger.error(f'OCR processing failed: {e}')
        raise HTTPException(status_code=500, detail='Failed to process OCR due to server error')

