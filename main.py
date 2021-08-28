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
        self.max_textsize = 24
        self.min_textsize = 8
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
            "Helvetica", self.textsize), undo=True, maxundo=-1)
        # relative units used to ensure textarea always takes up same space
        # regardless of window size
        self.textarea.place(relheight=1.0, relwidth=1.0)

    def changetext_size(self, event):
        # returns 120 if scrolling up , -120 if down
        wheel_rotation = event.delta
        # sets the textsize to a clamped value
        self.textsize = self.clamp(self.textsize, self.min_textsize, self.max_textsize,
                                   self.textsize + (1 if wheel_rotation == 120 else -1))
        self.textarea["font"] = ("Helvetica", self.textsize)

    # function ensure that values are clamped between min and max
    def clamp(self, val, min, max, change_val):
        if change_val < min or change_val > max:
            return val
        return change_val


if __name__ == "__main__":
    app = App()
    app.mainloop()
