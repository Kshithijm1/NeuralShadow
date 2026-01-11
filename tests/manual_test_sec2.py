import sys
import os
import time

# Fix import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("Imports starting...")
from core.config import DATA_DIR, COLLECTION_NAME
try:
    from core.memory.embeddings import EmbeddingService
    from core.memory.db import VectorDB
    print("Imports done.")
except Exception as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test():
    print("Initializing EmbeddingService (this may download model)...")
    service = EmbeddingService()
    service.load_model()
    print("Model loaded.")
    
    print("Getting Embedding...")
    vec = service.get_embedding("Neural Shadow Test")
    print(f"Vector generated. Dim: {len(vec)}")
    
    print("Initializing VectorDB...")
    db = VectorDB()
    
    print("Adding Doc...")
    db.add("Neural Shadow Test", vec, {"test": "true"})
    
    print("Querying Doc...")
    results = db.query([vec], n_results=1)
    
    print("Results:", results)
    
    if results and len(results['ids'][0]) > 0:
        print("SUCCESS: Section 2 Verified.")
    else:
        print("FAILURE: No results found.")

if __name__ == "__main__":
    test()
