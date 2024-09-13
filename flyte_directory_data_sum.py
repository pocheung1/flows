import pickle
import subprocess

import pandas as pd


def list_directory(directory):
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
named_input = "data_dir"
input_path = f"{workflow_inputs}/{named_input}"
with open(input_path, "rb") as file:
    flyte_dir = pickle.load(file)

# Debug: list contents of data directory
data_path = flyte_dir.path
list_directory(data_path)

# Read CSV files
df_a = pd.read_csv(f"{data_path}/a.csv")
df_b = pd.read_csv(f"{data_path}/b.csv")
df_c = pd.read_csv(f"{data_path}/c.csv")

# Sum the values in each row across each column in the CSV files
df_sum = pd.DataFrame()
df_sum['sum'] = df_a['a'] + df_b['b'] + df_c['c']

# Write a CSV file as the named output
named_output = "sum"
output_path = f"/workflow/outputs/{named_output}"
df_sum.to_csv(output_path, index=False)
print(f"Wrote CSV file to {output_path}")