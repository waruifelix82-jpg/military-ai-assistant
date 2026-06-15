import pyttsx3

class AudioOutput:
    def __init__(self, rate=175, volume=1.0):
        """Initializes the offline text-to-speech engine with a female voice."""
        self.engine = pyttsx3.init()
        
        # Configure speaking speed and volume
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Set to a female voice
        self.set_female_voice()

    def set_female_voice(self):
        """Loops through installed system voices and selects a female option."""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                return
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)

    def speak(self, text):
        """Converts text into spoken audio."""
        if not text:
            return
            
        # Updated to display her name in the console output
        print(f"Natalia: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# Quick local test
if __name__ == "__main__":
    print("Testing Natalia's Audio Output...")
    speaker = AudioOutput()
    speaker.speak("Systems operational. Hello, I am Natalia, your tactical data assistant. How can I help you today?")