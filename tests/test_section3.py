import unittest
import time
import requests
import threading
import sys
import os
import uvicorn
from fastapi.testclient import TestClient

# Fix path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.api.app import app
from core.memory.db import VectorDB
from core.memory.embeddings import EmbeddingService

client = TestClient(app)

class TestSection3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Pre-seed DB with known data
        print("Seeding DB for API Test...")
        db = VectorDB()
        embedder = EmbeddingService()
        vec = embedder.get_embedding("The secret code is 42.")
        db.add("The secret code is 42.", vec, {"source": "test_seed", "timestamp": 12345})

    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        print("Health Check Passed.")

    def test_search_endpoint(self):
        print("Testing /search endpoint...")
        # Note: This will try to hit Ollama. If Ollama is down, it should still return context but generic error answer.
        response = client.post("/search", json={"query": "What is the secret code?", "limit": 1})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("query", data)
        self.assertIn("answer", data)
        self.assertIn("context", data)
        
        # Check context retrieval
        has_secret = any("42" in item["text"] for item in data["context"])
        self.assertTrue(has_secret, "Context retrieval failed to find seed data.")
        
        print("\n=== RAG Result ===")
        print(f"Q: {data['query']}")
        print(f"A: {data['answer']}")
        print(f"Context Found: {len(data['context'])} items")
        print("==================\n")

if __name__ == '__main__':
    unittest.main()
