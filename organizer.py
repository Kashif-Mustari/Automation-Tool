#!/usr/bin/env python3

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

ALL_CATEGORIES = list(FILE_TYPES.keys()) + ["Others"]


def get_folder_for_file(filename):
    extension = Path(filename).suffix.lower()

    for folder, extensions in FILE_TYPES.items():
        if extension in extensions:
            return folder
    return "Others"


def is_hidden_path(path):
    return any(part.startswith(".") for part in Path(path).parts)


def get_unique_destination(source_path, destination_folder, dry_run=False):
    destination_folder = Path(destination_folder)
    if not dry_run:
        destination_folder.mkdir(parents=True, exist_ok=True)

    filename = Path(source_path).name
    destination_path = destination_folder / filename
    counter = 1

    while destination_path.exists():
        stem = destination_path.stem
        suffix = destination_path.suffix
        destination_path = destination_folder / f"{stem}_{counter}{suffix}"
        counter += 1

    return destination_path


def organize_folder(source_folder, destination_folder=None, recursive=False, dry_run=False):
    source = Path(source_folder)
    if not source.is_dir():
        raise FileNotFoundError("Selected folder does not exist.")

    destination = Path(destination_folder) if destination_folder else source
    if destination.resolve() != source.resolve() and destination.resolve().is_relative_to(source.resolve()):
        raise ValueError("Destination must not be a subfolder of the source folder.")

    paths = list(source.rglob("*") if recursive else source.iterdir())
    moved_files = []
    errors = []

    for item in paths:
        if item.is_dir():
            continue

        if is_hidden_path(item):
            continue

        if destination.resolve() != source.resolve() and destination.resolve() in item.resolve().parents:
            continue

        if destination.resolve() == source.resolve():
            first_part = item.relative_to(source).parts[0]
            if first_part in ALL_CATEGORIES:
                continue

        category = get_folder_for_file(item.name)
        target_folder = destination / category

        try:
            destination_path = get_unique_destination(item, target_folder, dry_run=dry_run)
            if not dry_run:
                shutil.move(str(item), str(destination_path))
            moved_files.append((str(item), category, destination_path.name))
        except OSError as error:
            errors.append((str(item), str(error)))

    return moved_files, errors


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("One Click File Organizer")
        self.root.geometry("820x560")
        self.root.minsize(720, 500)

        self.folder_var = tk.StringVar(value=DEFAULT_SOURCE_FOLDER)
        self.destination_var = tk.StringVar(value=DEFAULT_SOURCE_FOLDER)
        self.status_var = tk.StringVar(value="Ready")
        self.summary_var = tk.StringVar(value="")
        self.recursive_var = tk.BooleanVar(value=False)
        self.dry_run_var = tk.BooleanVar(value=False)

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f7f8fb")
        style.configure("Header.TLabel", background="#f7f8fb", foreground="#1f2937", font=("Arial", 24, "bold"))
        style.configure("Body.TLabel", background="#f7f8fb", foreground="#4b5563", font=("Arial", 11))
        style.configure("Status.TLabel", background="#eef2ff", foreground="#3730a3", font=("Arial", 10, "bold"))
        style.configure("Primary.TButton", font=("Arial", 12, "bold"), padding=(16, 10))
        style.configure("Secondary.TButton", font=("Arial", 10), padding=(10, 7))
        style.configure("Log.TLabel", background="#ffffff", foreground="#111827", font=("Arial", 11))
        style.configure("TCheckbutton", background="#f7f8fb", font=("Arial", 10))
        style.configure("TProgressbar", thickness=16)

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="File Organizer", style="Header.TLabel")
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main_frame,
            text="Choose a folder and destination, then organize files by category. Enable recursive scan or dry run as needed.",
            style="Body.TLabel",
            wraplength=760,
        )
        subtitle.pack(anchor="w", pady=(6, 20))

        source_frame = ttk.Frame(main_frame)
        source_frame.pack(fill="x", pady=(0, 12))

        source_label = ttk.Label(source_frame, text="Source folder:", style="Body.TLabel")
        source_label.pack(anchor="w", pady=(0, 4))

        source_entry = ttk.Entry(source_frame, textvariable=self.folder_var, font=("Arial", 11))
        source_entry.pack(side="left", fill="x", expand=True, ipady=7)

        browse_source_button = ttk.Button(
            source_frame,
            text="Browse",
            style="Secondary.TButton",
            command=self.choose_folder,
        )
        browse_source_button.pack(side="left", padx=(10, 0))

        destination_frame = ttk.Frame(main_frame)
        destination_frame.pack(fill="x", pady=(0, 18))

        destination_label = ttk.Label(destination_frame, text="Destination folder:", style="Body.TLabel")
        destination_label.pack(anchor="w", pady=(0, 4))

        destination_entry = ttk.Entry(destination_frame, textvariable=self.destination_var, font=("Arial", 11))
        destination_entry.pack(side="left", fill="x", expand=True, ipady=7)

        browse_destination_button = ttk.Button(
            destination_frame,
            text="Browse",
            style="Secondary.TButton",
            command=self.choose_destination,
        )
        browse_destination_button.pack(side="left", padx=(10, 0))

        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill="x", pady=(0, 8))

        recursive_checkbox = ttk.Checkbutton(
            options_frame,
            text="Recursive scan",
            variable=self.recursive_var,
            style="TCheckbutton",
        )
        recursive_checkbox.pack(side="left")

        dry_run_checkbox = ttk.Checkbutton(
            options_frame,
            text="Dry run (no files moved)",
            variable=self.dry_run_var,
            style="TCheckbutton",
        )
        dry_run_checkbox.pack(side="left", padx=(28, 0))

        organize_button = ttk.Button(
            main_frame,
            text="Organize Now",
            style="Primary.TButton",
            command=self.organize_selected_folder,
        )
        organize_button.pack(anchor="w", pady=(8, 18))

        status_label = ttk.Label(main_frame, textvariable=self.status_var, style="Status.TLabel", padding=10)
        status_label.pack(fill="x", pady=(0, 12))

        progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate", variable=tk.DoubleVar(value=0))
        progress.pack(fill="x", pady=(0, 10))
        self.progress_bar = progress

        self.summary_label = ttk.Label(main_frame, textvariable=self.summary_var, style="Body.TLabel")
        self.summary_label.pack(anchor="w", pady=(0, 12))

        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill="both", expand=True)

        self.log_box = tk.Text(
            log_frame,
            height=14,
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
            self.status_var.set("Source folder selected")
            self.write_log(f"Source: {folder}")

    def choose_destination(self):
        folder = filedialog.askdirectory(initialdir=self.destination_var.get() or DEFAULT_SOURCE_FOLDER)
        if folder:
            self.destination_var.set(folder)
            self.status_var.set("Destination folder selected")
            self.write_log(f"Destination: {folder}")

    def organize_selected_folder(self):
        source = self.folder_var.get().strip()
        destination = self.destination_var.get().strip() or source
        recursive = self.recursive_var.get()
        dry_run = self.dry_run_var.get()

        self.log_box.delete("1.0", "end")
        self.status_var.set("Organizing...")
        self.summary_var.set("")
        self.progress_bar['value'] = 0
        self.root.update_idletasks()

        try:
            moved_files, errors = organize_folder(
                source_folder=source,
                destination_folder=destination,
                recursive=recursive,
                dry_run=dry_run,
            )
        except (FileNotFoundError, PermissionError, ValueError, OSError) as error:
            self.status_var.set("Could not organize folder")
            messagebox.showerror("Error", str(error))
            self.write_log(f"Error: {error}")
            return

        total = len(moved_files) + len(errors)
        for index, (original, category, final_name) in enumerate(moved_files, start=1):
            if original.endswith(final_name):
                self.write_log(f"Moved: {Path(original).name} -> {category}")
            else:
                self.write_log(f"Moved: {Path(original).name} -> {category}/{final_name}")
            self.progress_bar['value'] = int(index / max(total, 1) * 100)
            self.root.update_idletasks()

        for index, (filename, error) in enumerate(errors, start=len(moved_files) + 1):
            self.write_log(f"Failed: {Path(filename).name} ({error})")
            self.progress_bar['value'] = int(index / max(total, 1) * 100)
            self.root.update_idletasks()

        summary_parts = []
        if moved_files:
            summary_parts.append(f"Organized {len(moved_files)} file(s)")
        if errors:
            summary_parts.append(f"{len(errors)} failed")

        self.summary_var.set(". ".join(summary_parts))

        if dry_run:
            self.status_var.set("Dry run complete.")
            messagebox.showinfo("Dry Run", f"Found {len(moved_files)} file(s) that would be organized.")
        elif moved_files:
            self.status_var.set(f"Done. Organized {len(moved_files)} file(s).")
            messagebox.showinfo("Complete", f"Organized {len(moved_files)} file(s).")
        else:
            self.status_var.set("No files to organize.")
            self.write_log("No files found for organization.")

        if errors:
            self.write_log(f"\n{len(errors)} file(s) could not be moved.")

    def write_log(self, message):
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
