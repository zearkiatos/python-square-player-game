import json

def read_json_file(file_path:str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data