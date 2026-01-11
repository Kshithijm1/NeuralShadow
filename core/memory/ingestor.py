import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ..config import DATA_DIR
from ..utils import log
from .db import VectorDB
from .embeddings import EmbeddingService

class IngestHandler(FileSystemEventHandler):
    def __init__(self, db, embedder):
        self.db = db
        self.embedder = embedder

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Process .txt files
        if event.src_path.endswith(".txt"):
            # Small delay to ensure write complete
            time.sleep(1) 
            self._process_file(Path(event.src_path))

    def _process_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                return

            log.info(f"Ingesting file: {file_path.name}")
            
            # Determine type from path
            doc_type = "unknown"
            if "screen" in str(file_path):
                doc_type = "screen"
            elif "audio" in str(file_path):
                doc_type = "audio"
            
            # 1. Chunking (Simple Sliding Window for now: treat whole file as chunk if small, otherwise need split)
            # For this MVP, we treat the captured OCR block (which is usually one screen) as one document.
            # TODO: robust sliding window for long audio transcripts.
            
            # 2. Embedding
            vec = self.embedder.get_embedding(content)
            
            if vec:
                # 3. Store
                meta = {
                    "source": str(file_path.name),
                    "type": doc_type,
                    "timestamp": int(time.time()) # approximate
                }
                self.db.add(content, vec, meta)
                
        except Exception as e:
            log.error(f"Error processing file {file_path}: {e}")

class IngestorService:
    def __init__(self):
        self.db = VectorDB()
        self.embedder = EmbeddingService()
        self.observer = Observer()
        self.handler = IngestHandler(self.db, self.embedder)
        
    def start(self):
        log.info("Starting Ingestor Service (Watchdog)...")
        # Watch screen and audio dirs
        screen_dir = DATA_DIR / "screen"
        audio_dir = DATA_DIR / "audio"
        
        screen_dir.mkdir(parents=True, exist_ok=True)
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        self.observer.schedule(self.handler, str(screen_dir), recursive=False)
        self.observer.schedule(self.handler, str(audio_dir), recursive=False)
        
        self.observer.start()
        
    def stop(self):
        log.info("Stopping Ingestor Service...")
        self.observer.stop()
        self.observer.join()
