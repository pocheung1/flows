print("Job begins")

with open("/workflow/outputs/model", "w") as output:
    print("This is the model output", file=output)

print("Job ends")
