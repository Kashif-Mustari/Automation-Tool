#!/usr/bin/env python3

import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


DEFAULT_SOURCE_FOLDER = str(Path.home() / "Downloads")

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".cpp", ".c", ".java", ".ino", ".js", ".html", ".css", ".json"],
    "Apps": [".exe", ".msi", ".appimage", ".deb"],
}


def get_folder_for_file(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder
    return "Others"


def get_unique_destination(file_path, destination_folder):
    filename = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, filename)

    counter = 1
    while os.path.exists(destination_path):
        name, ext = os.path.splitext(filename)
        new_name = f"{name}_{counter}{ext}"
        destination_path = os.path.join(destination_folder, new_name)
        counter += 1

    return destination_path


def move_file(file_path, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    destination_path = get_unique_destination(file_path, destination_folder)
    shutil.move(file_path, destination_path)
    return destination_path


def organize_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise FileNotFoundError("Selected folder does not exist.")

    moved_files = []
    errors = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if not os.path.isfile(item_path) or item.startswith("."):
            continue

        target_folder = get_folder_for_file(item)
        destination_folder = os.path.join(folder_path, target_folder)

        try:
            destination_path = move_file(item_path, destination_folder)
            moved_files.append((item, target_folder, os.path.basename(destination_path)))
        except OSError as error:
            errors.append((item, str(error)))

    return moved_files, errors


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("One Click File Organizer")
        self.root.geometry("720x480")
        self.root.minsize(620, 420)

        self.folder_var = tk.StringVar(value=DEFAULT_SOURCE_FOLDER)
        self.status_var = tk.StringVar(value="Ready")

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f7f8fb")
        style.configure("Header.TLabel", background="#f7f8fb", foreground="#1f2937", font=("Arial", 22, "bold"))
        style.configure("Body.TLabel", background="#f7f8fb", foreground="#4b5563", font=("Arial", 11))
        style.configure("Status.TLabel", background="#eef2ff", foreground="#3730a3", font=("Arial", 10, "bold"))
        style.configure("Primary.TButton", font=("Arial", 12, "bold"), padding=(16, 10))
        style.configure("Secondary.TButton", font=("Arial", 10), padding=(10, 7))

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="File Organizer", style="Header.TLabel")
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main_frame,
            text="Choose a folder, then organize files into Images, Documents, Videos, Music, Code, Apps and more.",
            style="Body.TLabel",
            wraplength=640,
        )
        subtitle.pack(anchor="w", pady=(6, 22))

        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill="x")

        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, font=("Arial", 11))
        folder_entry.pack(side="left", fill="x", expand=True, ipady=7)

        browse_button = ttk.Button(
            folder_frame,
            text="Browse",
            style="Secondary.TButton",
            command=self.choose_folder,
        )
        browse_button.pack(side="left", padx=(10, 0))

        organize_button = ttk.Button(
            main_frame,
            text="Organize Now",
            style="Primary.TButton",
            command=self.organize_selected_folder,
        )
        organize_button.pack(anchor="w", pady=(20, 18))

        status_label = ttk.Label(main_frame, textvariable=self.status_var, style="Status.TLabel", padding=10)
        status_label.pack(fill="x", pady=(0, 14))

        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill="both", expand=True)

        self.log_box = tk.Text(
            log_frame,
            height=12,
            wrap="word",
            bg="#ffffff",
            fg="#111827",
            font=("Consolas", 10),
            relief="solid",
            borderwidth=1,
        )
        self.log_box.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_box.configure(yscrollcommand=scrollbar.set)

        self.write_log("Select a folder and click Organize Now.")

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or DEFAULT_SOURCE_FOLDER)
        if folder:
            self.folder_var.set(folder)
            self.status_var.set("Folder selected")
            self.write_log(f"Selected: {folder}")

    def organize_selected_folder(self):
        folder = self.folder_var.get().strip()
        self.log_box.delete("1.0", "end")
        self.status_var.set("Organizing...")
        self.root.update_idletasks()

        try:
            moved_files, errors = organize_folder(folder)
        except (FileNotFoundError, PermissionError, OSError) as error:
            self.status_var.set("Could not organize folder")
            messagebox.showerror("Error", str(error))
            self.write_log(f"Error: {error}")
            return

        for original_name, target_folder, final_name in moved_files:
            if original_name == final_name:
                self.write_log(f"Moved: {original_name} -> {target_folder}")
            else:
                self.write_log(f"Moved: {original_name} -> {target_folder}/{final_name}")

        for filename, error in errors:
            self.write_log(f"Failed: {filename} ({error})")

        if moved_files:
            self.status_var.set(f"Done. Organized {len(moved_files)} file(s).")
            messagebox.showinfo("Complete", f"Organized {len(moved_files)} file(s).")
        else:
            self.status_var.set("No files to organize.")
            self.write_log("No files found in the selected folder.")

        if errors:
            self.write_log(f"\n{len(errors)} file(s) could not be moved.")

    def write_log(self, message):
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
