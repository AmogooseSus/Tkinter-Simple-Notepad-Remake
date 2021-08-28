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
        #Creates a new top level window and sets it properties
        self.box = tk.Toplevel(self.root)
        self.box.geometry("200x200")
        self.box.title(self.window_title)
        self.box.grab_current()
        #binds the Red cross exit to the close function
        self.box.protocol("WM_DELETE_WINDOW",
                          lambda: self.handle_close(self.box))
        #label to show request information
        self.label = ttk.Label(self.box, text=self.window_text)
        self.label.pack()
        
        #entry to get the input
        self.entry = ttk.Entry(self.box)
        self.entry.pack()

        #button to allow users to confirm their choice as well to validate it
        self.confirm = ttk.Button(self.box, text="Confirm")
        self.confirm.pack()
        self.confirm["command"] = self.validate
        #ensures that the window only closes when input has been recieved 
        #causing the execution of the programming to halt at this window
        self.confirm.wait_variable(self.wait_var)
        self.box.destroy()

    def validate(self):
        #regex for anything that isn't whitespace
        match = re.compile(".+")
        if match.match(self.entry.get()):
            self.wait_var.set(self.entry.get())
        else:
            showerror("Value Error", "Invalid Name")
            self.box.grab_current()

    def handle_close(self, box):
        del self
        box.destroy()
