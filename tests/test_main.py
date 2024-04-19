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
    response = client.get("/get-template/", params={"template_name": "new_template"})
    expected_response = {"template_name": "new_template", "x": 1, "y": 2, "z": 3}
    assert response.status_code == 200
    assert response.json() == expected_response


def test_process_ocr():
    # Test OCR processing on a dummy image with more parameters
    response = client.post("/process_ocr/", json={
        "template_name": "new_template",
        "rectangles": [
            {"x": 10, "y": 10, "width": 50, "height": 50},
            {"x": 20, "y": 20, "width": 30, "height": 30}
        ]
    })
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.json())
    assert response.status_code == 200

def test_authentication():
    # Test the API authentication with more rigorous checks
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json() and "token_type" in response.json()

def test_secure_endpoint_access():
    response = client.get("/secure-endpoint")
    assert response.status_code == 401  # Make sure this checks for proper token absence

    # Now test with valid token
    token_response = client.post("/token", data={"username": "admin", "password": "secret"})
    token = token_response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get("/secure-endpoint", headers=headers)
    assert response.status_code == 200

