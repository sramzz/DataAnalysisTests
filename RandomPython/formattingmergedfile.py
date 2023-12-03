import pandas as pd

# Load the data
file_path = "G:\\My Drive\\FDB\\TPZ PT\\ContentErrorsPT\\CSVFilesPT\\promotions2\\20231102_merged_file.csv"  # Replace with your actual path
data = pd.read_csv(file_path)

# 1. Remove rows with 0 in specified columns
filter_cols = ['StoreWebcode', 'StoreName', 'PromoWebcode', 'PromoName', 'PromoCode', 'BodyAnonymized']
data = data[~(data[filter_cols] == 0).any(axis=1)]

# 2. Format TimeStamp
# data['TimeStamp'] = pd.to_datetime(data['TimeStamp']).dt.strftime('2023-09-13T%H:%M:%S.%f')
data['TimeStamp'] = pd.to_datetime(data['TimeStamp']).dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

# 3. Sort by TimeStamp
data = data.sort_values(by='TimeStamp')

# 3.5 add Date column

# Manually convert to datetime if automatic conversion fails
data['Date'] = pd.to_datetime(data['TimeStamp'], errors='coerce', format='%Y-%m-%d')

# 4. Output to CSV
output_path = "G:\\My Drive\\FDB\\TPZ PT\\ContentErrorsPT\\CSVFilesPT\\promotions2\\20231102_sorted_file.csv"  # Replace with your desired output path
data.to_csv(output_path, index=False)
