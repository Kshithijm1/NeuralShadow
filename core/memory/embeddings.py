from sentence_transformers import SentenceTransformer
from ..config import EMBEDDING_MODEL
from ..utils import log

class EmbeddingService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance.model = None
        return cls._instance

    def load_model(self):
        if self.model is None:
            log.info(f"Loading Embedding Model: {EMBEDDING_MODEL}...")
            try:
                self.model = SentenceTransformer(EMBEDDING_MODEL)
                log.info("Embedding Model Loaded.")
            except Exception as e:
                log.error(f"Failed to load embedding model: {e}")
                
    def get_embedding(self, text: str):
        if not text:
            return None
        if self.model is None:
            self.load_model()
        
        try:
            # Return list of floats
            return self.model.encode(text).tolist()
        except Exception as e:
            log.error(f"Embedding error: {e}")
            return None
