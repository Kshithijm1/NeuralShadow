from fastapi import APIRouter, HTTPException
from .models import SearchRequest, SearchResponse
from ..brain.search_engine import SearchEngine
from ..utils import log

router = APIRouter()
engine = SearchEngine()

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Neural Shadow API"}

@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    log.info(f"API Search Request: {request.query}")
    try:
        result = engine.search(request.query, request.limit)
        return result
    except Exception as e:
        log.error(f"Search API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
