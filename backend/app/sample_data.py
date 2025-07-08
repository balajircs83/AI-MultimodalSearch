import asyncio
from PIL import Image, ImageDraw
from search_engine import SearchEngine

# Sample text data
SAMPLE_TEXTS = [
    {
        "text": "A beautiful red sunset over the ocean with golden reflections on the water",
        "metadata": {"category": "nature", "tags": ["sunset", "ocean", "red"]}
    },
    {
        "text": "A red sports car speeding down a highway at sunset",
        "metadata": {"category": "vehicles", "tags": ["car", "red", "sunset"]}
    },
    {
        "text": "A red rose blooming in a garden with morning dew",
        "metadata": {"category": "nature", "tags": ["flower", "red", "garden"]}
    },
    {
        "text": "A red apple on a wooden table with natural lighting",
        "metadata": {"category": "food", "tags": ["fruit", "red", "still life"]}
    },
    {
        "text": "A red balloon floating in a clear blue sky",
        "metadata": {"category": "objects", "tags": ["balloon", "red", "sky"]}
    },
    {
        "text": "A red brick building with modern architecture",
        "metadata": {"category": "architecture", "tags": ["building", "red", "modern"]}
    },
    {
        "text": "A red dress hanging in a boutique window",
        "metadata": {"category": "fashion", "tags": ["clothing", "red", "retail"]}
    },
    {
        "text": "A red fire truck responding to an emergency",
        "metadata": {"category": "vehicles", "tags": ["truck", "red", "emergency"]}
    },
    {
        "text": "A red stop sign at a busy intersection",
        "metadata": {"category": "street", "tags": ["sign", "red", "traffic"]}
    },
    {
        "text": "A red umbrella in the rain on a city street",
        "metadata": {"category": "street", "tags": ["umbrella", "red", "rain"]}
    }
]

async def create_sample_image(color, size=(224, 224)):
    """Create a simple colored image with some pattern"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Add some simple patterns to make the images more interesting
    if color == "red":
        draw.rectangle([50, 50, 174, 174], fill="white")
    elif color == "blue":
        draw.ellipse([50, 50, 174, 174], fill="white")
    elif color == "green":
        draw.polygon([(112, 50), (174, 174), (50, 174)], fill="white")
    
    return img

# Sample image data
SAMPLE_IMAGES = [
    {
        "color": "red",
        "description": "A red image with white square",
        "metadata": {"category": "color", "tags": ["red", "square", "pattern"]}
    },
    {
        "color": "blue",
        "description": "A blue image with white circle",
        "metadata": {"category": "color", "tags": ["blue", "circle", "pattern"]}
    },
    {
        "color": "green",
        "description": "A green image with white triangle",
        "metadata": {"category": "color", "tags": ["green", "triangle", "pattern"]}
    }
]

async def index_sample_data():
    """Index all sample data (both text and images)"""
    search_engine = SearchEngine()
    
    print("Indexing sample text data...")
    for item in SAMPLE_TEXTS:
        result = await search_engine.index_text(item["text"], item["metadata"])
        print(f"Indexed text: {item['text'][:50]}... (ID: {result['id']})")
    
    print("\nIndexing sample images...")
    for item in SAMPLE_IMAGES:
        image = await create_sample_image(item["color"])
        result = await search_engine.index_image(image, item["metadata"])
        print(f"Indexed image: {item['description']} (ID: {result['id']})")
    
    print("\nSample data indexing complete!")
    print("You can now search for both text and images.")

if __name__ == "__main__":
    asyncio.run(index_sample_data()) 