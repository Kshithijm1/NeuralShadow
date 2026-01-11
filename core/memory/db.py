import chromadb
import uuid
import time
from chromadb.config import Settings
from ..config import DB_PATH, COLLECTION_NAME
from ..utils import log

class VectorDB:
    def __init__(self):
        log.info(f"Initializing VectorDB at {DB_PATH}")
        # Initialize Client
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        log.info(f"Connected to collection: {COLLECTION_NAME}")

    def add(self, text: str, embedding: list, metadata: dict = None):
        if not text or not embedding:
            return
            
        try:
            doc_id = str(uuid.uuid4())
            if metadata is None:
                metadata = {}
            
            # Ensure timestamp in metadata
            if "timestamp" not in metadata:
                metadata["timestamp"] = int(time.time())
                
            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            log.debug(f"Indexed document: {doc_id} ({len(text)} chars)")
            return doc_id
        except Exception as e:
            log.error(f"Failed to add document to DB: {e}")

    def query(self, query_embeddings: list, n_results: int = 5):
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
            return results
        except Exception as e:
            log.error(f"Query error: {e}")
            return None
