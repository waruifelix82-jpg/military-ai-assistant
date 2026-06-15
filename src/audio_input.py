import os
import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class AudioInput:
    def __init__(self, model_path="models/vosk-model"):
        """Initializes the offline microphone listener."""
        self.audio_queue = queue.Queue()
        
        if not os.path.exists(model_path):
            print(f"Error: Voice model folder not found at '{model_path}'")
            print("Please make sure you downloaded and extracted the Vosk model there.")
            sys.exit(1)
            
        # Load the model and initialize the recognizer at standard 16000Hz
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def _callback(self, indata, frames, time, status):
        """Internal callback to push microphone audio blocks into our queue."""
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(bytes(indata))

    def listen(self):
        """Opens the mic, listens until a complete phrase is captured, and returns text."""
        print("\nListening for voice command...")
        
        # Open raw audio input stream from default microphone
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self._callback):
            
            while True:
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    if text.strip():
                        print(f"You said: {text}")
                        return text