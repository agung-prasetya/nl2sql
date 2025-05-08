import json
import os

paths = ['akademik_1.json']
# base_dir = os.path.dirname(os.path.abspath(__file__))
# full_db_path = os.path.abspath(base_dir)
full_db_path = os.path.abspath("e:/codes/nl2sql/databases/sorting_detector/")

for path in paths:
    file_database_json = os.path.join(full_db_path, path)

    with open(file_database_json,'r') as file:
        data = json.load(file)
        
    entitas_attributes = {}
    for entity in data['entities']:
        attribute_name_type = {}
        for atribut in entity['attributes']:
            attribute_name_type[atribut.lower()] = "" 
        entitas_attributes[entity['name'].lower()] = attribute_name_type
    
    new_data = {'entitas':entitas_attributes}
    
    with open(file_database_json, 'w') as file:
        json.dump(new_data, file, indent=4)
            