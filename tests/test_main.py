from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    # Simulate file upload with a dummy PDF file
    response = client.post("/upload-pdf/", files={"file": ("dummy.pdf", b"PDF content", "application/pdf")})
    assert response.status_code == 200
    assert "Processed" in response.json()["message"]

def test_save_template():
    # Test saving a new template with more detailed data
    response = client.post("/save-template/", json={"template_name": "new_template", "template_data": {"x": 1, "y": 2, "z": 3}})
    assert response.status_code == 200
    assert "Template saved successfully." in response.json()["message"]

def test_get_template():
    # Test retrieving the previously saved template with additional checks
    response = client.get("/get-template/", params={"template_name": "new_template"})
    assert response.status_code == 200
    assert response.json() == {"x": 1, "y": 2, "z": 3}

def test_process_ocr():
    # Test OCR processing on a dummy image with more parameters
    response = client.post("/process_ocr/", json={"template_name": "new_template", "rectangles": [{"x": 10, "y": 10, "width": 50, "height": 50}, {"x": 20, "y": 20, "width": 30, "height": 30}]})
    assert response.status_code == 200
    assert "Data processed successfully!" in response.json()["message"]

def test_authentication():
    # Test the API authentication with more rigorous checks
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json() and "token_type" in response.json()

def test_secure_endpoint_access():
    # Test accessing a secure endpoint with and without authentication
    response = client.get("/secure-endpoint")
    assert response.status_code == 401
    # Test with token
    token_response = client.post("/token", data={"username": "admin", "password": "secret"})
    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get("/secure-endpoint", headers=headers)
    assert response.status_code == 200

