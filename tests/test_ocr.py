import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.ocr_processing import process_image_with_tesseract, process_image_with_layoutparser

class TestOCRProcessing:
    @pytest.fixture
    def client(self):
        with TestClient(app) as c:
            yield c

    def test_process_image_with_tesseract(self, client):
        image_path = 'tests/fixtures/sample_image.png'
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        response = process_image_with_tesseract(image_data)
        assert response is not None
        assert 'Sample text extracted' in response

    def test_process_image_with_layoutparser(self, client):
        image_path = 'tests/fixtures/sample_image.png'
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        response = process_image_with_layoutparser(image_data)
        assert response is not None
        assert 'Complex layout analyzed' in response

