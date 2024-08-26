print("Job begins")

with open("/workflow/outputs/model", "w") as output:
    print("This is the content of the workflow output.", file=output)

print("Job ends")
