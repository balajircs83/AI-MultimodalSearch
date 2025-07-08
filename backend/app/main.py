from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from .search_engine import SearchEngine
from .models import SearchResult
from pydantic import BaseModel
from PIL import Image
import io

app = FastAPI(title="Multimodal Search Engine")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine as a global variable
search_engine = SearchEngine()

class TextSearchQuery(BaseModel):
    query: str

@app.post("/search/text", response_model=List[SearchResult])
async def search_text(query: TextSearchQuery):
    """Search using text query"""
    return await search_engine.search_text(query.query)

@app.post("/search/image", response_model=List[SearchResult])
async def search_image(file: UploadFile = File(...)):
    """Search using image query"""
    # Read the uploaded file
    contents = await file.read()
    
    # Convert to PIL Image
    image = Image.open(io.BytesIO(contents))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    return await search_engine.search_image(image)

@app.post("/index/text")
async def index_text(text: str, metadata: dict = None):
    """Index a text document"""
    return await search_engine.index_text(text, metadata)

@app.post("/index/image")
async def index_image(file: UploadFile = File(...), metadata: dict = None):
    """Index an image"""
    # Read the uploaded file
    contents = await file.read()
    
    # Convert to PIL Image
    image = Image.open(io.BytesIO(contents))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    return await search_engine.index_image(image, metadata)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 