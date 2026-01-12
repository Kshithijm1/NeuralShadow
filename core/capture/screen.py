import time
import mss
import mss.tools
import pytesseract
import numpy as np
from PIL import Image
from threading import Thread, Event
from ..config import SCREEN_CAPTURE_INTERVAL, SCREEN_DIFF_THRESHOLD, TESSERACT_CMD, DATA_DIR, ENABLE_ENCRYPTION
from ..utils import log
from ..processing.text_cleaner import TextCleaner
from ..security.encryption import SecurityManager

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class ScreenCapturer:
    def __init__(self):
        self._stop_event = Event()
        self.last_image = None
        self.output_dir = DATA_DIR / "screen"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def start(self):
        """Starts the screen capture thread."""
        self.thread = Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        log.info("Screen Capture Service Started")

    def stop(self):
        """Stops the capture thread."""
        self._stop_event.set()
        self.thread.join()
        log.info("Screen Capture Service Stopped")

    def _run_loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Capture primary monitor
            
            while not self._stop_event.is_set():
                try:
                    # Capture
                    sct_img = sct.grab(monitor)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    
                    # Diff Check
                    if self._should_process(img):
                        self._process_frame(img)
                        self.last_image = img
                    
                    time.sleep(SCREEN_CAPTURE_INTERVAL)
                    
                except Exception as e:
                    log.error(f"Error in screen capture loop: {e}")
                    time.sleep(5)

    def _should_process(self, current_img):
        if self.last_image is None:
            return True
            
        # Resize for faster comparison
        curr_small = current_img.resize((100, 100))
        last_small = self.last_image.resize((100, 100))
        
        # Calculate diff
        diff = np.mean(np.abs(np.array(curr_small) - np.array(last_small)))
        
        # Normalize diff to percentage (approx) 
        # A drastic change max pixel diff is 255. 
        diff_percent = (diff / 255.0) * 100
        
        return diff_percent > SCREEN_DIFF_THRESHOLD

    def _process_frame(self, img):
        timestamp = int(time.time())
        filename = self.output_dir / f"{timestamp}.png"
        
        # Save minimal reference
        img.save(filename)
        
        if ENABLE_ENCRYPTION:
            SecurityManager().encrypt_file(filename)
        
        # OCR
        text = pytesseract.image_to_string(img)
        cleaned_text = TextCleaner.clean_text(text)
        cleaned_text = TextCleaner.redact_pii(cleaned_text)
        
        if cleaned_text:
            log.debug(f"Captured Text ({len(cleaned_text)} chars): {cleaned_text[:50]}...")
            # TODO: Send to Vector DB Queue
            # For now, save to text file
            with open(self.output_dir / f"{timestamp}.txt", "w", encoding="utf-8") as f:
                f.write(cleaned_text)
