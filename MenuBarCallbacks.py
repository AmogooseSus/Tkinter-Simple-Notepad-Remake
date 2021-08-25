from tkinter import Menu


def generate_menudata_dict(name, callback_func, keyboard_shortcut):
    return {"Name": name, "Callback": callback_func, "Shortcut": keyboard_shortcut}


class MenuBar:

    def __init__(self, root, textarea):
        self.root = root
        self.textarea = textarea
        self.filemenu_data = [
            generate_menudata_dict(
                "New Control-N", self.new_area, "<Control-n>"),
            generate_menudata_dict(
                "New Window Control-Shift-N", self.new_window, "<Control-Shift-n>"),
            generate_menudata_dict(
                "Open Control-o", self.open_file, "<Control-O>")
        ]
        self.create_visuals()

    def create_visuals(self):
        # Set up a menu bar and link it with the main window
        self.menubar = Menu(self.root)
        self.root["menu"] = self.menubar

        # create a new menu, a child for the bar
        self.file_menu = Menu(self.menubar, tearoff=False)
        for x in self.filemenu_data:
            self.file_menu.add_command(label=x["Name"], command=x["Callback"])
            self.root.bind(x["Shortcut"], x["Callback"])

        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def new_area(self, e=None):
        print("owrks")

    def new_window(self, e=None):
        pass

    def open_file(self, e=None):
        pass

    def save(self, e=None):
        pass

    def save_as(self, e=None):
        pass

    def exit(self, e=None):
        pass
