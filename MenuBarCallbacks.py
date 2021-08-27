from tkinter import Menu
import tkinter
import tkinter.filedialog as fd
from tkinter import END
from tkinter.messagebox import *
import re
from Inputbox import inputbox
import os


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
                "Open Control-o", self.open_file, "<Control-o>"),
            generate_menudata_dict("Save Control-S", self.save, "<Control-s>"),
            generate_menudata_dict(
                "Save As Control-Shift-S", self.save_as, "<Control-Shift-s>"),
            generate_menudata_dict("Exit Control-E", self.exit, "<Control-e>")
        ]
        self.create_visuals()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

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
        pass

    def new_window(self, e=None):
        pass

    def open_file(self, e=None):
        if not self.check_hassaved():
            self.generate_savewarning()
        file = fd.askopenfile()
        if file == None:
            return
        dirs = file.name.split("/")
        filedir = ""
        filename = ""
        self.root.current_file = file
        for x in range(len(dirs)):
            if x != len(dirs) - 1 and x != len(dirs) - 2:
                filedir += dirs[x] + "/"
            elif x != len(dirs) - 1:
                filedir += dirs[x]
            else:
                filename = dirs[x]
        self.open_file_helper(filedir, filename)
        lines_towrite = file.readlines()
        for line in range(len(lines_towrite)):
            self.textarea.insert(f'{line + 1}.0', lines_towrite[line])
        file.close()

    def save(self, e=None):
        if self.root.currently_opened == None:
            return self.save_as()
        self.location = f'{self.root.currently_opened}/{self.root.currently_filename}'
        self.saving_proceddure()

    def save_as(self, e=None):
        self.filename = tkinter.StringVar()
        self.inputbox = inputbox(
            "File Name Request", "Please enter a filename", self.root, self.filename)
        self.directory = fd.askdirectory()
        self.location = f'{self.directory}/{self.filename.get()}'
        self.saving_proceddure()
        self.open_file_helper(self.directory, self.filename.get())

    def saving_proceddure(self):
        text_to_save = self.textarea.get("1.0", END)
        file = open(self.location +
                    ".txt" if self.location[-4:] != ".txt" else self.location, "w")
        file.writelines(text_to_save)
        file.close()
        showinfo("Success", f'Sucessfully saved the file')

    def exit(self, e=None):
        if not self.check_hassaved():
            self.generate_savewarning()
        leave_question = askyesno(
            "Are you sure?", "Would you like to quit")
        if leave_question:
            self.root.destroy()

    def open_file_helper(self, dir, name):
        self.root.currently_opened = dir
        self.root.currently_filename = name
        self.root.title(f'{name} - Notepad')

    def check_hassaved(self):
        if self.root.currently_opened == None:
            empty_txt = self.textarea.get("1.0", END).strip()
            if empty_txt == "":
                return True
            return False
        file_tocheck = open(self.root.currently_opened + "/"
                            + self.root.currently_filename, "r")
        multilinetxt = file_tocheck.readlines()
        multilinetxt = "".join(multilinetxt).strip()
        compare_text = self.textarea.get("1.0", END).strip()
        if multilinetxt != compare_text:
            return False
        return True

    def generate_savewarning(self):
        self.warning = askyesno(
            "File not Saved", "Would you like to save?")
        if self.warning == True:
            self.save()
