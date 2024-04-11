import os
import csv
from tqdm import tqdm

def convert_bytes_to_gigabytes(bytes_size):
    """
    Convert bytes to gigabytes (GB).
    """
    return bytes_size / (1024 * 1024 * 1024)

def crawl_directory(directory_path, csv_writer, pbar_dirs, pbar_files):
    """
    Recursively crawl through a directory and its subdirectories
    and write directory path and file size information to a CSV file
    for files larger than 1 GB.
    """
    for root, dirs, files in os.walk(directory_path):
        # Update directory progress bar
        pbar_dirs.update(1)

        # Write information about files in the current directory to CSV
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size_bytes = os.path.getsize(file_path)
            file_size_gb = convert_bytes_to_gigabytes(file_size_bytes)
            if file_size_gb > 1:
                csv_writer.writerow({'Directory': root, 'File': file_name, 'Size (Bytes)': file_size_bytes, 'Size (GB)': file_size_gb})
            # Update file progress bar
            pbar_files.update(1)

        # Recursively crawl through subdirectories
        for dir_name in dirs:
            crawl_directory(os.path.join(root, dir_name), csv_writer, pbar_dirs, pbar_files)

# Define the DFS path to the Windows CIFS share
dfs_path = r"\\your_domain\dfs\path\to\cifs\share"

# Define the CSV file path
csv_file_path = r"C:\cifs_share_info_over_1GB.csv"

# Count the total number of directories and files
total_dirs = sum(len(dirs) for _, dirs, _ in os.walk(dfs_path))
total_files = sum(len(files) for _, _, files in os.walk(dfs_path))

# Initialize tqdm progress bars
pbar_dirs = tqdm(total=total_dirs, desc='Directories', unit='dir')
pbar_files = tqdm(total=total_files, desc='Files', unit='file')

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csv_file:
    # Define CSV fieldnames
    fieldnames = ['Directory', 'File', 'Size (Bytes)', 'Size (GB)']

    # Initialize CSV writer
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write CSV header
    csv_writer.writeheader()

    # Call the crawl_directory function with the DFS path
    crawl_directory(dfs_path, csv_writer, pbar_dirs, pbar_files)

# Close tqdm progress bars
pbar_dirs.close()
pbar_files.close()

print(f"CSV file '{csv_file_path}' has been generated with directory path and file size information for files larger than 1GB.")
