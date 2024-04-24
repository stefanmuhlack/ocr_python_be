import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    response = client.post("/upload-pdf/")
    assert response.status_code == 200
    assert response.json() == {"message": "PDF uploaded"}

def test_save_template():
    response = client.post("/save-template/")
    assert response.status_code == 200
    assert response.json() == {"message": "Template saved successfully."}

def test_get_template():
    response = client.get("/get-template/", params={"template_name": "new_template"})
    assert response.status_code == 200
    assert response.json() == {"template_name": "new_template", "details": "Template details here."}

def test_process_ocr():
    with open("path/to/test/image.jpg", "rb") as image_file:
        response = client.post("/process-ocr/", files={"file": ("image.jpg", image_file, "image/jpeg")})
        assert response.status_code == 200
        assert "OCR processed successfully!" in response.json()["message"]
        assert "results" in response.json()

def test_authentication():
    form_data = {'username': 'admin', 'password': 'secret'}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json() and "token_type" in response.json()

def test_secure_endpoint_access():
    token = "some_valid_token"
    headers = {'Authorization': 'Bearer ' + token}
    response = client.get("/secure-endpoint", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Secure content"}

    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get("/secure-endpoint", headers=headers)
    assert response.status_code == 200

