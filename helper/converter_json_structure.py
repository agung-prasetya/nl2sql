import json
import os

paths = ['inventory1.json','kepegawaian2.json','pemesanan1.json','pemesanan2.json','penjualan1.json','penjualan2.json']
base_dir = os.path.dirname(os.path.abspath(__file__))
full_db_path = os.path.abspath(base_dir)

for path in paths:
    new_data = {'entitas':{}}

    file_database_json = os.path.join(full_db_path, path)

    with open(file_database_json,'r') as file:
        data = json.load(file)
        
    entitas_attributes = {}
    for entitas, details in data['entitas'].items():
        attribute_name_type = {}
        for attribute_name, attribute_type in details['attributes'].items():
            attribute_name_type[attribute_name.lower()]=attribute_type.lower()
        entitas_attributes[entitas.lower()] = attribute_name_type
    
    new_data = {'entitas':entitas_attributes}
    
    with open(file_database_json, 'w') as file:
        json.dump(new_data, file, indent=4)
            