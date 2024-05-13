import os
import shutil
import subprocess

def locate_pen_drives():
    """Locate all connected pen drives."""
    pen_drives = []
    volumes = [os.path.join("/Volumes", d) for d in os.listdir("/Volumes") if not d.startswith(".")]
    for volume in volumes:
        if os.path.ismount(volume):
            pen_drives.append(volume)
    return pen_drives

def create_backup_folders(drive):
    """Create 'fyql' backup folder on the specified drive."""
    backup_folder = os.path.join(drive, "fyql")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    return backup_folder

def move_files_to_pen_drive(pen_drive, file_sequence):
    """Move files from top level of pen drive to the 'fyql' folder."""
    moved_files = []
    backup_folder = create_backup_folders(pen_drive)
    for filename in file_sequence:
        source_file = os.path.join(pen_drive, filename)
        if os.path.isfile(source_file):
            destination_file = os.path.join(backup_folder, os.path.basename(filename))
            shutil.move(source_file, destination_file)
            moved_files.append(filename)
            print(f"Moved '{filename}' to '{backup_folder}'")
    
    # Check if the backup folder is empty
    if not os.listdir(backup_folder):
        print("Stupid" * 3)
        exit()
    
    return moved_files

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
    
    pen_drives = locate_pen_drives()
    if len(pen_drives) == 0:
        print("No pen drives found.")
    else:
        print("Pen drives found:")
        for i, drive in enumerate(pen_drives, 1):
            print(f"{i}. {drive}")
            moved_files = move_files_to_pen_drive(drive, file_sequence)
            print("Files moved successfully to the 'fyql' folder.")
            print("Files moved:")
            for filename in moved_files:
                print(filename)
            eject_pen_drive(drive)
