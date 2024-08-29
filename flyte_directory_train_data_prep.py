import os
import pickle

from flytekit.types.directory import FlyteDirectory

# Read the data directory path from the named input
named_input = "data_path"
input_path = f"/workflow/inputs/{named_input}"
with open(input_path, "r") as file:
    data_dir = file.read()

# Ensure the directory path is valid and exists
if not os.path.isdir(data_dir):
    raise ValueError(f"Provided data directory does not exist: {data_dir}")

print(f"Data directory: {data_dir}")

# Create a FlyteDirectory for the data directory and serialize it as a named output
named_output = "data_dir"
output_path = f"/workflow/outputs/{named_output}"
with open(output_path, "wb") as file:
    pickle.dump(FlyteDirectory(data_dir), file)
    print(f"Serialized FlyteDirectory to {output_path}")
