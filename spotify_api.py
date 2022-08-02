import requests
import json
import telegram_api


def get_id(token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}

    r = requests.get(url=url, headers=headers)
    r = r.json()
    return r["id"]





def set_playlist(token):
    spotify_id = get_id(token)
    url = f"https://api.spotify.com/v1/users/{spotify_id}/playlists"
    data = {
        "name":"Shazamify",
        "description": "Playlist created by shazamify bot",
        "public": False
    }
    data = json.dumps(data)
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    
    r = requests.post(url=url, data=data, headers=headers)
    r = r.json()


    return r["id"]






def add_song(token, uri, user, db_user):
    playlist_id = db_user.playlist_id
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    uri = uri
    body = {f"uris": [uri]}
    print(body)
    body = json.dumps(body)
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}

    r = requests.post(url=url, data=body, headers=headers)
    if not r:
        telegram_api.send_message(user, "Sorry but I could not add the track")
    else:
        telegram_api.send_message(user, "Track added succesfully")
    print(r.text)


def find_song(token, song, user):
    name = song["name"]
    artist = song["artist"]

    type = "track"
    q = f"track:{name}+artist:{artist}"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    url = f"https://api.spotify.com/v1/search?type={type}&include_external=audio&q={q}"
    r = requests.get(url=url, headers=headers)
    r = r.json()
    if not r["tracks"]["items"]:
        telegram_api.send_message(
            user, "Sorry but I could not find this track ):")
    song_uri = r["tracks"]["items"][0]["uri"]
    
    return song_uri
 