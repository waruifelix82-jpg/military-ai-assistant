import threading
import sys
import customtkinter as ctk

# Import your existing backend classes
from audio_input import AudioInput
from nlp_engine import NLPEngine
from audio_output import AudioOutput

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernNataliaGUI:
    def __init__(self):
        # 1. Initialize Backend Core System Assets
        self.listener = AudioInput()
        self.nlp = NLPEngine()
        self.natalia = AudioOutput()

        # 2. Main Window Blueprint
        self.root = ctk.CTk()
        self.root.title("NATALIA // COGNITIVE HUD v2.5")
        self.root.geometry("900x650")  # Expanded slightly for the input box
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 3. Grid Configuration (Asymmetric Sidebar Layout)
        self.root.grid_columnconfigure(0, weight=1, minsize=220) # Sidebar
        self.root.grid_columnconfigure(1, weight=3)             # Main Console
        self.root.grid_rowconfigure(0, weight=1)

        # ==========================================
        # SIDEBAR PANEL (System Status & Quick Actions)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#0d1117")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.brand_lbl = ctk.CTkLabel(
            self.sidebar, 
            text="NATALIA AI", 
            font=("Courier New", 26, "bold"), 
            text_color="#00f0ff"
        )
        self.brand_lbl.pack(padx=20, pady=(30, 10))

        self.sub_lbl = ctk.CTkLabel(
            self.sidebar, 
            text="HYBRID CORE ENGINE", 
            font=("Arial", 11, "bold"), 
            text_color="#555555"
        )
        self.sub_lbl.pack(padx=20, pady=(0, 30))

        self.div = ctk.CTkFrame(self.sidebar, height=2, fg_color="#1f242c")
        self.div.pack(fill="x", padx=20, pady=10)

        self.telemetry_title = ctk.CTkLabel(self.sidebar, text="SYSTEM STATUS:", font=("Courier New", 12, "bold"), text_color="#888")
        self.telemetry_title.pack(anchor="w", padx=25, pady=(10, 5))

        self.status_lbl = ctk.CTkLabel(self.sidebar, text="• ONLINE [SECURE]", font=("Courier New", 14, "bold"), text_color="#39ff14")
        self.status_lbl.pack(anchor="w", padx=35, pady=2)

        self.mode_lbl = ctk.CTkLabel(self.sidebar, text="• MODE: STANDBY", font=("Courier New", 14, "bold"), text_color="#ffb300")
        self.mode_lbl.pack(anchor="w", padx=35, pady=2)

        self.action_btn = ctk.CTkButton(
            self.sidebar, 
            text="ENGAGE COGNITIVE LINK", 
            font=("Courier New", 12, "bold"),
            fg_color="#00f0ff",
            text_color="#000000",
            hover_color="#00c8d7",
            height=40,
            command=self.start_voice_thread
        )
        self.action_btn.pack(side="bottom", fill="x", padx=20, pady=30)

        # ==========================================
        # MAIN CENTRAL CONSOLE TERMINAL
        # ==========================================
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=3) # Primary HUD Display
        self.main_container.grid_rowconfigure(1, weight=1) # Diagnostic Log Frame
        self.main_container.grid_rowconfigure(2, weight=0) # Text Input Row

        # Live HUD Dialogue Display Box
        self.display_box = ctk.CTkTextbox(
            self.main_container, 
            font=("Courier New", 15), 
            text_color="#f5f5f5",
            border_width=1,
            border_color="#1f242c",
            fg_color="#161b22"
        )
        self.display_box.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Diagnostic Live Ticker Display Box
        self.diag_box = ctk.CTkTextbox(
            self.main_container,
            font=("Courier New", 11),
            text_color="#8b949e",
            border_width=1,
            border_color="#1f242c",
            fg_color="#0d1117"
        )
        self.diag_box.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

        # ---- NEW: TEXT INPUT BAR CONFIGURATION ----
        self.input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.text_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type tactical command here and press Enter...",
            font=("Courier New", 14),
            fg_color="#0d1117",
            border_color="#1f242c",
            text_color="#ffffff"
        )
        self.text_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        # Bind the Enter key directly to processing function
        self.text_entry.bind("<Return>", lambda event: self.process_text_input())

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="EXECUTE",
            font=("Courier New", 12, "bold"),
            width=100,
            fg_color="#1f242c",
            text_color="#00f0ff",
            hover_color="#161b22",
            command=self.process_text_input
        )
        self.send_btn.grid(row=0, column=1, sticky="e")
        # --------------------------------------------

        self.insert_hud_text("// NATALIA HYBRID INTERFACE INITIALIZED\n// TEXT & VOICE PROCESSING CHANNELS READY...\n")
        self.insert_diag_text("[CORE] Text terminal link online.\n")

    def insert_hud_text(self, text):
        self.display_box.insert("end", text)
        self.display_box.see("end")

    def insert_diag_text(self, text):
        self.diag_box.insert("end", text)
        self.diag_box.see("end")

    def process_text_input(self):
        """Processes query typed directly into the input entry box."""
        user_text = self.text_entry.get().strip()
        
        if not user_text:
            return

        # Clear the field instantly for next command
        self.text_entry.delete(0, "end")

        # Display the text inputs on the HUD and Diag frames
        self.insert_hud_text(f"\n[TEXT_CMD] >> {user_text}\n")
        self.insert_diag_text(f"[KEYBOARD] Intercepted text command string.\n")

        # Graceful manual system exits via keyboard text
        if user_text.lower() in ["exit system", "shutdown", "quit"]:
            self.insert_hud_text("[NATALIA] >> Shutting down tactical assistant. Stay safe.\n")
            self.natalia.speak("Shutting down tactical assistant. Stay safe out there.")
            self.root.quit()
            return

        # Match query using our native JSON-driven processor engine
        self.insert_diag_text(f"[NLP] Query parsing active...\n")
        response = self.nlp.process_query(user_text)

        # Output the results visually and read aloud safely
        self.insert_hud_text(f"[NATALIA] >> {response}\n")
        
        # Fire text-to-speech in a background step so the typing interface stays smooth
        threading.Thread(target=self.natalia.speak, args=(response,), daemon=True).start()
        self.insert_diag_text("[AUDIO] Speech synthesis thread executed.\n")

    def start_voice_thread(self):
        self.action_btn.configure(state="disabled", text="LINK ACTIVE", fg_color="#1f242c", text_color="#888")
        self.mode_lbl.configure(text="• MODE: LISTENING", text_color="#00f0ff")
        
        voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
        voice_thread.start()

    def voice_loop(self):
        self.natalia.speak("Systems fully operational. I am Natalia. Awaiting your voice command.")
        self.insert_hud_text("\n[NATALIA] Ready for tactical inquiries...\n")

        while True:
            try:
                self.root.after(0, self.insert_diag_text, "[MIC] Listening to audio channel input...\n")
                voice_text = self.listener.listen()
                
                self.root.after(0, self.insert_hud_text, f"\n[USER_CMD] >> {voice_text}\n")
                self.root.after(0, self.insert_diag_text, f"[NLP] Tokenizing input: '{voice_text[:20]}...'\n")

                if "exit system" in voice_text or "shutdown" in voice_text or "quit" in voice_text:
                    self.natalia.speak("Shutting down tactical assistant. Stay safe out there.")
                    self.root.after(0, self.root.quit)
                    break

                response = self.nlp.process_query(voice_text)

                self.root.after(0, self.insert_hud_text, f"[NATALIA] >> {response}\n")
                self.root.after(0, self.insert_diag_text, "[AUDIO] Generating local speech synthesis output stream...\n")
                self.natalia.speak(response)

            except Exception as e:
                print(f"Loop Error: {e}")
                break

    def on_closing(self):
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = ModernNataliaGUI()
    app.root.mainloop()