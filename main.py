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
        # To keep track of the current textsize in the editor
        self.textsize = 12
        # initlise winodw properties
        self.setup_window()
        # initlise the widgets for the editor
        self.generate_textarea()
        # initlise the menubar for the window
        self.menubar = MenuBar(self, self.textarea)

    def setup_window(self):
        #
        self.title("Untitled - Notepad")
        self.iconbitmap("./notepad.ico")
        self.geometry("1080x800")

    def generate_textarea(self):
        self.textarea = ScrolledText(self, font=(
            "Helvetica", self.textsize))
        self.textarea.place(relheight=1.0, relwidth=1.0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
