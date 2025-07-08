from pydantic import BaseModel
from typing import Optional, Dict, Any

class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    metadata: Optional[Dict[str, Any]] = None
    type: str  # "text" or "image"

class IndexResponse(BaseModel):
    id: str
    status: str
    message: str 