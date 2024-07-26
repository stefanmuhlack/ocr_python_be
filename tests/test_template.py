import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.template import Template, TemplateField
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    Base.metadata.drop_all(bind=engine)
    db.close()

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

def test_create_template(client):
    response = client.post("/templates/", json={
        "name": "Test Template",
        "fields": [
            {"name": "Field1", "type": "text"},
            {"name": "Field2", "type": "boolean"}
        ]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Template created successfully"

def test_update_template(client):
    response = client.put("/templates/1", json={
        "name": "Updated Template",
        "fields": [
            {"name": "UpdatedField1", "type": "text"}
        ]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Template updated successfully"

def test_delete_template(client):
    response = client.delete("/templates/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Template deleted successfully"