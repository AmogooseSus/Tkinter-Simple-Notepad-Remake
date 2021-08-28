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

# class to manage all functions related to the menubaar


class MenuBar:

    def __init__(self, root, textarea):
        # references to the main window and textarea
        self.root = root
        self.textarea = textarea
        # store the menu items and their hotkeys
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
        # bind the red cross close to the exit function
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    def create_visuals(self):
        # Set up a menu bar and link it with the main window
        self.menubar = Menu(self.root)
        self.root["menu"] = self.menubar

        # create a new menu, a child for the bar
        self.file_menu = Menu(self.menubar, tearoff=False)
        for x in self.filemenu_data:
            # set up the text,click callback and the hotkey for the command
            self.file_menu.add_command(label=x["Name"], command=x["Callback"])
            self.root.bind(x["Shortcut"], x["Callback"])

        # add the item to the menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def new_area(self, e=None):
        if not self.check_hassaved():
            self.generate_savewarning()
        # reset the currently opened file
        self.open_file_helper(None, None)
        # delete all the text from the area
        self.textarea.delete("1.0", END)

    def new_window(self, e=None):
        pass

    def open_file(self, e=None):
        if not self.check_hassaved():
            self.generate_savewarning()
        # ask for the file and open it
        file = fd.askopenfile()
        # incase the user doesn't select a file
        if file == None:
            return
        self.textarea.delete("1.0", END)
        """
        algorithim to get the directory and filename seperately 
        1- splits the returned full directory by "/"
        2- loops the array of string
        3- checks if the item isn't the last or second last
        4- if so then add it the filedir var bur with "/" concatnated
        5- else if it isn't the last item (second last in this case) also add it to filedir var 
        6- else set the filename var to the item (final index)
        """
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
        # sets the currently opened file attributes of the main winodw
        self.open_file_helper(filedir, filename)
        # reads lines from the text file and adds them to text area
        lines_towrite = file.readlines()
        for line in range(len(lines_towrite)):
            self.textarea.insert(f'{line + 1}.0', lines_towrite[line])
        file.close()

    def save(self, e=None):
        # used to check if we even have a file opened
        if self.root.currently_opened == None:
            return self.save_as()
        # sets the location to the files directory and filename
        self.location = f'{self.root.currently_opened}/{self.root.currently_filename}'
        self.saving_proceddure()

    def save_as(self, e=None):
        # Gets the filename desried
        self.filename = tkinter.StringVar()
        self.inputbox = inputbox(
            "File Name Request", "Please enter a filename", self.root, self.filename)
        self.directory = fd.askdirectory()
        # sets the location to the dir and filename concatnated with "/"
        self.location = f'{self.directory}/{self.filename.get()}.txt'
        self.saving_proceddure()
        # set the main winodws currently opened file attributes
        self.open_file_helper(self.directory, self.filename.get() + ".txt")

    def saving_proceddure(self):
        # gets the text from the textarea
        text_to_save = self.textarea.get("1.0", END)
        # opens the file to save
        # ensures the location is correctly formated
        file = open(self.location, "w")
        # saves the text to the file and informs the user if it worked or not
        try:
            file.writelines(text_to_save)
            file.close()
            showinfo("Success", f'Sucessfully saved the file')
        except:
            showerror("Error Saving", "Could not save the file")

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
        self.root.title(name if self.root.currently_opened !=
                        None else "Untitled" + " - " + "Notepad")

    def check_hassaved(self):
        # checks if we even have a file open
        if self.root.currently_opened == None:
            # check if the textareas empty
            empty_txt = self.textarea.get("1.0", END).strip()
            if empty_txt == "":
                return True
            return False
        # Opens the file and comapres weather any new text has been added
        print(self.root.currently_opened, self.root.currently_filename)
        filedir = f'{self.root.currently_opened}/{self.root.currently_filename}'
        file_tocheck = open(filedir, "r")
        multilinetxt = file_tocheck.readlines()
        # gets the lines in the text in a string and gets rid of any whitespace
        multilinetxt = "".join(multilinetxt).strip()
        # gets the text in the textarea and gets rid of any whitespace
        compare_text = self.textarea.get("1.0", END).strip()
        if multilinetxt != compare_text:
            return False
        return True

    def generate_savewarning(self):
        self.warning = askyesno(
            "File not Saved", "Would you like to save?")
        if self.warning == True:
            self.save()
