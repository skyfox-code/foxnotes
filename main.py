import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os

class FoxNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("FoxNotes")
        self.root.geometry("800x600")

        self.notes = {}
        self.current_file = None
        self._save_job = None

        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar_frame = ttk.Frame(main_frame, width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT, padx=(0, 5))

        # Buttons frame
        buttons_frame = ttk.Frame(sidebar_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.new_button = ttk.Button(buttons_frame, text="New Note", command=self.new_note, bootstyle="success")
        self.new_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.delete_button = ttk.Button(buttons_frame, text="Delete Note", command=self.delete_note, bootstyle="danger")
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Notes listbox
        self.notes_listbox = tk.Listbox(sidebar_frame, exportselection=False)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)


        # Note content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.text_area = tk.Text(content_frame, wrap=tk.WORD, relief=tk.FLAT)
        self.text_area.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)
        self.text_area.bind('<KeyRelease>', self.schedule_save)

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

    def schedule_save(self, event=None):
        if self._save_job:
            self.root.after_cancel(self._save_job)
        self._save_job = self.root.after(1000, self.save_note)

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
    root = ttk.Window(themename="darkly")
    app = FoxNotes(root)
    root.mainloop()