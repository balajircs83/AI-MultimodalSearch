import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
import torch
from typing import List, Dict, Any
import uuid
from PIL import Image
import io
from scipy.spatial.distance import cdist
from .models import SearchResult
import pickle
import os

class SearchEngine:
    def __init__(self):
        # Initialize text model
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize CLIP model for image-text multimodal search
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Initialize storage for embeddings and metadata
        self.text_embeddings = []
        self.image_embeddings = []
        self.text_metadata = {}
        self.image_metadata = {}
        self.text_content = {}
        self.image_content = {}

        # Load existing data if available
        self.load_data()

    def save_data(self):
        """Save the current state of the search engine"""
        data = {
            'text_embeddings': self.text_embeddings,
            'image_embeddings': self.image_embeddings,
            'text_metadata': self.text_metadata,
            'image_metadata': self.image_metadata,
            'text_content': self.text_content,
            'image_content': self.image_content
        }
        with open('search_data.pkl', 'wb') as f:
            pickle.dump(data, f)

    def load_data(self):
        """Load saved data if it exists"""
        if os.path.exists('search_data.pkl'):
            with open('search_data.pkl', 'rb') as f:
                data = pickle.load(f)
                self.text_embeddings = data['text_embeddings']
                self.image_embeddings = data['image_embeddings']
                self.text_metadata = data['text_metadata']
                self.image_metadata = data['image_metadata']
                self.text_content = data['text_content']
                self.image_content = data['image_content']

    async def _get_text_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text"""
        return self.text_model.encode(text)

    async def _get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """Get embedding for image"""
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
        return image_features.numpy()

    async def index_text(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, str]:
        """Index a text document"""
        doc_id = str(uuid.uuid4())
        embedding = await self._get_text_embedding(text)
        
        # Add to embeddings list
        self.text_embeddings.append(embedding)
        
        # Store metadata and content
        self.text_metadata[doc_id] = metadata or {}
        self.text_content[doc_id] = text
        
        # Save the updated data
        self.save_data()
        
        return {"id": doc_id, "status": "success", "message": "Text indexed successfully"}

    async def index_image(self, image: Image.Image, metadata: Dict[str, Any] = None) -> Dict[str, str]:
        """Index an image"""
        doc_id = str(uuid.uuid4())
        embedding = await self._get_image_embedding(image)
        
        # Ensure embedding is 1D array
        embedding = np.array(embedding).flatten()
        print(f"Indexing image with embedding shape: {embedding.shape}")
        
        # Add to embeddings list
        self.image_embeddings.append(embedding)
        
        # Store metadata and content
        self.image_metadata[doc_id] = metadata or {}
        self.image_content[doc_id] = image
        
        # Save the updated data
        self.save_data()
        
        return {"id": doc_id, "status": "success", "message": "Image indexed successfully"}

    async def search_text(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search using text query"""
        if not self.text_embeddings:
            return []
            
        query_embedding = await self._get_text_embedding(query)
        
        # Calculate distances using scipy
        distances = cdist([query_embedding], np.array(self.text_embeddings), 'cosine')[0]
        
        # Get top k results
        top_k_indices = np.argsort(distances)[:k]
        
        results = []
        for idx in top_k_indices:
            doc_id = list(self.text_content.keys())[idx]
            results.append(SearchResult(
                id=doc_id,
                content=self.text_content[doc_id],
                score=float(1 - distances[idx]),  # Convert cosine distance to similarity
                metadata=self.text_metadata[doc_id],
                type="text"
            ))
        
        return results

    async def search_image(self, image: Image.Image, k: int = 5) -> List[SearchResult]:
        """Search using image query"""
        if not self.image_embeddings:
            print("No images indexed yet")
            return []
            
        query_embedding = await self._get_image_embedding(image)
        print(f"Query embedding shape: {query_embedding.shape}")
        
        # Ensure embeddings are 2D arrays
        query_embedding = np.array(query_embedding).reshape(1, -1)
        image_embeddings = np.array(self.image_embeddings)
        print(f"Image embeddings shape: {image_embeddings.shape}")
        
        # Ensure image_embeddings is 2D
        if len(image_embeddings.shape) == 1:
            image_embeddings = image_embeddings.reshape(1, -1)
        elif len(image_embeddings.shape) > 2:
            image_embeddings = image_embeddings.reshape(len(self.image_embeddings), -1)
        
        print(f"Reshaped image embeddings shape: {image_embeddings.shape}")
        
        # Calculate distances using scipy
        distances = cdist(query_embedding, image_embeddings, 'cosine')[0]
        
        # Get top k results
        top_k_indices = np.argsort(distances)[:k]
        
        results = []
        for idx in top_k_indices:
            doc_id = list(self.image_content.keys())[idx]
            results.append(SearchResult(
                id=doc_id,
                content="[Image content]",
                score=float(1 - distances[idx]),  # Convert cosine distance to similarity
                metadata=self.image_metadata[doc_id],
                type="image"
            ))
        
        return results 