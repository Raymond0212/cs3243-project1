import json

with open("summary.txt", 'r') as f:
    data = json.loads(f.read())  # data becomes a dictionary
    print(data["n_equals_3/input_2.txt"])