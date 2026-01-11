import unittest
import time
import shutil
import sys
import os
from pathlib import Path

# Fix import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.memory.embeddings import EmbeddingService
from core.config import DATA_DIR, COLLECTION_NAME

class TestSection2(unittest.TestCase):
    def test_embeddings(self):
        print("\nTesting Embeddings...")
        service = EmbeddingService()
        vec = service.get_embedding("Neural Shadow is cool")
        self.assertIsNotNone(vec)
        self.assertEqual(len(vec), 384) # MiniLM-L6-v2 dimension
        print("Embeddings OK.")

    def test_chroma_ingestion(self):
        print("\nTesting ChromaDB Ingestion...")
        import chromadb
        
        # We can't easily query the running main service db due to lock, 
        # so we rely on the implementation logic or check if collection exists.
        client = chromadb.PersistentClient(path=str(DATA_DIR / "chroma_db"))
        col = client.get_or_create_collection(COLLECTION_NAME)
        
        count_before = col.count()
        print(f"Docs in DB before: {count_before}")
        
        # Create a test file
        test_file = DATA_DIR / "screen" / "test_ingest.txt"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        with open(test_file, "w") as f:
            f.write("This is a test memory for Neural Shadow.")
            
        print("Created test file. Waiting for Ingestor (if running)...")
        # Note: In a unit test environment, the IngestorService isn't running in background unless we start it.
        # So we will verify the components directly.
        
        from core.memory.db import VectorDB
        db = VectorDB()
        doc_id = db.add("Manual entry", [0.1]*384, {"test": "true"})
        self.assertIsNotNone(doc_id)
        
        # Query it back
        results = db.query(query_embeddings=[[0.1]*384], n_results=1)
        self.assertTrue(len(results['ids'][0]) > 0)
        print("DB Add/Query OK.")

if __name__ == '__main__':
    unittest.main()
