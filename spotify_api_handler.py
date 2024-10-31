import base64
from requests import post, get
from dotenv import load_dotenv
import os
import json
import time
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



def get_artist_spotify(token, artist_name):
    """
    Make a GET request to the Spotify API for the artist with the given name
    :param token: The access token
    :param artist_name: The name of the artist
    :return: A JSON object representing the first artist in the search results
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=20"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result



def get_related_artists_spotify(token, id):
    """
    Make a GET request to the Spotify API for the related artists of the artist with the given id
    :param token: The access token
    :param id: The id of the artist
    :return: A list of related artists
    """

    url = "https://api.spotify.com/v1/artists/" + str(id) + "/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    try:
        related_artists = json.loads(result.content)["artists"]
        return related_artists
    except json.decoder.JSONDecodeError as e:
        print("Error: ", e)
        print("Response: ", result)
        print("Current time: ", datetime.now()) 
        print("Sleeping for: ", result.headers["retry-after"], " seconds = ", round(int(result.headers["retry-after"])/3600, 2), " hours")
        print("Starting again: ", datetime.fromtimestamp(datetime.now().timestamp() + int(result.headers["retry-after"])))
        time.sleep(int(result.headers["retry-after"]) + 10)
        return get_related_artists(get_token(), id)

    



