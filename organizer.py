import os
import shutil

# 👉 Folder path change here
SOURCE_FOLDER = "/home/mr-max/Downloads"

# File type mapping
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".html"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".cpp", ".c", ".java", ".ino", ".js", ".html", ".css"],
    "Apps": [".exe", ".msi", ".AppImage"],
}


def get_folder_for_file(filename):
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder
    return "Others"


def move_file(file_path, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)

    filename = os.path.basename(file_path)
    dest_path = os.path.join(destination_folder, filename)

    # Handle duplicate names
    counter = 1
    while os.path.exists(dest_path):
        name, ext = os.path.splitext(filename)
        new_name = f"{name}_{counter}{ext}"
        dest_path = os.path.join(destination_folder, new_name)
        counter += 1

    shutil.move(file_path, dest_path)


def organize_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            target_folder = get_folder_for_file(item)
            destination = os.path.join(folder_path, target_folder)

            move_file(item_path, destination)
            print(f"Moved: {item} → {target_folder}")


if __name__ == "__main__":
    organize_folder(SOURCE_FOLDER)
    print("\n✅ Organization complete!")
