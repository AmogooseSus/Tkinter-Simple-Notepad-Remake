from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from MenuBarCallbacks import *
from tkinter.scrolledtext import ScrolledText


# The main application class
class App(Tk):

    def __init__(self):
        super().__init__()
        # to keep track of currently open file
        self.currently_opened = None
        self.current_filename = None
        self.current_file = None
        # To keep track of the current textsize in the editor
        self.textsize = 12
        # initlise winodw properties
        self.setup_window()
        # initlise the widgets for the editor
        self.generate_textarea()
        # initlise the menubar for the window
        self.menubar = MenuBar(self, self.textarea)
        self.bind("<Control-MouseWheel>", self.changetext_size)

    def setup_window(self):
        self.title("Untitled - Notepad")
        self.iconbitmap("./notepad.ico")
        self.geometry("1080x800")

    def generate_textarea(self):
        self.textarea = ScrolledText(self, font=(
            "Helvetica", self.textsize))
        self.textarea.place(relheight=1.0, relwidth=1.0)

    def changetext_size(self, event):
        wheel_rotation = event.delta % 120
        print(wheel_rotation)
        if wheel_rotation == 1:
            self.textsize += 2
        else:
            self.textsize -= 2
        self.textarea["font"] = ("Helvetica", self.textsize)


if __name__ == "__main__":
    app = App()
    app.mainloop()
