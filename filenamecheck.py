import os
import csv
import requests
import time  # Added for cache-busting

# Read the root directory from path.txt
with open("path.txt", "r") as path_file:
    root_dir = path_file.read().strip()

# Append the rest of the path
root_dir = os.path.join(root_dir, "SimObjects", "Airplanes")

# Define the URL of the file_list.csv on GitHub with a cache-busting query parameter
github_csv_url = f"https://raw.githubusercontent.com/DeshMindER/mtlfilecheck/main/file_list.csv?t={int(time.time())}"

# Download the CSV file from GitHub
response = requests.get(github_csv_url)
if response.status_code == 200:
    csv_content = response.text
    # Parse the CSV content as before
    reader = csv.reader(csv_content.splitlines())
    file_list = {}
    for row in reader:
        subfolder = row[0]
        expected_filenames = row[1:]
        file_list[subfolder] = expected_filenames
else:
    print("Failed to fetch file_list.csv from GitHub.")

# Define global exclusion file types
global_exclusion_file_types = [".ini", ".json", ".liv", ".cfg"]

# Open filenamereport.txt for writing
with open("filenamereport.txt", "w") as f:

    # Loop through each subfolder and check for incorrect filenames
    for subfolder, expected_filenames in file_list.items():
        texture_dir = os.path.join(root_dir, subfolder)
        for filename in os.listdir(texture_dir):
            if os.path.isdir(os.path.join(texture_dir, filename)) and filename.lower().startswith("texture") and not filename.lower().endswith(".base"):
                texture_subdir = os.path.join(texture_dir, filename)
                for filename in os.listdir(texture_subdir):
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext in global_exclusion_file_types or filename.lower() == "texture.cfg" or filename.lower() == "light.png.dds" or filename.lower().endswith("_l.png.dds") or filename.lower().endswith("_l.dds"):
                        continue  # skip this filename if its file type is in the global exclusion list, or if it's "texture.cfg", "light.png.dds", ends in "_l.png.dds", or ends in "_l.dds"
                    if filename.lower() not in [name.lower() for name in expected_filenames]:
                        error_msg = f"Incorrect filename found in {texture_subdir}: {filename}\n"
                        f.write(error_msg)
                        print(error_msg)
