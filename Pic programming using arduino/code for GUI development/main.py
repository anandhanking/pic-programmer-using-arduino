import tkinter as tk
import tkinter.filedialog as fd
import subprocess
import threading
import tkinter.messagebox as mbox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Microcontroller Programmer")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Row 1 - COM Port Entry
        self.com_label = tk.Label(self, text="COM Port:")
        self.com_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 5), sticky="w")

        self.com_entry = tk.Entry(self, width=10)
        self.com_entry.grid(row=0, column=1, pady=(10, 5))

        # Row 2 - Read Button
        self.read_button = tk.Button(self, text="Read Memory", command=self.read)
        self.read_button.grid(row=1, column=0, padx=(10, 5), pady=5)

        # Row 2 - Write Button
        self.write_button = tk.Button(self, text="Write Memory", command=self.write)
        self.write_button.grid(row=1, column=1, padx=(5, 10), pady=5)

        # Row 3 - Erase Button
        self.erase_button = tk.Button(self, text="Erase Memory", command=self.erase)
        self.erase_button.grid(row=2, column=0, padx=(10, 5), pady=5)

        # Row 3 - Quit Button
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Row 4 - Result Text Box
        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

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
            confirm = mbox.askquestion(title="Confirmation", message=f"Do you want to write {filename} to the device?")
            if confirm == 'yes':
                threading.Thread(target=self.run_command, args=(cmd,)).start()

    def erase(self):
        com_port = self.com_entry.get()
        cmd = f'ardpicprog -p /dev/{com_port} --erase'
        threading.Thread(target=self.run_command, args=(cmd,)).start()
  
    def run_command(self, cmd):
        self.result_text.delete(1.0, tk.END)  # clear result text box
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if not output:
                break
            self.result_text.insert(tk.END, output.decode('utf-8'))
            self.result_text.see(tk.END)
        while True:
            error = process.stderr.readline()
            if not error:
                break
            self.result_text.insert(tk.END, error.decode('utf-8'))
            self.result_text.see(tk.END)
        process.wait()
        if process.returncode == 0:
            mbox.showinfo(title="Success", message="Command executed successfully!")
        else:
            mbox.showerror(title="Error", message="An error occurred while executing the command.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()