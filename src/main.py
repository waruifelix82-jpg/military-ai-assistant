import sys
from audio_input import AudioInput
from nlp_engine import NLPEngine
from audio_output import AudioOutput

def run_voice_assistant():
    print("Loading Natalia's tactical systems...")
    
    # Initialize all three modules
    listener = AudioInput()
    nlp = NLPEngine()
    natalia = AudioOutput()
    
    # Startup greeting
    natalia.speak("Systems fully operational. I am Natalia. Awaiting your voice command.")
    
    while True:
        try:
            # 1. Capture audio from microphone and convert to text
            voice_text = listener.listen()
            
            # Check for shutdown commands in user speech
            if "exit system" in voice_text or "shutdown" in voice_text or "quit" in voice_text:
                natalia.speak("Shutting down tactical assistant. Stay safe out there.")
                break
                
            # 2. Match the spoken text against our military database
            response = nlp.process_query(voice_text)
            
            # 3. Natalia speaks the procedure back to you
            natalia.speak(response)
            
        except Exception as e:
            print(f"System Error encountered: {e}")
            natalia.speak("System error. Re-initializing voice parameters.")

if __name__ == "__main__":
    try:
        run_voice_assistant()
    except KeyboardInterrupt:
        print("\nSystem closed by user interface.")
        sys.exit(0)