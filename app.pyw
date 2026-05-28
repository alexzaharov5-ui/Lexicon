import os
import threading
import whisper
import customtkinter as ctk
from tkinter import filedialog
import builtins
from tinytag import TinyTag

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Audio to Text (Whisper Max)")
        self.geometry("620x600")
        self.resizable(False, False)
        
        self.stop_event = threading.Event()
        self.file_path = ""
        self.total_duration = 0.0
        
        self.label_title = ctk.CTkLabel(self, text="Audio to Text Converter", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.pack(pady=15)
        
        self.btn_select = ctk.CTkButton(self, text="Select File", command=self.select_file, fg_color="#2b2b2b", hover_color="#3e3e3e", height=35)
        self.btn_select.pack(pady=5)
        
        self.label_file = ctk.CTkLabel(self, text="No file selected", text_color="gray", wraplength=500)
        self.label_file.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self, width=540)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.label_percentage = ctk.CTkLabel(self, text="Progress: 0%", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_percentage.pack(pady=2)
        
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(pady=10)
        
        self.btn_start = ctk.CTkButton(self.frame_buttons, text="Start", command=self.start_transcription_thread, state="disabled", fg_color="#2b2b2b", hover_color="#3e3e3e", width=150, height=35)
        self.btn_start.grid(row=0, column=0, padx=10)
        
        self.btn_stop = ctk.CTkButton(self.frame_buttons, text="Stop / Reset", command=self.stop_transcription, state="disabled", fg_color="#5a5a5a", hover_color="#6e6e6e", width=150, height=35)
        self.btn_stop.grid(row=0, column=1, padx=10)
        
        self.label_monitor = ctk.CTkLabel(self, text="Text from audio with timestamps:", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_monitor.pack(pady=(10, 0), anchor="w", padx=30)
        
        self.text_box = ctk.CTkTextbox(self, width=540, height=220, activate_scrollbars=True)
        self.text_box.pack(pady=5, padx=30)
        self.text_box.insert("0.0", "The text with timestamps will appear here during processing...")
        
        self.label_status = ctk.CTkLabel(self, text="Status: Waiting for file", font=ctk.CTkFont(size=12))
        self.label_status.pack(pady=10)

    def select_file(self):
        file_types = [("Media Files", "*.mp3 *.mp4 *.wav *.mkv *.m4a *.avi"), ("All Files", "*.*")]
        self.file_path = filedialog.askopenfilename(filetypes=file_types)
        if self.file_path:
            try:
                tag = TinyTag.get(self.file_path)
                self.total_duration = tag.duration if tag.duration else 0.0
            except:
                self.total_duration = 0.0
                
            self.label_file.configure(text=f"Selected: {os.path.basename(self.file_path)}", text_color="white")
            self.btn_start.configure(state="normal")
            self.label_status.configure(text="Status: Ready to start")
            self.progress_bar.set(0)
            self.label_percentage.configure(text="Progress: 0%")

    def start_transcription_thread(self):
        self.stop_event.clear()
        threading.Thread(target=self.run_transcription, daemon=True).start()

    def stop_transcription(self):
        self.stop_event.set()
        self.label_status.configure(text="Status: Stopping process...", text_color="gray")
        self.btn_stop.configure(state="disabled")

    def run_transcription(self):
        self.btn_select.configure(state="disabled")
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.label_status.configure(text="Status: Loading AI model...", text_color="gray")
        self.text_box.delete("0.0", "end") 

        try:
            model = whisper.load_model("small")
            self.label_status.configure(text="Status: Transcribing audio...", text_color="gray")
            
            original_print = whisper.transcribe.__globals__.get('print')
            
            def custom_print(*args, **kwargs):
                if self.stop_event.is_set():
                    raise KeyboardInterrupt()
                if args:
                    msg = str(args[0])
                    if "-->" in msg:
                        try:
                            time_part, text_part = msg.split("]", 1)
                            time_range = time_part.replace("[", "").strip()
                            clean_text = text_part.strip()
                            
                            start_time_str = time_range.split("-->")[0].strip()
                            minutes, seconds = start_time_str.split(":")
                            current_seconds = int(minutes) * 60 + float(seconds)
                            
                            if self.total_duration > 0:
                                progress = min(current_seconds / self.total_duration, 1.0)
                                self.progress_bar.set(progress)
                                self.label_percentage.configure(text=f"Progress: {int(progress * 100)}%")
                        except:
                            time_range = "⏱️"
                            clean_text = msg
                        
                        formatted_line = f"[{time_range}] {clean_text}\n"
                        self.text_box.insert("end", formatted_line)
                        self.text_box.see("end")

            builtins.print = custom_print
            result = model.transcribe(self.file_path, language="ru", verbose=True)
            builtins.print = original_print

            if not self.stop_event.is_set():
                output_text_path = os.path.splitext(self.file_path)[0] + "_text.txt"
                with open(output_text_path, "w", encoding="utf-8") as f:
                    f.write(result["text"])
                self.progress_bar.set(1.0)
                self.label_percentage.configure(text="Progress: 100%")
                self.label_status.configure(text="Status: Saved successfully!", text_color="gray")
            else:
                self.label_status.configure(text="Status: Transcription stopped", text_color="gray")
                
        except (KeyboardInterrupt, Exception) as e:
            builtins.print = original_print
            if self.stop_event.is_set():
                self.label_status.configure(text="Status: Transcription stopped", text_color="gray")
            else:
                self.label_status.configure(text=f"Status: Error: {str(e)}", text_color="gray")
        finally:
            self.btn_select.configure(state="normal")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="disabled")

if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()