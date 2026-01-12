import time
import sys
import threading
from core.utils import log
from core.capture.screen import ScreenCapturer
from core.capture.audio import AudioCapturer
from core.memory.ingestor import IngestorService

def main():
    log.info("=== Neural Shadow v0.1 Starting ===")
    
    screen_service = ScreenCapturer()
    audio_service = AudioCapturer()
    ingest_service = IngestorService()
    
import uvicorn
from core.api.app import app

def main():
    log.info("=== Neural Shadow v0.1 Starting ===")
    
    screen_service = ScreenCapturer()
    audio_service = AudioCapturer()
    ingest_service = IngestorService()
    
    try:
        # Start Background Services
        ingest_service.start()
        screen_service.start()
        audio_service.start()
        
        # Start API Server (Blocking)
        log.info("Starting API Server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        log.info("Stopping services...")
    finally:
        screen_service.stop()
        audio_service.stop()
        ingest_service.stop()
        log.info("Services stopped. Exiting.")

if __name__ == "__main__":
    main()
