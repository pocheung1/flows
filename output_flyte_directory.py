import os
import pickle

from flytekit.types.directory import FlyteDirectory

# Create the directory
files_path = "/workflow/outputs/files"
os.makedirs(files_path, exist_ok=True)

# Create file1
file1_path = f"{files_path}/file1"
with open(file1_path, "w") as file1:
    print("This is file1", file=file1)

# Create file2
file2_path = f"{files_path}/file2"
with open(file2_path, "w") as file2:
    print("This is file2", file=file2)

# Create a FlyteDirectory for the files directory and serialize it as a named output
named_output = "output_path"
named_output_path = f"/workflow/outputs/{named_output}"
with open(named_output_path, "w") as output:
    # print(files_path, file=output)
    pickle.dump(FlyteDirectory(files_path), output)
    print(f"Serialized FlyteDirectory to {named_output_path}")
