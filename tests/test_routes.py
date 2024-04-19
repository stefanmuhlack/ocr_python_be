from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    response = client.post("/upload-pdf/", files={"file": ("dummy.pdf", b"PDF content", "application/pdf")})
    assert response.status_code == 200, response.text

def test_save_template():
    response = client.post("/save-template/", json={"template_name": "example_template", "template_data": {"key": "value"}})
    assert response.status_code == 200, response.text

def test_get_template():
    response = client.get("/get-template/", params={"template_name": "example_template"})
    assert response.status_code == 200, response.text

def test_process_ocr():
    response = client.post("/process-ocr/", json={"template_name": "example_template", "rectangles": []})
    assert response.status_code == 200, response.text
