import os
import subprocess

import pandas as pd


def list_directory(directory):
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return
    try:
        result = subprocess.run(['ls', '-l', directory], capture_output=True, text=True, check=True)
        print(f"$ ls -l {directory}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


# Debug: list contents of workflow inputs
workflow_inputs = "/workflow/inputs"
list_directory(workflow_inputs)

# Deserialize the named input to a FlyteDirectory
named_input = "csv_files_path"
named_input_path = f"{workflow_inputs}/{named_input}"
with open(named_input_path, "r") as file:
    csv_files_path = file.read().strip()

print(f"CSV files path: {csv_files_path}")

if not os.path.exists(csv_files_path):
    raise ValueError(f"CSV files path does not exist: {csv_files_path}")

list_directory(csv_files_path)

# Read CSV files
df_a = pd.read_csv(f"{csv_files_path}/a.csv")
df_b = pd.read_csv(f"{csv_files_path}/b.csv")
df_c = pd.read_csv(f"{csv_files_path}/c.csv")

# Sum the values in each row across each column in the CSV files
df_sum = pd.DataFrame()
df_sum['sum'] = df_a['a'] + df_b['b'] + df_c['c']

# Write a CSV file as the named output
named_output = "sum"
named_output_path = f"/workflow/outputs/{named_output}"
df_sum.to_csv(named_output_path, index=False)
print(f"Wrote CSV file to {named_output_path}")