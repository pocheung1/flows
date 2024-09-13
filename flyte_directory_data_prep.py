import os
import pickle
import subprocess

import pandas as pd
from flytekit.types.directory import FlyteDirectory


def list_directory(directory):
    try:
        result = subprocess.run(['ls', '-l', directory], capture_output=True, text=True, check=True)
        print(f"$ ls -l {directory}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


# Read the data directory path from the named input
named_input = "data_path"
input_path = f"/workflow/inputs/{named_input}"
with open(input_path, "r") as file:
    csv_data_path = file.read().strip()

print(f"Data path: {csv_data_path}")
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

flyte_directory = FlyteDirectory.new_remote().new_dir("csv_files")
print(f"Flyte directory: {flyte_directory}")
print(f"Flyte directory path: {flyte_directory.path}")
print(f"Flyte directory remote directory: {flyte_directory.remote_directory}")
print(f"Flyte directory remote source: {flyte_directory.remote_source}")

flyte_file_a = flyte_directory.new_file("a.csv")
# df[['a']].to_csv(flyte_file_a, index=False, header=True)
flyte_file_b = flyte_directory.new_file("b.csv")
# df[['b']].to_csv(flyte_file_b, index=False, header=True)
flyte_file_c = flyte_directory.new_file("c.csv")
# df[['c']].to_csv(flyte_file_c, index=False, header=True)
# list_directory(flyte_directory.path)
FlyteDirectory.listdir(flyte_directory)

with open(output_path, "wb") as file:
    pickle.dump(flyte_directory, file)
    print(f"Serialized FlyteDirectory to {output_path}")
