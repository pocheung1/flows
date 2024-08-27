print("Job begins")

print("Writing to /workflow/inputs/model")

with open("/workflow/inputs/model", "w") as file:
    print("This is the content of the workflow input.", file=file)

print("Job ends")
