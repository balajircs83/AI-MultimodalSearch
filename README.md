# Multimodal Search Engine

A search engine that understands both text and images, providing relevant results by analyzing both modalities simultaneously.

## Features

- Text and image search capabilities
- Vector-based similarity search using CLIP and Sentence Transformers
- FastAPI backend with persistent storage
- React frontend with Material-UI
- Comprehensive test suite

## Project Structure

```
MultimodalSearch/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application code
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic models
│   │   ├── sample_data.py    # Sample data and indexing
│   │   └── search_engine.py  # Core search functionality
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── venv/                 # Virtual environment
├── frontend/                  # React frontend
│   ├── public/               # Static files
│   ├── src/                  # React source code
│   ├── package.json          # Node.js dependencies
│   └── package-lock.json     # Node.js lock file
└── README.md                 # Project documentation
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd MultimodalSearch
```

2. Set up the backend:
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash
# or
.\venv\Scripts\activate      # On Windows CMD

# Install dependencies
pip install -r requirements.txt

# Index sample data
python -m app.sample_data

# Run the backend server
uvicorn app.main:app --reload
```

3. Set up the frontend:
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## Usage

1. Text Search:
   - Enter your search query in the text box
   - Click "Search" or press Enter
   - View results with similarity scores and metadata

2. Image Search:
   - Switch to the "Image Search" tab
   - Drag and drop an image or click to select
   - View similar images with similarity scores

## API Endpoints

- `POST /search/text` - Search using text query
- `POST /search/image` - Search using image query
- `POST /index/text` - Index a text document
- `POST /index/image` - Index an image

## Testing

Run the test suite:
```bash
cd backend
pytest
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Technologies Used

- Backend:
  - FastAPI
  - CLIP (Contrastive Language-Image Pre-training)
  - Sentence Transformers
  - NumPy and SciPy for vector operations
  - Pickle for data persistence

- Frontend:
  - React
  - Material-UI
  - Axios for API calls
  - React Dropzone for file uploads 