import json

json_string: str = ""
filePath = '../Json_Class/JSONCONFIG1.json'

with open(filePath) as f:
     json_string = json.load(f)
     f.close()

jsonsamplestring = json.dumps(json_string["edge device"]["properties"])
json_dictionary = json.loads(jsonsamplestring)
jsondummy={}
        
for key in json_dictionary:
    json_dict =  { key : json_dictionary[key] }
    jsondummy.update(json_dict)
print(jsondummy)