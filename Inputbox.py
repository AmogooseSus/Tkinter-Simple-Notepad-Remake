import tkinter as tk
from tkinter import ttk
import re
from tkinter.messagebox import *


class inputbox(object):

    def __init__(self, window_title, window_text, root, wait_var) -> None:
        super().__init__()
        self.window_title = window_title
        self.window_text = window_text
        self.root = root
        self.wait_var = wait_var
        self.generate_view()

    def generate_view(self):
        self.box = tk.Toplevel(self.root)
        self.box.geometry("200x200")
        self.box.title(self.window_title)
        self.box.grab_current()
        self.box.protocol("WM_DELETE_WINDOW",
                          lambda: self.handle_close(self.box))

        self.label = ttk.Label(self.box, text=self.window_text)
        self.label.pack()

        self.entry = ttk.Entry(self.box)
        self.entry.pack()

        self.confirm = ttk.Button(self.box, text="Confirm")
        self.confirm.pack()
        self.confirm["command"] = self.validate
        self.confirm.wait_variable(self.wait_var)
        self.box.destroy()

    def validate(self):
        match = re.compile(".+")
        if match.match(self.entry.get()):
            self.wait_var.set(self.entry.get())
            print("Did run")
        else:
            showerror("Value Error", "Invalid Name")

    def handle_close(self, box):
        del self
        box.destroy()
