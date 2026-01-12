from ..memory.db import VectorDB
from ..memory.embeddings import EmbeddingService
from .llm_client import LLMClient
from ..utils import log

class SearchEngine:
    def __init__(self):
        self.db = VectorDB()
        self.embedder = EmbeddingService()
        self.llm = LLMClient()

    def search(self, query: str, limit: int = 5):
        """
        Performs semantic search + RAG generation.
        """
        # 1. Embed Query
        query_vec = self.embedder.get_embedding(query)
        if not query_vec:
            return {"answer": "Error generating embedding.", "context": []}

        # 2. Retrieve from DB
        results = self.db.query([query_vec], n_results=limit)
        
        # Parse Results
        context = []
        if results and results['ids']:
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                text = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                context.append({
                    "id": doc_id,
                    "text": text,
                    "source": metadata.get("source", "unknown"),
                    "type": metadata.get("type", "unknown"),
                    "timestamp": metadata.get("timestamp", 0),
                    "score": distance # Lower is better in Chroma (L2) usually, or similarity
                })

        # 3. Generate Answer (RAG)
        answer = self.llm.generate_answer(query, context)
        
        return {
            "query": query,
            "answer": answer,
            "context": context
        }
