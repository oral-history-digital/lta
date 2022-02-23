import json

filename = 'new-ids.txt'

with open(filename) as f:
    content = f.readlines()

ids = []

for line in content:
    ids_for_line = line.split()
    ids += ids_for_line

ids.sort()

json_string = json.dumps(ids, sort_keys=True, indent=4)

print(json_string)

with open('new-interview-ids.json', 'w') as f:
    f.write(json_string)
