import json 

with open('peraturan2.json') as f:
    json_data = json.load(f)
    data_list = json_data

json_data = sorted(data_list, key=lambda e: e['peraturanType'])

with open('newfile.json') as f:
    json.dump(json_data) 

