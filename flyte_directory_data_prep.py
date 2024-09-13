import os

import pandas as pd

# Read the data directory path from the named input
named_input = "data_path"
input_path = f"/workflow/inputs/{named_input}"
with open(input_path, "r") as file:
    csv_data_path = file.read().strip()

print(f"Data path: {csv_data_path}")
df = pd.read_csv(csv_data_path)
print(df)

named_output = "csv_files"
csv_files_dir = f"/workflow/outputs/{named_output}"
os.makedirs(csv_files_dir, exist_ok=True)

# Write each column (a, b, c) to separate CSV files
df[['a']].to_csv(os.path.join(csv_files_dir, 'a.csv'), index=False, header=True)
df[['b']].to_csv(os.path.join(csv_files_dir, 'b.csv'), index=False, header=True)
df[['c']].to_csv(os.path.join(csv_files_dir, 'c.csv'), index=False, header=True)
