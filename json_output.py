import json

print("Job begins")

data = {
    "key1": 1,
    "key2": "foo",
}

with open("/workflow/outputs/model", "w") as output:
    json.dump(data, output, indent=4)

print("Job ends")
