# simple tk window for submitting individual credentials to the credentials api

import tkinter as tk
from credentials import add_credential
from authusers import load_config

def on_submit():
    
    u, p = load_config()
    
    # clear error msg if exists
    error_label.config(text="")
    
    service = service_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if not service or not username or not password:
        error_label.config(text="Please fill out each field")
    else:
        add_credential(service, username, password, u, p)
        # clear fields
        service_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

# main window init
root = tk.Tk()
root.title("Add Credentials")
root.geometry("800x600")

# font definitions
title_font = ("Arial", 24, "bold")
label_font = ("Arial", 18)
entry_font = ("Arial", 16)
error_font = ("Arial", 16, "italic")
button_font = ("Arial", 18)

# frame init for widget layout
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill=tk.BOTH)

# frame grid layout
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)
frame.rowconfigure(3, weight=1)
frame.rowconfigure(4, weight=1)
frame.rowconfigure(5, weight=1)
frame.rowconfigure(6, weight=1)

# title label
title_label = tk.Label(frame, text="Enter New Credentials", font=title_font)
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# error label. shown if missing at least one field
error_label = tk.Label(frame, text="", fg="red", font=error_font)
error_label.grid(row=1, column=0, columnspan=3)

# input fields created and placed
service_label = tk.Label(frame, text="Service", font=label_font)
service_label.grid(row=2, column=0, pady=5)
service_entry = tk.Entry(frame, font=entry_font)
service_entry.grid(row=2, column=1, columnspan=2, pady=5)

username_label = tk.Label(frame, text="Username", font=label_font)
username_label.grid(row=3, column=0, pady=5)
username_entry = tk.Entry(frame, font=entry_font)
username_entry.grid(row=3, column=1, columnspan=2, pady=5)

password_label = tk.Label(frame, text="Password", font=label_font)
password_label.grid(row=4, column=0, pady=5)
password_entry = tk.Entry(frame, font=entry_font, show="*")
password_entry.grid(row=4, column=1, columnspan=2, pady=5)

# submission btn created and placed
submit_button = tk.Button(frame, text="Submit", font=button_font, command=on_submit)
submit_button.grid(row=5, column=0, columnspan=3, pady=20)

# additional padding placed at bottom of window
frame.grid_rowconfigure(6, minsize=20)

# mainloop (not redundant at all). runs mainloop
# run the mainloop
# starts the mainloop
# run gui
root.mainloop()

