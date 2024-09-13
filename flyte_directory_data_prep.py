import os
import pickle

import pandas as pd
from flytekit.types.directory import FlyteDirectory

# Read the data directory path from the named input
named_input = "data_path"
input_path = f"/workflow/inputs/{named_input}"
with open(input_path, "r") as file:
    csv_data_path = file.read().strip()

print(f"Data directory: {csv_data_path}")
df = pd.read_csv(csv_data_path)
print(df)

csv_files_dir = f"/tmp/csv_files"
os.makedirs(csv_files_dir, exist_ok=True)

# Write each column (a, b, c) to separate CSV files
df[['a']].to_csv(os.path.join(csv_files_dir, 'a.csv'), index=False, header=True)
df[['b']].to_csv(os.path.join(csv_files_dir, 'b.csv'), index=False, header=True)
df[['c']].to_csv(os.path.join(csv_files_dir, 'c.csv'), index=False, header=True)

# Create a FlyteDirectory for the CSV files directory and serialize it as a named output
named_output = "csv_files_dir"
output_path = f"/workflow/outputs/{named_output}"
with open(output_path, "wb") as file:
    flyte_directory = FlyteDirectory(csv_files_dir)
    pickle.dump(flyte_directory, file)
    print(f"Serialized FlyteDirectory to {output_path}")
