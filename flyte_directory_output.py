import os

print("Job begins")

# Create the directory
os.makedirs("/workflow/outputs/model", exist_ok=True)

# Create and write to file1
with open("/workflow/outputs/model/file1", "w") as output1:
    print("This is the content of file1", file=output1)

# Create and write to file2
with open("/workflow/outputs/model/file2", "w") as output2:
    print("This is the content of file2", file=output2)

print("Job ends")
