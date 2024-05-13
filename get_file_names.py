import os
import json

def get_files_from_directory(directory_path):
    """Get a list of file names from the specified directory."""
    files = []
    if os.path.exists(directory_path):
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return files

if __name__ == "__main__":
    directory_path = input("Enter the path of the directory to check for files: ")
    files = get_files_from_directory(directory_path)
    # Encode the file names to UTF-8 to handle non-ASCII characters properly
    files_list = [f.encode('utf-8').decode('utf-8') for f in files]
    # Ensure non-ASCII characters are handled properly when printing JSON
    json_data = json.dumps(files_list, indent=4, ensure_ascii=False)
    print(json_data)
