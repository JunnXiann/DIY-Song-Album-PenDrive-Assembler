import os
import shutil
import subprocess
import sys

def locate_pen_drives():
    """Locate all connected writable pen drives (excluding system volumes)."""
    excluded = ["Macintosh HD", "Macintosh HD - Data", "Recovery", "com.apple.TimeMachine.localsnapshots"]
    pen_drives = []
    volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if not d.startswith(".")]
    for volume in volumes:
        if os.path.ismount(volume) and os.access(volume, os.W_OK):
            drive_name = os.path.basename(volume)
            if drive_name not in excluded:
                pen_drives.append(volume)
    return pen_drives


def create_fyql_folder(drive):
    """Create 'fyql' folder on the specified drive."""
    fyql_folder = os.path.join(drive, "fyql")
    os.makedirs(fyql_folder, exist_ok=True)
    return fyql_folder

def copy_files_to_pen_drive(source_dir, pen_drive, file_sequence):
    """Copy specified files from source directory to pen drive's 'fyql' folder."""
    fyql_folder = create_fyql_folder(pen_drive)
    copied_files = []

    for filename in file_sequence:
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            destination_path = os.path.join(fyql_folder, os.path.basename(filename))
            shutil.copy2(source_path, destination_path)
            copied_files.append(filename)
            print(f"Copied '{filename}' to '{fyql_folder}'")
        else:
            print(f"[Warning] File not found: {source_path}")

    return copied_files

def eject_pen_drive(drive):
    """Eject the specified pen drive."""
    try:
        subprocess.run(["diskutil", "eject", drive], check=True)
        print(f"Ejected '{drive}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to eject '{drive}': {e}")

if __name__ == "__main__":
    file_sequence = [
        "1 - FYQL 2.0 - 01 灯传.mp3",
        "1 - FYQL 2.0 - 02 Be With You.mp3",
        "1 - FYQL 2.0 - 03 步步.mp3",
        "1 - FYQL 2.0 - 04 拥抱呼吸.mp3",
        "1 - FYQL 2.0 - 05 树想.mp3",
        "1 - FYQL 2.0 - 06 活出喜悦.mp3",
        "1 - FYQL 2.0 - 07 以为没人知道.mp3",
        "1 - FYQL 2.0 - 08 佛法的侍者.mp3",
        "2 - FYQL - 01 水.mp3",
        "2 - FYQL - 02 法音清流.mp3",
        "2 - FYQL - 03 落叶.mp3",
        "2 - FYQL - 04 觉悟.mp3",
        "2 - FYQL - 05 选择.mp3",
        "2 - FYQL - 06 释迦如来.mp3",
        "2 - FYQL - 07 如莲的喜悦.mp3",
        "2 - FYQL - 08 至上的教诲.mp3",
        "2 - FYQL - 09 看海（之一）.mp3",
        "2 - FYQL - 10 承先启后.mp3"
    ]

    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as a normal Python script
        script_dir = os.path.dirname(os.path.abspath(__file__))

    source_dir = os.path.join(script_dir, "FYQL_source")

    if not os.path.isdir(source_dir):
        print(f"'FYQL_source' folder not found at: {source_dir}")
        exit()

    pen_drives = locate_pen_drives()
    if not pen_drives:
        print("No pen drives found.")
        exit()

    print("\nPen drives found:")
    for i, drive in enumerate(pen_drives, 1):
        print(f"{i}. {drive}")

    for drive in pen_drives:
        print(f"\nCopying to {drive}...")
        copied_files = copy_files_to_pen_drive(source_dir, drive, file_sequence)
        print(f"{len(copied_files)} files copied successfully.")
        eject_pen_drive(drive)
