import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("Python executable:", sys.executable)
print("CWD:", os.getcwd())

try:
    print("Importing utils...")
    from core.utils import log
    print("Utils ok.")

    print("Importing TextCleaner...")
    from core.processing.text_cleaner import TextCleaner
    print("TextCleaner ok.")

    print("Importing ScreenCapturer...")
    from core.capture.screen import ScreenCapturer
    print("ScreenCapturer ok.")

except Exception as e:
    print("\nIMPORT ERROR:")
    print(e)
    import traceback
    traceback.print_exc()
