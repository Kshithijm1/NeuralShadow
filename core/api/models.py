from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class ContextItem(BaseModel):
    id: str
    text: str
    source: str
    type: str
    timestamp: float
    score: float

class SearchResponse(BaseModel):
    query: str
    answer: str
    context: List[ContextItem]
