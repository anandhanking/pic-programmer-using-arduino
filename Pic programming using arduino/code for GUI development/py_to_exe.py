import tkinter as tk
from tkinter import filedialog
import subprocess


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Python to EXE Converter")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # File selection button
        self.file_button = tk.Button(self, text="Select Python file", command=self.select_file)
        self.file_button.pack(pady=10)

        # Conversion button
        self.convert_button = tk.Button(self, text="Convert to EXE", command=self.convert_file)
        self.convert_button.pack(pady=10)

        # Status text
        self.status_text = tk.StringVar()
        self.status_text.set("No file selected.")
        self.status_label = tk.Label(self, textvariable=self.status_text)
        self.status_label.pack(pady=10)

    def select_file(self):
        filetypes = [("Python files", "*.py")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.status_text.set(f"Selected file: {filename}")
            self.filename = filename

    def convert_file(self):
        try:
            cmd = f'pyinstaller "{self.filename}" --onefile -w'
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            if process.returncode == 0:
                self.status_text.set("Conversion successful!")
            else:
                self.status_text.set("Conversion failed.")
                print(error.decode())
        except AttributeError:
            self.status_text.set("No file selected.")
        except Exception as e:
            self.status_text.set(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()