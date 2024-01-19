import tkinter as tk
import tkinter.filedialog as fd
import subprocess
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.read_button = tk.Button(self)
        self.read_button["text"] = "Read"
        self.read_button["command"] = self.read
        self.read_button.pack(side="left")

        self.write_button = tk.Button(self)
        self.write_button["text"] = "Write"
        self.write_button["command"] = self.write
        self.write_button.pack(side="left")
        
        self.erase_button = tk.Button(self)
        self.erase_button["text"] = "Erase"
        self.erase_button["command"] = self.erase
        self.erase_button.pack(side="left")

        self.quit_button = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit_button.pack(side="left")

        self.com_label = tk.Label(self, text="Com Port: ")
        self.com_label.pack(side="left")

        self.com_entry = tk.Entry(self)
        self.com_entry.pack(side="left")

        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.pack()

    def read(self):
        filename = fd.asksaveasfilename(defaultextension='.hex')
        if filename:
            com_port = self.com_entry.get()
            cmd = f'ardpicprog -p /dev/{com_port} -o {filename}'
            threading.Thread(target=self.run_command, args=(cmd,)).start()

    def write(self):
        filename = fd.askopenfilename(defaultextension='.hex')
        if filename:
            com_port = self.com_entry.get()
            cmd = f'ardpicprog -p /dev/{com_port} --erase --burn -i {filename}'
            confirm = tk.messagebox.askquestion(title="Confirmation", message=f"Do you want to write {filename} to the device?")
            if confirm == 'yes':
                threading.Thread(target=self.run_command, args=(cmd,)).start()

    def erase(self):
        com_port = self.com_entry.get()
        cmd = f'ardpicprog -p /dev/{com_port} --erase'
        threading.Thread(target=self.run_command, args=(cmd,)).start()

    def run_command(self, cmd):
        self.result_text.insert(tk.END, f"Running command: {cmd}\n")
        self.result_text.see(tk.END)
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.result_text.insert(tk.END, f"Command completed successfully.\n")
            else:
                self.result_text.insert(tk.END, f"Command failed with error code {process.returncode}.\n")
            self.result_text.insert(tk.END, stdout.decode('utf-8'))
            self.result_text.insert(tk.END, stderr.decode('utf-8'))
        except Exception as e:
            self.result_text.insert(tk.END, f"Command failed with exception {e}.\n")
        self.result_text.insert(tk.END, f"Command completed.\n")
        self.result_text.see(tk.END)

root = tk.Tk()
app = Application(master=root)
app.mainloop()