import json


with open("salaries.json", "r") as f:
    salaries = json.load(f)

tmp_dict = {}

for employe in salaries["salaries-monthly"].keys():
    tmp_dict[employe] = {}

print(tmp_dict)

with open("tmp.json", "w") as f:
    json.dump(tmp_dict, f, indent=4)
