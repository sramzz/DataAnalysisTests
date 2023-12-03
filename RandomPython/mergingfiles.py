import os
import pandas as pd

# Path where the CSV files are stored
src_path = "G:\\My Drive\\FDB\\TPZ PT\\ContentErrorsPT\\CSVFilesPT\\promotions2"

# Get a list of all CSV files in the source directory
all_files = [f for f in os.listdir(src_path) if f.endswith('.csv')]

# Initialize an empty DataFrame to hold the merged data
merged_data = pd.DataFrame()

# Loop through each file, read its contents into a DataFrame, and append it to merged_data
for file_name in all_files:
    file_path = os.path.join(src_path, file_name)
    data = pd.read_csv(file_path)
    merged_data = merged_data.append(data, ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv(os.path.join(src_path, "20231102_merged_file.csv"), index=False)
