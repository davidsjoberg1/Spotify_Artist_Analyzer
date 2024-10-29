import json
import os

def get_json(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            file_data = json.load(file)
            return file_data
    return None

def write_json(data, filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r+') as file:
            file_data = json.load(file)

            for artist in file_data["artists"]:
                if artist["id"] == data["id"]:
                    return
            file_data["artists"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    else:
        with open(filename, 'w') as file:
            file_data = {"artists": [data]}
            json.dump(file_data, file, indent=4)


def delete_json(data, filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r+') as file:
            file_data = json.load(file)

            file_data["artists"] = [artist for artist in file_data["artists"] if artist["id"] != data["id"]]
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=4)