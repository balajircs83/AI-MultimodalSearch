import pytest
from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

def test_text_search_endpoint():
    response = client.post("/search/text", json={"query": "test query"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_image_search_endpoint(sample_image):
    files = {"file": ("test.png", sample_image, "image/png")}
    response = client.post("/search/image", files=files)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_text_index_endpoint():
    response = client.post("/index/text", json={
        "text": "test document",
        "metadata": {"source": "test"}
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_image_index_endpoint(sample_image):
    files = {"file": ("test.png", sample_image, "image/png")}
    response = client.post("/index/image", files=files)
    assert response.status_code == 200
    assert "id" in response.json() 