import unittest
import shutil
import time
import sys
import os
from pathlib import Path

# Fix import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.processing.text_cleaner import TextCleaner
from core.capture.screen import ScreenCapturer
from core.config import DATA_DIR

class TestSection1(unittest.TestCase):
    def setUp(self):
        # Clean up data dir before test
        if DATA_DIR.exists():
           # don't delete everything, just ensure it exists
           pass

    def test_text_cleaner(self):
        print("\nTesting Text Cleaner...")
        raw = "Hello   World\n\nThis is a    test."
        cleaned = TextCleaner.clean_text(raw)
        self.assertEqual(cleaned, "Hello World This is a test.")
        
        pii = "Contact me at bob@example.com or 555-123-4567."
        redacted = TextCleaner.redact_pii(pii)
        self.assertIn("[EMAIL_REDACTED]", redacted)
        self.assertIn("[PHONE_REDACTED]", redacted)
        print("Text Cleaner Passed.")

    def test_screen_capture_integration(self):
        print("\nTesting Screen Capture (Running for 4s)...")
        capturer = ScreenCapturer()
        capturer.start()
        
        # Simulate activity
        time.sleep(4)
        
        capturer.stop()
        
        # Check for files
        files = list((DATA_DIR / "screen").glob("*.png"))
        print(f"Captured {len(files)} frames.")
        
        self.assertTrue(len(files) > 0, "No screen frames captured! Ensure Tesseract is installed and screen is active.")

if __name__ == '__main__':
    unittest.main()
