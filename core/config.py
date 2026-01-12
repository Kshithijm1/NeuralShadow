import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# Ensure directories exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Capture Settings
SCREEN_CAPTURE_INTERVAL = 2.0  # Seconds between checks
SCREEN_DIFF_THRESHOLD = 0.5    # Percentage (0-100) difference to trigger save. 0.5% is sensitive.

# Audio Settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_BLOCK_SIZE = 2048
VAD_THRESHOLD = 0.5

# OCR Settings
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Memory Settings
DB_PATH = DATA_DIR / "chroma_db"
COLLECTION_NAME = "neural_shadow_memories"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM Settings
OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "mistral" # Ensure you have pulled this model: `ollama pull mistral`
