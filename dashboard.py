import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import re

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Dashboard")
        self.root.geometry("800x500")
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=5)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(header_frame, text="Status: Monitoring...")
        self.status_label.pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        clear_button = ttk.Button(button_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Live preview (top gray box)
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.X, pady=(0, 10))
        self.preview_var = tk.StringVar()
        self.preview_entry = tk.Entry(preview_frame, textvariable=self.preview_var, font=("Arial", 18), state="readonly", justify="left", readonlybackground="#ededed")
        self.preview_entry.pack(fill=tk.X, padx=10, pady=5, ipady=8)
        
        # Text area with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Start updating
        self.update_logs()
    
    def clear_logs(self):
        self.text.delete(1.0, tk.END)
        self.preview_var.set("")
        # Clear the keylog.txt file
        with open('keylog.txt', 'w') as f:
            f.write("")
        self.status_label.config(text="Status: Logs cleared")
        self.root.after(2000, lambda: self.status_label.config(text="Status: Monitoring..."))
    
    def reconstruct_text(self, log_content):
        # Extract only the actual characters typed
        chars = []
        for line in log_content.splitlines():
            match = re.search(r"Key pressed: (.+)", line)
            if match:
                key = match.group(1)
                if key.startswith("'") and key.endswith("'") and len(key) == 3:
                    chars.append(key[1])
                elif key == "Key.space":
                    chars.append(' ')
                elif key == "Key.enter":
                    chars.append('\n')
                elif key == "Key.tab":
                    chars.append('\t')
                elif key == "Key.backspace":
                    if chars:
                        chars.pop()
                # Ignore other special keys
        return ''.join(chars)
    
    def update_logs(self):
        try:
            with open('keylog.txt', 'r') as file:
                content = file.read()
                if content:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, content)
                    self.text.see(tk.END)  # Scroll to bottom
                    self.status_label.config(text=f"Status: Last updated {datetime.now().strftime('%H:%M:%S')}")
                    # Update live preview
                    preview = self.reconstruct_text(content)
                    self.preview_var.set(preview)
                    # Move cursor to end so preview scrolls with text
                    self.preview_entry.icursor(tk.END)
        except FileNotFoundError:
            self.status_label.config(text="Status: Waiting for log file...")
            self.preview_var.set("")
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {str(e)}")
            self.preview_var.set("")
        
        self.root.after(1000, self.update_logs)

def main():
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main() 