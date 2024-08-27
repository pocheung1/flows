import os

print("Job begins")

# Create the directory
os.makedirs("/workflow/inputs/model", exist_ok=True)

# Create and write to file1
print("Writing to /workflow/inputs/model/file1")
with open("/workflow/inputs/model/file1", "w") as file1:
    print("This is the content of file1", file=file1)

# Create and write to file2
print("Writing to /workflow/inputs/model/file2")
with open("/workflow/inputs/model/file2", "w") as file2:
    print("This is the content of file2", file=file2)

print("Job ends")
