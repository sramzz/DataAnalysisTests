import os
import shutil

# Define the source and destination paths
src_path = "G:\\My Drive\\FDB\\TPZ PT\\ContentErrorsPT\\CSVFilesPT"
dest_path = "G:\\My Drive\\FDB\\TPZ PT\\ContentErrorsPT\\CSVFilesPT\\promotions2"

# Ensure the destination directory exists
os.makedirs(dest_path, exist_ok=True)

# List all files in the source path
all_files = os.listdir(src_path)

# Loop through each file in the source path
for file_name in all_files:
    # Check if "ErrorPromotionsPT" is in the file name
    if "ErrorPromotionsPT" in file_name:
        # Construct full file paths
        full_file_path = os.path.join(src_path, file_name)
        dest_file_path = os.path.join(dest_path, file_name)
        
        # Copy the file to the destination path
        shutil.copy2(full_file_path, dest_file_path)
