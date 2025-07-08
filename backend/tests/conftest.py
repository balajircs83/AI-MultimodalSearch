import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.search_engine import SearchEngine
import numpy as np
from PIL import Image
import io

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def search_engine():
    return SearchEngine()

@pytest.fixture
def sample_text():
    return "This is a sample text for testing"

@pytest.fixture
def sample_image():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr 