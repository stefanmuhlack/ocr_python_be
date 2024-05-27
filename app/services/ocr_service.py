from .ocr_processing import preprocess_for_ocr, process_image_with_tesseract, process_image_with_layoutparser, process_image_with_paddleocr

class OCRService:
    def __init__(self):
        self.ocr_tesseract = True
        self.ocr_layoutparser = True
        self.ocr_paddleocr = PaddleOCR()

    def process_image(self, image_data, methods=['tesseract', 'layoutparser', 'paddleocr']):
        preprocessed_image = preprocess_for_ocr(image_data)
        results = {}
        if 'tesseract' in methods:
            results['tesseract'] = process_image_with_tesseract(preprocessed_image)
        if 'layoutparser' in methods:
            results['layoutparser'] = process_image_with_layoutparser(preprocessed_image)
        if 'paddleocr' in methods:
            results['paddleocr'] = self.ocr_paddleocr.ocr(preprocessed_image)
        return results

    def preprocess(self, file):
        # Add preprocessing steps here
        return file
        paddle_results = paddle_ocr.ocr(preprocessed_image, cls=True)
        return {'layout': layout, 'tesseract_text': tesseract_text, 'paddle_results': paddle_results}
    except Exception as e:
        logger.error(f'OCR processing failed: {e}')
        raise HTTPException(status_code=500, detail='Failed to process OCR due to server error')

