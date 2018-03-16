import os
import json
import csv

dir = './sounds/wav'
fjson = 'files_config.json'
aljson = 'alumnos.json'

file_ = "alumnos.csv"
ajson = "alumnos.json"
data = []

with open(file_) as f:
    for row in csv.DictReader(f):
        data.append(row)

with open(ajson, 'w') as outfile:
    json.dump(data, outfile, indent=2)

alumnos = data

def get_config(s, ismusic):
    if(ismusic):
        idx =  s["music_id"]
    else:
        idx = s["uid"]
    res = [x for x in alumnos if x["uid"] == idx ] 
    
    if(res):
        return res[0]
    else:
        return False

data_dict = []
for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith(".wav"):
            ff = os.path.join(root, file)
            f2 = ff.split("/")
            grp = f2[4]
            name = f2[5]
            grp_idx = grp.split("-")[0]
            name_idx = name.split("-")[0]
            uid =  grp_idx + name_idx
            ismusic = name.split('-')[1] == 'musica'
            if(ismusic):
                uid = uid + "-musica"
            dd = {
                "file": ff, 
                "group": grp, 
                "group_id": grp_idx, 
                "name": name, 
                "name_idx": name_idx, 
                "uid": uid,
                "ismusic": ismusic,
                "music_id": grp_idx + "-musica"
            }
            cf = get_config(dd, ismusic)
            if(cf):
                dd.update(cf)
                data_dict.append(dd)

with open(fjson, 'w') as outfile:
    json.dump(data_dict, outfile, indent=2)
