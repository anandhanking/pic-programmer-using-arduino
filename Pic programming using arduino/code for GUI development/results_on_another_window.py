import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


root = tk.Tk()
root.title("Arduino PIC Programmer")
root.geometry("400x400")
root.resizable(False, False)

comport_label = tk.Label(root, text="COM Port:")
comport_label.pack()

comport_entry = tk.Entry(root, width=10)
comport_entry.pack()

file_label = tk.Label(root, text="File Location:")
file_label.pack()

file_location = tk.StringVar()
file_location.set("")

file_location_label = tk.Label(root, textvariable=file_location)
file_location_label.pack()

def select_file():
    filetypes = (("HEX files", "*.hex"), ("All files", "*.*"))
    filename = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    file_location.set(filename)

def write_to_pic():
    comport = comport_entry.get()
    file = file_location.get()
    if comport == "":
        messagebox.showerror("Error", "Please enter a COM port number.")
    elif file == "":
        messagebox.showerror("Error", "Please select a file.")
    else:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to write to the PIC?")
        if confirm:
            command = f"ardpicprog -p /dev/{comport} --erase --burn -i {file}"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            messagebox.showinfo("Results", result.stdout)
        else:
            messagebox.showinfo("Information", "Write to PIC operation cancelled.")

def read_from_pic():
    comport = comport_entry.get()
    file = file_location.get()
    if comport == "":
        messagebox.showerror("Error", "Please enter a COM port number.")
    else:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to read from the PIC?")
        if confirm:
            command = f"ardpicprog -p /dev/{comport} -o {file}"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            messagebox.showinfo("Results", result.stdout)
        else:
            messagebox.showinfo("Information", "Read from PIC operation cancelled.")

def erase_pic():
    comport = comport_entry.get()
    if comport == "":
        messagebox.showerror("Error", "Please enter a COM port number.")
    else:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to erase the PIC?")
        if confirm:
            command = f"ardpicprog -p /dev/{comport} --erase"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            messagebox.showinfo("Results", result.stdout)
        else:
            messagebox.showinfo("Information", "Erase PIC operation cancelled.")

select_file_button = tk.Button(root, text="Select File", command=select_file)
select_file_button.pack()

write_button = tk.Button(root, text="Write to PIC", command=write_to_pic)
write_button.pack()

read_button = tk.Button(root, text="Read from PIC", command=read_from_pic)
read_button.pack()

erase_button = tk.Button(root, text="Erase PIC", command=erase_pic)
erase_button.pack()

root.mainloop()