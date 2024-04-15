print("Job begins")

with open("/workflow/outputs/model", "w") as model:
    print("This is the model output", file=model)

print("Job ends")
