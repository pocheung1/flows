import os

import pandas as pd

# Read the data directory path from the named input
named_input = "data_path"
named_input_path = f"/workflow/inputs/{named_input}"
with open(named_input_path, "r") as file:
    csv_data_path = file.read().strip()

print(f"Data path: {csv_data_path}")
df = pd.read_csv(csv_data_path)
print(df)

csv_files_path = f"/workflow/outputs/csv_files"
os.makedirs(csv_files_path, exist_ok=True)

# Write each column (a, b, c) to separate CSV files
df[['a']].to_csv(os.path.join(csv_files_path, 'a.csv'), index=False, header=True)
df[['b']].to_csv(os.path.join(csv_files_path, 'b.csv'), index=False, header=True)
df[['c']].to_csv(os.path.join(csv_files_path, 'c.csv'), index=False, header=True)

named_output = "csv_files_path"
named_output_path = f"/workflow/outputs/{named_output}"
with open(named_output_path, "w") as file:
    print(csv_files_path, file=file)

print(f"Wrote '{csv_files_path}' to named output at {named_output_path}")
