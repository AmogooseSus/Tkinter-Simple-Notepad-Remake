from tkinter import Menu
import tkinter
from tkinter.constants import EW, NS, NSEW
import tkinter.filedialog as fd
from tkinter import ttk
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
                "New Window Control-Shift-N", self.new_window, "<Control-Shift-KeyPress-n>"),
            generate_menudata_dict(
                "Open Control-o", self.open_file, "<Control-o>"),
            generate_menudata_dict("Save Control-S", self.save, "<Control-s>"),
            generate_menudata_dict(
                "Save As Control-Shift-S", self.save_as, "<Control-Shift-KeyPress-s>"),
            generate_menudata_dict("Exit Control-E", self.exit, "<Control-e>")
        ]
        self.editmenu_data = [generate_menudata_dict(
            "Find Control-F", self.find, "<Control-f>"),
            generate_menudata_dict("Replace Control-H",
                                   self.replace, "<Control-h>"),
            generate_menudata_dict("Go To Control-G", self.Go_to, "<Control-g>")]

        self.create_visuals()
        # bind the red cross close to the exit function
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        # used to keep track for the find function
        self.last_line_checked = 0

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

        # create the edit menu and its items
        self.edit_menu = Menu(self.menubar, tearoff=False)
        for x in self.editmenu_data:
            self.edit_menu.add_command(label=x["Name"], command=x["Callback"])
            self.root.bind(x["Shortcut"], x["Callback"])

        # add the item to the menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

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
        if self.filename.get() == "None":
            print("Input box closed")
            return

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

    def find(self, e=None):
        find_window = tkinter.Toplevel(self.root)
        find_window.geometry("250x50")
        find_window.resizable(0, 0)
        find_window.grab_current()

        find_window.columnconfigure(0, weight=2)
        find_window.columnconfigure(1, weight=1)

        find_value = tkinter.StringVar()
        find_entry = ttk.Entry(find_window, textvariable=find_value)
        find_entry.grid(row=0, column=0, sticky=NS, pady=10)
        # ensures when user changes the find input the line to check is reset
        find_value.trace("w", self.reset_line_check)

        find_btn = ttk.Button(find_window, text="Find/ Find Next")
        find_btn.grid(row=0, column=1, sticky=NS, pady=10)
        find_btn["command"] = lambda: self.find_word(
            find_value, self.highlight_words)

        find_window.protocol("WM_DELETE_WINDOW",
                             lambda: self.handle_findclose(find_window))

    def reset_line_check(self, a=None, b=None, c=None):
        self.last_line_checked = 0

    # allows you to find a word(s) in the text line by line
    def find_word(self, input, action_to_peform_onword):
        # gets rid of the highlight(s) on the previous line
        self.textarea.tag_delete("search")
        # gets the string value of text and gets rid of any whitespace
        input_filtered = input.get().strip()
        # check if we even have any valid input
        if input_filtered == "":
            return

        # get the total amount of lines to search through
        total_lines = int(self.root.textarea.index('end-1c').split('.')[0])

        # ensure we don't check beyond lines that don't exist
        if self.last_line_checked >= total_lines:
            # back to the first line
            self.last_line_checked = 1
        else:
            # increment so we can check the next line
            self.last_line_checked += 1

        # get the text from the line we have to check
        line_to_check = self.textarea.get(
            f'{self.last_line_checked}.0', f'{self.last_line_checked}.{END}')
        entire_text = self.textarea.get("1.0", END).strip()
        # use reg exp and set the value to the text user wants to find
        pattern = re.compile(input_filtered)

        # check if this line even has the desired word(s) and if so highlight them
        if pattern.search(line_to_check):
            # variables to store word information for text widget
            word_startline = self.last_line_checked
            word_startcol = 0
            word_endcol = 0
            word = ""
            # loop every index of each character in the line
            for x in range(len(line_to_check)):
                """
                if the character is a whitespace (meaning we've passed a word)
                reset the word var to an empty string
                and set the start_col to the current index of the character + 1
                and continue to the iteration 
                """
                if line_to_check[x] == " ":
                    word = ""
                    word_startcol = x + 1
                    continue
                # add the current character to the word
                word += line_to_check[x]
                # if the word is == to the user requested word
                if word == input_filtered:
                    # set the end column to the current index
                    word_endcol = x + 1
                    print(f'{word_startline}.{word_startcol}',
                          f'{word_startline}.{word_endcol}')

                    action_to_peform_onword(f'{word_startline}.{word_startcol}',
                                            f'{word_startline}.{word_endcol}')
                    # add a tag to that section of the text
                    # self.textarea.tag_add(
                    #     "search", f'{word_startline}.{word_startcol}', f'{word_startline}.{word_endcol}')
                    # # change that section of texts properties to highlight it as important
                    # self.textarea.tag_config("search", background="yellow",
                    #                          foreground="blue")

                    # # Go to the highlighted word and move the users cursor there
                    # self.textarea.mark_set(
                    #     "insert", f'{word_startline}.{word_startcol}')
                    # self.textarea.see(f'{word_startline}.{word_startcol}')

                    # reset the word and start col to the next char incase the word appears multiple times
                    word = ""
                    word_startcol = x + 1
            # to stop the recursion
            return
        # to ensure user is directed to the next occurence of the word rather than having to manually get to it line by line
        # and ensures that the word they're looking for is even in the entire text
        elif pattern.search(entire_text):
            self.find_word(input, action_to_peform_onword)
        else:
            showerror("Word not found",
                      "The word could not be found in the file")

    # highlights words based on their position in textarea
    def highlight_words(self, start, end):
        # add a tag to that section of the text
        self.textarea.tag_add(
            "search", start, end)
        # change that section of texts properties to highlight it as important
        self.textarea.tag_config("search", background="yellow",
                                 foreground="blue")

        # Go to the highlighted word and move the users cursor there
        self.textarea.mark_set(
            "insert", start)
        self.textarea.see(start)

    def handle_findclose(self, find_window):
        # get rid of any highlted text
        self.textarea.tag_delete("search")
        self.reset_line_check()
        # close the window
        find_window.destroy()

    # handles replace window
    def replace(self, e=None):
        # UI
        replace_window = tkinter.Toplevel(self.root)
        replace_window.geometry("350x100")
        replace_window.resizable(0, 0)
        replace_window.grab_current()

        replace_window.columnconfigure(0, weight=1)
        replace_window.columnconfigure(1, weight=3)
        replace_window.columnconfigure(2, weight=1)

        replace_window.rowconfigure(0, weight=1)
        replace_window.rowconfigure(1, weight=1)

        replace_what_label = ttk.Label(replace_window, text="Find What")
        replace_what_input = ttk.Entry(replace_window)
        replace_what_input.grid(column=1, row=0, sticky=EW)
        replace_what_label.grid(column=0, row=0, sticky=EW)

        replace_with_label = ttk.Label(replace_window, text="Replace With")
        replace_with_input = ttk.Entry(replace_window)
        replace_with_label.grid(column=0, row=1, sticky=EW)
        replace_with_input.grid(column=1, row=1, sticky=EW)

        replace_btn = ttk.Button(replace_window, text="Replace/ Replace Next")
        replace_btn.grid(column=2, row=0, sticky=EW, padx=20)

        replace_all = ttk.Button(replace_window, text="Replace All")
        replace_all.grid(column=2, row=1, sticky=EW, padx=20)

        # events
        replace_btn["command"] = lambda: self.replace_algorithm(
            replace_what_input, replace_with_input.get())

    def replace_algorithm(self, find_word, replace_word):
        start = None
        end = None

        def callback(s, e):
            global start
            global end
            start = s
            end = e

        self.find_word(find_word, callback)

        if not start == None and not end == None:
            print("did run")
            self.textarea.tag_add("replaceable", start, end)
            self.textarea.tag_config("replaceable", text=replace_word)

    def Go_to():
        pass
