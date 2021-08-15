import json

with open("json_files/particles.json", "r") as f:
    data = f.read()

data = json.loads(data)

