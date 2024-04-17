from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    # Simulate file upload with a dummy PDF file
    response = client.post("/upload-pdf/", files={"file": ("dummy.pdf", b"PDF content", "application/pdf")})
    assert response.status_code == 200
    assert "Processed" in response.json()["message"]

def test_save_template():
    # Test saving a new template
    response = client.post("/save-template/", json={"template_name": "new_template", "template_data": {"x": 1, "y": 2}})
    assert response.status_code == 200
    assert "Template saved successfully." in response.json()["message"]

def test_get_template():
    # Test retrieving the previously saved template
    response = client.get("/get-template/", params={"template_name": "new_template"})
    assert response.status_code == 200
    assert response.json() == {"x": 1, "y": 2}

def test_process_ocr():
    # Test OCR processing on a dummy image
    response = client.post("/process_ocr/", json={"template_name": "new_template", "rectangles": [{"x": 10, "y": 10, "width": 50, "height": 50}]})
    assert response.status_code == 200
    assert "Data processed successfully!" in response.json()["message"]

def test_authentication():
    # Test the API authentication
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_secure_endpoint_access():
    # Test accessing a secure endpoint without authentication
    response = client.get("/secure-endpoint")
    assert response.status_code == 401
