import os
import shutil
import zipfile
import argparse

def extract_and_clean(source_folder, destination_folder, exclude_extension):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".zip"):
            zip_path = os.path.join(source_folder, filename)
            extract_folder = os.path.join(destination_folder, os.path.splitext(filename)[0])  # Remove .zip extension

            # Ensure extraction folder exists
            os.makedirs(extract_folder, exist_ok=True)
            
            print(f"Processing {zip_path}" )
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

            print(f"Extracted {filename} to {extract_folder}")

            # Move files with the specified extension to the root of the extraction folder and delete everything else
            for root, dirs, files in os.walk(extract_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith(exclude_extension):
                        shutil.move(file_path, os.path.join(extract_folder, file))
                        # print(f"Moved {file_path} to {extract_folder}")
                    else:
                        os.remove(file_path)
                        # print(f"Deleted {file_path}")

            # Remove empty directories
            for root, dirs, files in os.walk(extract_folder, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        # print(f"Removed empty directory {dir_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract ZIP files and clean up files based on extension.')
    parser.add_argument('--source_folder', type=str, required=True, help='Path to the source folder containing ZIP files')
    parser.add_argument('--destination_folder', type=str, required=True, help='Path to the destination folder for extracted files')
    parser.add_argument('--exclude_extension', type=str, required=True, help='File extension to exclude from deletion (e.g., .java)')
    args = parser.parse_args()

    extract_and_clean(args.source_folder, args.destination_folder, args.exclude_extension)