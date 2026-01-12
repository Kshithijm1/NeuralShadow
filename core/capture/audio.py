import time
import threading
from threading import Thread, Event
from pathlib import Path
from ..config import AUDIO_SAMPLE_RATE, DATA_DIR, ENABLE_ENCRYPTION
from ..utils import log
from ..processing.text_cleaner import TextCleaner
from ..security.encryption import SecurityManager

try:
    import soundcard as sc
    import soundfile as sf
    import numpy as np
    from faster_whisper import WhisperModel
    AUDIO_AVAILABLE = True
except ImportError as e:
    log.warning(f"Audio dependencies missing: {e}. Audio capture disabled.")
    AUDIO_AVAILABLE = False

class AudioCapturer:
    def __init__(self):
        self._stop_event = Event()
        self.output_dir = DATA_DIR / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_duration = 30 # seconds
        self.model = None
        
        if not AUDIO_AVAILABLE:
            return

        # Initialize Whisper (Download small model by default)
        log.info("Loading Whisper Model...")
        try:
             # dynamic quantization for cpu
            self.model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
            log.info("Whisper Model Loaded.")
        except Exception as e:
             log.error(f"Failed to load Whisper: {e}")
             self.model = None

    def start(self):
        self.thread = Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        log.info("Audio Capture Service Started")

    def stop(self):
        self._stop_event.set()
        self.thread.join()
        log.info("Audio Capture Service Stopped")

    def _run_loop(self):
        # Get loopback microphone (system audio)
        # Note: This might require specific setup on Windows (Stereo Mix) or soundcard library support
        try:
            mics = sc.all_microphones(include_loopback=True)
            if not mics:
                log.warning("No microphones found. Audio capture disabled.")
                return
            
            # Prefer the default loopback if available, else standard mic
            mic = mics[0] 
            for m in mics:
                if m.isloopback:
                    mic = m
                    break
            
            log.info(f"Recording from: {mic.name}")

            with mic.recorder(samplerate=AUDIO_SAMPLE_RATE) as recorder:
                while not self._stop_event.is_set():
                    # Record a chunk
                    data = recorder.record(numframes=AUDIO_SAMPLE_RATE * self.chunk_duration)
                    
                    # Process in a separate thread/step to not block recording? 
                    # For simplicity, we process valid chunks after recording. 
                    # In production, use two threads (recorder -> buffer -> processor).
                    self._process_audio(data[:, 0]) # Mono
                    
        except Exception as e:
            log.error(f"Error in audio loop: {e}")

    def _process_audio(self, audio_data):
        # audio_data is float32 numpy array
        # Check energy level (simple VAD before Whisper to save compute)
        rmse = np.sqrt(np.mean(audio_data**2))
        if rmse < 0.01: # Silence threshold
            return

        timestamp = int(time.time())
        filename = self.output_dir / f"{timestamp}.wav"
        
        # Save WAV
        sf.write(filename, audio_data, AUDIO_SAMPLE_RATE)
        
        if ENABLE_ENCRYPTION:
            SecurityManager().encrypt_file(filename)
        
        try:
            # Transcribe
            segments, info = self.model.transcribe(str(filename), vad_filter=True)
            full_text = " ".join([segment.text for segment in segments])
            
            cleaned_text = TextCleaner.clean_text(full_text)
            cleaned_text = TextCleaner.redact_pii(cleaned_text)

            if cleaned_text:
                log.debug(f"Captured Audio: {cleaned_text[:50]}...")
                # Save Transcript
                with open(self.output_dir / f"{timestamp}.txt", "w", encoding="utf-8") as f:
                    f.write(cleaned_text)
            else:
                # If pure silence/noise was detected by VAD but no text, maybe delete wav?
                # Keeping it for now.
                pass
                
        except Exception as e:
            log.error(f"Whisper transcription error: {e}")
