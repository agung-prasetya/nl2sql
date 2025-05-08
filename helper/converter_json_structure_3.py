import json
import os

paths = ['hotel2.json']
base_dir = os.path.dirname(os.path.abspath(__file__))
full_db_path = os.path.abspath(base_dir)

for path in paths:
    new_data = {'entitas':{}}

    file_database_json = os.path.join(full_db_path, path)

    with open(file_database_json,'r') as file:
        data = json.load(file)
        
    entitas_attributes = {}
    for details in data['entities']:
        attribute_name_type = {}
        for atribut in details['attributes']:
            attribute_name_type[atribut['name'].lower()] = atribut['type'].lower()
        entitas_attributes[details['name'].lower()] = attribute_name_type
    
    new_data = {'entitas':entitas_attributes}
    
    with open(file_database_json, 'w') as file:
        json.dump(new_data, file, indent=4)
            