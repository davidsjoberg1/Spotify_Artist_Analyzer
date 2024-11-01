import base64
from requests import post, get, exceptions
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    try:
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
    except exceptions.ConnectionError as e:
        print("Error: ", e)
        print("Connection error in get_token, trying again in 5 seconds. Time: ", datetime.now())
        time.sleep(5)
        return get_token()
    

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def get_artist_spotify(token, artist_name, limit=20):
    """
    Make a GET request to the Spotify API for the artist with the given name
    :param token: The access token
    :param artist_name: The name of the artist
    :return: A JSON object representing the first artist in the search results
    """
    
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit={limit}"
    query_url = url + query
    try:
        result = get(query_url, headers=headers)
        if result.status_code != 200:
            token = error_handler(result)
            return get_artist_spotify(token, artist_name)
        json_result = json.loads(result.content)["artists"]["items"]
        return json_result
    except exceptions.ConnectionError as e:
        print("Error: ", e)
        print("Connection error in get_artist_spotify, trying again in 5 seconds. Time: ", datetime.now())
        time.sleep(5)
        return get_artist_spotify(token, artist_name)



def get_related_artists_spotify(token, id):
    """
    Make a GET request to the Spotify API for the related artists of the artist with the given id
    :param token: The access token
    :param id: The id of the artist
    :return: A list of related artists
    """
    try:
        url = "https://api.spotify.com/v1/artists/" + str(id) + "/related-artists"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        if result.status_code != 200:

            token = error_handler(result)
            return get_related_artists_spotify(token, id)
            
        related_artists = json.loads(result.content)["artists"]
        return related_artists
    except exceptions.ConnectionError as e:
        print("Error: ", e)
        print("Connection error in get_related_artists_spotify, trying again in 5 seconds. Time: ", datetime.now())
        time.sleep(5)
        return get_related_artists_spotify(token, id)
    

def error_handler(result):
    """
    Handles errors from the Spotify API
    :param result: The result of the request
    :return: A new access token
    """
    print("Error: ", result.status_code)
    print("Current time: ", datetime.now()) 
    print("Response: ", result.headers)

    if result.status_code == 429:
        print("Sleeping for: ", result.headers["retry-after"], " seconds = ", round(int(result.headers["retry-after"])/3600, 2), " hours")
        print("Starting again: ", datetime.fromtimestamp(datetime.now().timestamp() + int(result.headers["retry-after"])))
        time.sleep(int(result.headers["retry-after"]))
    time.sleep(5)
    return get_token()
    

    
    
    



