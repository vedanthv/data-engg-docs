import json

with open("test.json", "r") as f:
    data = json.load(f)

for key, value in data.items():
    if isinstance(value, list):
        print(f"{key}: {len(value)} records")
    else:
        print(f"{key}: not a list (skipped)")
