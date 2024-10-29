from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from datetime import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
    

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"][0]
    return json_result



def get_related_artists(token, id):
    url = "https://api.spotify.com/v1/artists/" + str(id) + "/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]
    return json_result



def get_all_artists(token):
    with open("artists.json", 'r') as file:
        file_data = json.load(file)
        all_artists = file_data["all_artists"]
        search_artists = file_data["search_artists"]
    
            
    current_artist = search_artists.pop(0)
    related_artists = get_related_artists(token, current_artist["id"])
    current_artist["related_artists"] = related_artists
   
    while True:
        if len(search_artists) == 0:
            break
        current_artist = search_artists.pop(0)
        related_artists = get_related_artists(token, current_artist["id"])
        current_artist["related_artists"] = related_artists
        for artist in related_artists:
            if artist not in all_artists:
                all_artists.append(artist)
                search_artists.append(artist)

    write_json(all_artists, "all_artists")
    write_json(search_artists, "search_artists")
    

                    


def write_json(new_data, write_to):
    # Check if the file exists and is not empty
    if os.path.exists("artists.json") and os.path.getsize("artists.json") > 0:
        with open("artists.json", 'r+') as file:
            # Load existing data into a dict
            file_data = json.load(file)
            for artist in file_data[write_to]:
                if artist["id"] == new_data["id"]:
                    return  
            # Join new_data with file_data inside emp_details
            file_data[write_to].append(new_data)
            # Sets file's current position at offset
            file.seek(0)
            # Convert back to json
            json.dump(file_data, file, indent=4)
    else:
        # If file does not exist or is empty, create it with initial data
        with open("artists.json", 'w') as file:
            file_data = {"all_artists": [new_data], "search_artists": [new_data]}
            json.dump(file_data, file, indent=4)



if __name__ == '__main__':
    start_time = datetime.now()
    token = get_token()

    while True:
        
    input_new = input("New artist?? y/n")
    if input_new == "y":
        artist_name = input("Enter artist name: ")
        artist = get_artist(token, artist_name)
        artist["related_artists"] = get_related_artists(token, artist["id"])
        write_json(artist, "all_artists")
        write_json(artist, "search_artists")
    


   


    

