import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os

STORAGE_DIR = "storage"

class FoxNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("FoxNotes")
        self.root.geometry("800x600")

        self.current_file = None
        self._save_job = None

        # Ensure storage directory exists
        os.makedirs(STORAGE_DIR, exist_ok=True)

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


    def load_notes(self):
        self.update_notes_list()

    def update_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for filename in os.listdir(STORAGE_DIR):
            if filename.endswith((".md", ".txt")):
                self.notes_listbox.insert(tk.END, filename)

    def load_note_content(self, filename):
        file_path = os.path.join(STORAGE_DIR, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.current_file = file_path
        except IOError as e:
            messagebox.showerror("Load Error", f"Could not load note: {e}")

    def delete_note(self):
        if not self.current_file:
            messagebox.showwarning("No Note Selected", "Please select a note to delete.")
            return

        filename = os.path.basename(self.current_file)
        if messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{filename}'?"):
            try:
                os.remove(self.current_file)
                self.current_file = None
                self.text_area.delete(1.0, tk.END)
                self.update_notes_list()
            except OSError as e:
                messagebox.showerror("Delete Error", f"Could not delete note: {e}")


    def save_note(self):
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            return

        if self.current_file:
            file_path = self.current_file
        else:
            # Generate a filename based on the first line of content
            first_line = content.split('\n')[0][:50].strip()
            if not first_line:
                first_line = "Untitled"

            base_filename = "".join(c for c in first_line if c.isalnum() or c in (' ', '-', '_')).strip()
            if not base_filename:
                base_filename = "Untitled"

            filename = f"{base_filename}.md"
            file_path = os.path.join(STORAGE_DIR, filename)

            i = 1
            while os.path.exists(file_path):
                filename = f"{base_filename} ({i}).md"
                file_path = os.path.join(STORAGE_DIR, filename)
                i += 1

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.current_file = file_path
            self.update_notes_list()
            # Select the saved note in listbox
            filename_only = os.path.basename(file_path)
            for i, item in enumerate(self.notes_listbox.get(0, tk.END)):
                if item == filename_only:
                    self.notes_listbox.selection_set(i)
                    self.notes_listbox.see(i) # Ensure the selected item is visible
                    break
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save note: {e}")

    def load_notes(self):
        self.update_notes_list()

    def update_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for filename in os.listdir(STORAGE_DIR):
            if filename.endswith((".md", ".txt")):
                self.notes_listbox.insert(tk.END, filename)

    def load_note_content(self, filename):
        file_path = os.path.join(STORAGE_DIR, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.current_file = file_path
        except IOError as e:
            messagebox.showerror("Load Error", f"Could not load note: {e}")

    def delete_note(self):
        if not self.current_file:
            messagebox.showwarning("No Note Selected", "Please select a note to delete.")
            return

        filename = os.path.basename(self.current_file)
        if messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{filename}'?"):
            try:
                os.remove(self.current_file)
                self.current_file = None
                self.text_area.delete(1.0, tk.END)
                self.update_notes_list()
            except OSError as e:
                messagebox.showerror("Delete Error", f"Could not delete note: {e}")


    

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = FoxNotes(root)
    root.mainloop()