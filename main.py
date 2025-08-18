import tkinter as tk
from tkinter import messagebox, Listbox
import json
import os

class FoxNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("FoxNotes")
        self.root.geometry("800x600")

        self.notes = {}
        self.current_file = None

        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar_frame = tk.Frame(main_frame, width=200, bg='lightgrey')
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        # Buttons frame
        buttons_frame = tk.Frame(sidebar_frame, bg='lightgrey')
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.new_button = tk.Button(buttons_frame, text="New Note", command=self.new_note)
        self.new_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(buttons_frame, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Notes listbox
        self.notes_listbox = Listbox(sidebar_frame, exportselection=False)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)


        # Note content frame
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.text_area = tk.Text(content_frame, wrap=tk.WORD)
        self.text_area.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Note", command=self.save_note)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def on_note_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            title = event.widget.get(index)
            self.load_note_content(title)

    def new_note(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.notes_listbox.selection_clear(0, tk.END)


    def delete_note(self):
        if not self.current_file:
            messagebox.showwarning("No Note Selected", "Please select a note to delete.")
            return

        if messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{self.current_file}'?"):
            del self.notes[self.current_file]
            self.current_file = None
            self.text_area.delete(1.0, tk.END)
            self.update_notes_list()
            self.save_notes_to_file()


    def save_note(self):
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Empty Note", "Cannot save an empty note.")
            return

        if self.current_file and self.current_file in self.notes:
            self.notes[self.current_file] = content
            title = self.current_file
        else:
            title = content.split('\n')[0][:30]
            if not title:
                title = "Untitled"
            i = 1
            base_title = title
            while title in self.notes:
                title = f"{base_title} ({i})"
                i += 1

            self.notes[title] = content
            self.current_file = title

        self.update_notes_list()
        self.save_notes_to_file()
        # select the saved note in listbox
        for i, item in enumerate(self.notes_listbox.get(0, tk.END)):
            if item == title:
                self.notes_listbox.selection_set(i)
                break


    def load_notes(self):
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as f:
                self.notes = json.load(f)
            self.update_notes_list()

    def save_notes_to_file(self):
        with open("notes.json", "w") as f:
            json.dump(self.notes, f, indent=4)

    def update_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for title in self.notes:
            self.notes_listbox.insert(tk.END, title)

    def load_note_content(self, title):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.notes[title])
        self.current_file = title

if __name__ == "__main__":
    root = tk.Tk()
    app = FoxNotes(root)
    root.mainloop()
