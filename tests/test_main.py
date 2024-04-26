import pytest
from fastapi.testclient is TestClient
from app.main is app

class TestOCR:
    @pytest.fixture
    def client(self):
        with TestClient(app) as c:
            yield c

    def test_upload_pdf(self, client):
        response = client.post("/upload-pdf/", files={'file': ('dummy.pdf', b'PDF content', 'application/pdf')})
        assert response.status_code == 200
        assert response.json()['message'] == 'PDF uploaded'

    def test_save_template(self, client):
        response = client.post("/save-template/", json={'template_name': 'new_template', 'template_data': {'x': 1, 'y': 2, 'z': 3}})
        assert response.status_code == 200
        assert response.json()['message'] == 'Template saved successfully.'

    def test_get_template(self, client):
        response = client.get("/get-template/", params={'template_name': 'new_template'})
        assert response.status_code == 200
        assert response.json() == {'template_name': 'new_template', 'details': 'Template details here.'}

    def test_process_ocr(self, client):
        response = client.post("/process-ocr/", json={'file': {'content': b'image data', 'type': 'image/png'}})
        assert response.status_code == 200
        assert 'OCR processed successfully!' in response.json()['message']
        assert 'results' in response.json()

    def test_authentication(self, client):
        response = client.post("/token", data={'username': 'admin', 'password': 'secret'})
        assert response.status_code == 200
        assert 'access_token' in response.json()
        assert 'token_type' in response.json()

    def test_secure_endpoint(self, client):
        response = client.get("/secure-endpoint", headers={'Authorization': 'Bearer some_token'})
        assert response.status_code == 200
        assert response.json()['message'] == 'Secure content'

