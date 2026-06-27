# File Organizer

A simple yet powerful GUI application to automatically organize files into categorized folders with one click.

## Features

✨ **Key Capabilities:**

- 🎯 **One-Click Organization** - Organize entire folders instantly
- 📁 **Automatic Categorization** - Files sorted into 9 categories + Others
- 🔄 **Recursive Scanning** - Option to scan subfolders
- 👁️ **Dry Run Mode** - Preview changes without moving files
- 📊 **Real-Time Progress** - Visual progress bar and detailed logs
- 🔒 **Safe Operations** - Handles duplicate filenames automatically
- 🖱️ **User-Friendly GUI** - Clean, intuitive Tkinter interface

## Supported File Categories

The application organizes files into the following categories:

| Category | Extensions |
|----------|-----------|
| **Images** | .jpg, .jpeg, .png, .gif, .webp, .svg |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt |
| **Spreadsheets** | .xls, .xlsx, .csv |
| **Presentations** | .ppt, .pptx |
| **Videos** | .mp4, .mkv, .avi, .mov, .webm |
| **Music** | .mp3, .wav, .aac, .flac |
| **Archives** | .zip, .rar, .tar, .gz, .7z |
| **Code** | .py, .cpp, .c, .java, .ino, .js, .html, .css, .json |
| **Apps** | .exe, .msi, .appimage, .deb |
| **Others** | All unrecognized file types |

## Requirements

- Python 3.7 or higher
- Tkinter (usually included with Python)
- Linux/Windows/macOS

### Installing Tkinter

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Tkinter is included with Python by default.

## Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd Automation-Tool
   ```

2. **Make the script executable:**
   ```bash
   chmod +x organizer.py
   ```

3. **Run the application:**
   ```bash
   python3 organizer.py
   ```

## Usage

### GUI Interface

1. **Select Source Folder** - Click "Browse" to choose the folder you want to organize
2. **Select Destination Folder** (optional) - Choose where organized files should go
   - If not specified, files will be organized in the source folder
3. **Configure Options:**
   - ✅ **Recursive Scan** - Enable to include files in subfolders
   - ✅ **Dry Run** - Enable to preview changes without moving files
4. **Click "Organize Now"** - Start the organization process
5. **Review Results** - Check the progress bar and log for detailed information

### Example Workflow

```
Downloads/
├── vacation.jpg
├── report.pdf
├── song.mp3
├── project.zip
└── script.py

After organization:
├── Images/
│   └── vacation.jpg
├── Documents/
│   └── report.pdf
├── Music/
│   └── song.mp3
├── Archives/
│   └── project.zip
└── Code/
    └── script.py
```

## Desktop Application (Linux)

You can create a desktop shortcut to launch the application from your application menu:

The project includes `File Organizer.desktop` for easy launching on Linux systems.

To install:
```bash
cp "File Organizer.desktop" ~/.local/share/applications/
```

Then search for "File Organizer" in your application launcher.

## API Usage (Programmatic)

You can also use the organizer in your own Python scripts:

```python
from organizer import organize_folder

# Organize files
moved_files, errors = organize_folder(
    source_folder="/path/to/source",
    destination_folder="/path/to/destination",  # Optional
    recursive=False,
    dry_run=True  # Set to False to actually move files
)

# Process results
for original_path, category, new_filename in moved_files:
    print(f"Moved: {original_path} -> {category}/{new_filename}")

for failed_file, error in errors:
    print(f"Error moving {failed_file}: {error}")
```

## Features Explained

### Dry Run Mode
Preview what will happen without actually moving any files. Perfect for testing your organization rules before committing changes.

### Recursive Scanning
When enabled, the tool will search through all subfolders and organize files found at any depth level.

### Duplicate Handling
If a file already exists in the destination, the application automatically renames it by appending a counter (e.g., `document_1.pdf`, `document_2.pdf`).

### Hidden Files
Hidden files and files in hidden directories (starting with `.`) are automatically skipped.

## Error Handling

The application gracefully handles:
- Files that cannot be accessed (permission denied)
- Destination folders that are subfolders of the source
- Files that already exist in the destination
- Missing or invalid source folders

All errors are logged in the application window for your review.

## Performance

- Handles folders with hundreds of files smoothly
- Progress bar updates in real-time
- Efficient path handling with Python's `pathlib`

## Project Structure

```
Automation-Tool/
├── organizer.py              # Main application
├── File Organizer.desktop    # Linux desktop entry
└── README.md                 # This file
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tkinter not found | Install with `sudo apt-get install python3-tk` |
| Permission denied errors | Ensure you have read/write permissions for the folders |
| Files not moving | Check "Dry Run" is unchecked; use it first to preview |
| Application won't start | Verify Python 3.7+ is installed: `python3 --version` |

## Contributing

Feel free to fork, modify, and improve this project. Suggested enhancements:
- Add custom category configurations
- Support for file renaming patterns
- Undo functionality
- Advanced filtering options

## License

This project is open source and available for personal and commercial use.

## Support

If you encounter issues:
1. Enable "Dry Run" to test without changes
2. Check the log window for detailed error messages
3. Verify folder permissions with `ls -la` command
4. Try running with a smaller test folder first

---

**Enjoy organizing your files! 📁✨**
