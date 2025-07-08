import pytest
from app.search_engine import SearchEngine
from PIL import Image
import numpy as np

@pytest.mark.asyncio
async def test_text_indexing(search_engine, sample_text):
    result = await search_engine.index_text(sample_text)
    assert result["status"] == "success"
    assert "id" in result

@pytest.mark.asyncio
async def test_image_indexing(search_engine, sample_image):
    image = Image.open(sample_image)
    result = await search_engine.index_image(image)
    assert result["status"] == "success"
    assert "id" in result

@pytest.mark.asyncio
async def test_text_search(search_engine, sample_text):
    # First index the text
    await search_engine.index_text(sample_text)
    
    # Then search for it
    results = await search_engine.search_text(sample_text)
    assert len(results) > 0
    assert results[0].type == "text"
    assert results[0].score < 1.0  # Should be a reasonable similarity score

@pytest.mark.asyncio
async def test_image_search(search_engine, sample_image):
    # First index the image
    image = Image.open(sample_image)
    await search_engine.index_image(image)
    
    # Then search for it
    results = await search_engine.search_image(image)
    assert len(results) > 0
    assert results[0].type == "image"
    assert results[0].score < 1.0  # Should be a reasonable similarity score

@pytest.mark.asyncio
async def test_metadata_storage(search_engine, sample_text):
    metadata = {"source": "test", "category": "example"}
    result = await search_engine.index_text(sample_text, metadata)
    
    # Search and verify metadata
    results = await search_engine.search_text(sample_text)
    assert results[0].metadata == metadata 