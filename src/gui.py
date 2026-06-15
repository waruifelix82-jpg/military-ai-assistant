import threading
import sys
import customtkinter as ctk

# Import your existing backend classes
from audio_input import AudioInput
from nlp_engine import NLPEngine
from audio_output import AudioOutput

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class NataliaGUI:
    def __init__(self):
        # 1. Initialize Backend Systems
        self.listener = AudioInput()
        self.nlp = NLPEngine()
        self.natalia = AudioOutput()

        # 2. Main Window Configuration
        self.root = ctk.CTk()
        self.root.title("NATALIA - Tactical Data Assistant")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Handle window closure cleanly
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 3. Header Status Frame
        self.header_frame = ctk.CTkFrame(self.root, height=70, corner_radius=8)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.header_frame.pack_propagate(False)

        self.status_indicator = ctk.CTkLabel(
            self.header_frame, 
            text="• NATALIA SYSTEM ONLINE", 
            font=("Courier New", 20, "bold"),
            text_color="#deff9a"
        )
        self.status_indicator.pack(side="left", padx=20, pady=20)

        self.mode_label = ctk.CTkLabel(
            self.header_frame, 
            text="STANDBY", 
            font=("Courier New", 14, "bold"),
            text_color="#666666"
        )
        self.mode_label.pack(side="right", padx=20, pady=20)

        # 4. Dialogue Box
        self.display_box = ctk.CTkTextbox(
            self.root, 
            font=("Courier New", 15), 
            text_color="#f5f5f5",
            border_width=1,
            border_color="#333333"
        )
        self.display_box.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.insert_log("Initializing system arrays...\n")
        self.insert_log("All local modules integrated successfully.\n")

        # 5. Interactive Control Panel
        self.control_frame = ctk.CTkFrame(self.root, height=80, corner_radius=8)
        self.control_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.control_frame.pack_propagate(False)

        self.action_btn = ctk.CTkButton(
            self.control_frame, 
            text="ENGAGE VOICE ASSISTANT", 
            font=("Courier New", 14, "bold"),
            command=self.start_voice_thread
        )
        self.action_btn.pack(fill="both", expand=True, padx=15, pady=15)

    def insert_log(self, text):
        """Appends logs safely to the screen monitor."""
        self.display_box.insert("end", text)
        self.display_box.see("end")

    def start_voice_thread(self):
        """Spawns background worker thread so the interface doesn't freeze."""
        self.action_btn.configure(state="disabled", text="VOICE RECOGNITION ACTIVE")
        self.mode_label.configure(text="LISTENING", text_color="#deff9a")
        
        # Fire off the worker thread
        voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
        voice_thread.start()

    def voice_loop(self):
        """Background loop reading audio streams and invoking processing pipelines."""
        # Initial greeting aloud
        self.natalia.speak("Systems fully operational. I am Natalia. Awaiting your voice command.")
        self.insert_log("\n[NATALIA] Awaiting voice command...\n")

        while True:
            try:
                # 1. Listen for mic audio
                voice_text = self.listener.listen()
                
                # Render speech to text translation instantly inside the HUD
                self.root.after(0, self.insert_log, f"\n[YOU] {voice_text}\n")

                if "exit system" in voice_text or "shutdown" in voice_text or "quit" in voice_text:
                    self.natalia.speak("Shutting down tactical assistant. Stay safe out there.")
                    self.root.after(0, self.root.quit)
                    break

                # 2. Extract procedures from data mapping configuration
                response = self.nlp.process_query(voice_text)

                # 3. Print output and invoke text-to-speech engine
                self.root.after(0, self.insert_log, f"[NATALIA] {response}\n")
                self.natalia.speak(response)

            except Exception as e:
                print(f"Loop Exception: {e}")
                break

    def on_closing(self):
        """Gracefully terminates system assets upon window destruction."""
        print("Closing application modules cleanly...")
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = NataliaGUI()
    app.root.mainloop()