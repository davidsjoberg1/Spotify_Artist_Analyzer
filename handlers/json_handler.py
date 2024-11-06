import json
import os

def get_json(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            file_data = json.load(file)
            return file_data
    return None

def write_json(key, value, filename):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data[key] = value
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except Exception as e:
        print("Error: ", e)
        pass




def delete_json(key, filename):

    with open(filename, 'r+') as file:
        file_data = json.load(file)
        if key in file_data:
            del file_data[key]
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)
