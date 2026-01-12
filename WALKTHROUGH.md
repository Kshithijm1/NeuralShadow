# Section 3: The Semantic Gateway - Walkthrough

## Overview
The "Brain" of Neural Shadow is now online. We have built a FastAPI service that exposes the system's memory and uses RAG (Retrieval Augmented Generation) to answer user queries via a local LLM (Ollama).

## Components Built
1.  **FastAPI Server**: Running on `http://localhost:8000`.
2.  **Search Logic** (`core/brain`):
    - `LLMClient`: Connects to `ollama` (default: `mistral` model). Handles connection errors gracefully.
    - `SearchEngine`: Performs Vector Search (ChromaDB) to find top-k relevant context chunks, then constructs a prompt for the LLM.
3.  **API Endpoints** (`core/api`):
    - `GET /health`: Health check.
    - `POST /search`: Accepts `{query: str}` and returns `{answer: str, context: List[...]}`.
4.  **Integration**: Updated `main.py` to launch the API server alongside capture services.

## Verification Results
- **Automated Tests**: `tests/test_section3.py` passed.
    - **Health Check**: Endpoint returns 200 OK.
    - **RAG Flow**: Seeded the DB with "The secret code is 42", queried "What is the secret code?", and verified that the context contained the answer.

## Usage
- Start the app: `python main.py`.
- Query manually:
  ```bash
  curl -X POST "http://localhost:8000/search" \
       -H "Content-Type: application/json" \
       -d '{"query": "What was I working on yesterday?"}'
  ```

## Next Steps
- **Review**: Ensure `ollama` is running for full RAG experience.
- **Push**: Commit Section 3.
- **Proceed**: Section 4 (The Interface).
