from tkinter import Tk, Listbox, Button, Label, END, Toplevel, Text
import tkinter.font as tk_font
from tkinter.font import Font

import json

class ToDo:
    """
    Represents an instance of the To-Do List application.
    """
    def __init__(self) -> None:
        """
        Initializes the ToDo class. Sets up ui elements and class attributes.
        """
        self.root: Tk = Tk()
        self.root.geometry("450x300+500+200")
        self.root.resizable(False, False)
        self.root.title("To Do List")

        self.TITLE_FONT: str = "Trebuchet MS"
        self.FONT: str = "Courier New" 
        self.bg_color: str = "#abcdef"

        self.root.config(background=self.bg_color)

        self.title: Label = Label(self.root, text="TO-DO LIST",
                                  background=self.bg_color)
        self.title.place(relx=0.82, rely=0.1, anchor="center")

        title_font: Font = tk_font.Font(self.title, self.title.cget("font"))
        title_font.config(family=self.TITLE_FONT, underline=True, size=15)
        self.title.config(font=title_font)

        self.list: Listbox = Listbox(self.root, width=35, height=16,
                                     borderwidth=2,
                                     font=(self.FONT, 10),
                                     activestyle="none")
        self.list.place(relx=0.02, rely=0.04, anchor="nw")        


        self.add_button: Button = Button(self.root, text="Add Task",
                                         width=10,
                                         command=self.add_task)
        self.add_button.place(relx=0.82, rely=0.21, anchor="center")

        self.mark_button: Button = Button(self.root, text="Complete",
                                          width=10,
                                          command=self.mark_as_complete)
        self.mark_button.place(relx=0.82, rely=0.31, anchor="center")

        self.progress_button: Button = Button(self.root, text="In Progress",
                                              width=10,
                                              command=self.mark_as_in_progress)
        self.progress_button.place(relx=0.82, rely=0.41, anchor="center")

        self.delete_button: Button = Button(self.root, text="Delete Task",
                                            width=10,
                                            command=self.delete_item)
        self.delete_button.place(relx=0.82, rely=0.51, anchor="center")

        self.reset_task: Button = Button(self.root, text="Reset Task",
                                         width=10,
                                         command=self.reset_item)
        self.reset_task.place(relx=0.82, rely=0.61, anchor="center")

        self.deselect_button: Button = Button(self.root, text="Deselect",
                                              width=10,
                                              command=self.deselect_item)
        self.deselect_button.place(relx=0.82, rely=0.8, anchor="center")

        self.clear_button: Button = Button(self.root, text="Clear All", 
                                           width=10,
                                           command=self.delete_all_items)
        self.clear_button.place(relx=0.82, rely=0.9, anchor="center")


        self.list_items: dict[str,str] = {}

        self.load_from_file()
        self.update_list()

        self.root.mainloop()


    def save_to_file(self) -> None:
        """
        Store current list items and statuses in the json file.
        """
        with open("to_do_list_data.json", "w") as file:
            json.dump(self.list_items, file)

    
    def load_from_file(self) -> None:
        """
        Load stored list items from the json file.
        """
        try:
            with open("to_do_list_data.json", "r") as file:
                self.list_items = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_to_file()
            

    def deselect_item(self) -> None:
        """
        Deselect all list items.
        """
        self.list.selection_clear(0, END)
        
    
    def update_list(self) -> None:
        """
        Update the ui listbox to match the data in the list dictionary.
        """
        self.list.delete(0, END)

        for idx, item in enumerate(self.list_items.items(), 1):
            self.list.insert(END, f"({idx}) {item[0]}")

            match item[1]:
                case "N":
                    bg = "white"
                case "C":
                    bg = "green"
                case "P":
                    bg = "khaki3"
                    
            self.list.itemconfig(idx-1, {'bg': bg}) # type: ignore


    def add_task(self) -> None:
        """
        Launches pop-up window to add a task to the to-do list.
        """
        if len(self.list_items) >= 16:
            return

        menu: Toplevel = Toplevel()
        menu.geometry("250x100+600+300")
        menu.resizable(False, False)
        menu.title("Add Task")
        menu.grab_set()

        CHAR_LIMIT: int = 31

        def char_count(event):
            # disallows typing in the task entry field after a character
            # limit is reached
            count = len(task_entry.get('1.0', END))
            if count >= CHAR_LIMIT and event.keysym not in \
                {'BackSpace', 'Delete', 'Up', 'Down', 'Left', 'Right'}:
                return 'break'

        task_entry: Text = Text(menu, width=20, height=2, wrap="word")
        task_entry.place(relx=0.5, rely=0.4, anchor="center")

        task_entry.bind('<KeyPress>', char_count)
        task_entry.bind('<KeyRelease>', char_count)

        def add() -> None:
            # add to dictionary
            item: str = task_entry.get('1.0', END).strip()
            if item:
                self.list_items[item] = "N"

            # save to json file
            self.save_to_file()
            self.update_list()
        
            menu.destroy()

        add_button: Button = Button(menu, text="Add Task",
                                    command=add)
        add_button.place(relx=0.5, rely=0.8, anchor="center")

    
    def mark_as_complete(self) -> None:
        """
        Mark the selected task as 'Completed'.
        """
        try:
            current_index: int = self.list.curselection()[0]
        except IndexError:
            return
        
        item: str = list(self.list_items.keys())[current_index]

        self.list_items[item] = "C"
        self.list.itemconfig(current_index, {'bg': 'green'})
        self.deselect_item()

        self.save_to_file()

    
    def mark_as_in_progress(self) -> None:
        """
        Mark the selected task as 'in Progress'.
        """
        try: 
            current_index: int = self.list.curselection()[0]
        except IndexError:
            return
        
        item: str = list(self.list_items.keys())[current_index]
        
        self.list_items[item] = "P"
        self.list.itemconfig(current_index, {'bg': 'khaki3'})
        self.deselect_item()

        self.save_to_file()

    
    def reset_item(self) -> None:
        """
        Mark the selected task as 'None'.
        """
        try: 
            current_index: int = self.list.curselection()[0]
        except IndexError:
            return
        
        item: str = list(self.list_items.keys())[current_index]

        self.list_items[item] = "N"
        self.list.itemconfig(current_index, {'bg': 'white'})
        self.deselect_item()

        self.save_to_file()

    
    def delete_item(self) -> None:
        """
        Delete the selected task.
        """
        try: 
            current_index: int = self.list.curselection()[0]
        except IndexError:
            return
        item: str = list(self.list_items.keys())[current_index]
        del self.list_items[item]

        self.update_list()
        self.save_to_file()

    
    def delete_all_items(self) -> None:
        """
        Launch a pop-up window to delete all tasks in the list.
        """
        menu: Toplevel = Toplevel()
        menu.geometry("200x100+600+300")
        menu.resizable(False, False)
        menu.title("Add Task")
        menu.grab_set()

        menu_bg: str = "#ddd"
        menu.config(background=menu_bg)

        warning: Label = Label(menu, text="Delete all\n tasks?",
                               font=(self.FONT, 12),
                               foreground="red",
                               background=menu_bg)
        warning.place(relx=0.5, rely=0.3, anchor="center")

        def delete() -> None:
            # delete all the items, reset the dictionary
            # and update the json file
            self.list_items = {}
            self.save_to_file()
            self.update_list()
            menu.destroy()

        def cancel() -> None:
            menu.destroy()

        delete_button: Button = Button(menu, text="Delete",
                                       font=(self.FONT, 8),
                                       command=delete)
        delete_button.place(relx=0.3, rely=0.75, anchor="center")

        cancel_button: Button = Button(menu, text="Cancel",
                                       font=(self.FONT, 8),
                                       command=cancel)
        cancel_button.place(relx=0.7, rely=0.75, anchor="center")


if __name__ == "__main__":
    ToDo()