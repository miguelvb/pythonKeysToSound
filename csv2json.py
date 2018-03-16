import csv
import json

file_ = "alumnos.csv"
fjson = "alumnos.json"
data = []
with open(file_) as f:
    for row in csv.DictReader(f):
        data.append(row)
        json_data = json.dumps(data)
       #print(data)

with open(fjson, 'w') as outfile:
    json.dump(json_data, outfile)
