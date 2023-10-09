from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    # Simulate uploading a PDF file
    response = client.post("/upload-pdf/", files={"file": ("example.pdf", open("./Templates/example.pdf", "rb"))})
    assert response.status_code == 200
    assert "Processed" in response.json()["message"]

def test_save_template():
    # Simulate saving a template
    response = client.post("/save-template/", json={"template_name": "example_template", "template_data": {"key": "value"}})
    assert response.status_code == 200
    assert "Template saved successfully." in response.json()["message"]

def test_get_template():
    # Simulate getting a template
    response = client.get("/get-template/?template_name=example_template")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_process_ocr():
    # Simulate processing OCR data
    response = client.post("/process_ocr/", json={"template_name": "example_template", "rectangles": []})
    assert response.status_code == 200
    assert "Data processed successfully!" in response.json()["message"]
