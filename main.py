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
    
    try:
        # Start Memory Ingestion first
        ingest_service.start()
        
        # Start Senses
        screen_service.start()
        audio_service.start()
        
        while True:
            # Main thread keep-alive
            time.sleep(1)
            
    except KeyboardInterrupt:
        log.info("Stopping services...")
        screen_service.stop()
        audio_service.stop()
        ingest_service.stop()
        log.info("Services stopped. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
