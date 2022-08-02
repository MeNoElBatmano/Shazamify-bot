
import re
from urllib import response
from flask import session, redirect
import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import time
import telegram_api
import db_manager
import spotify_api
from main import config





def authenticate(telegram_user, first_time, authorization_response):
    auth_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    redirect_uri = "https://2d83-87-71-179-1.eu.ngrok.io/callback"

    client_id = config.get('client_id')
    client_secret = config.get('client_secret')

    scope = [
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public"
    ]   

    if first_time:
        client = BackendApplicationClient(client_id=client_id)
        spotify = OAuth2Session(client_id, redirect_uri=redirect_uri,
                                scope=scope)
        authorization_url, state = spotify.authorization_url(auth_url)
        db_manager.add_user_db(telegram_user, state, None)

        telegram_api.send_message(
            telegram_user, f"Please go here to authenticate - {authorization_url}")

        return "end first step"

    else:

        loc = authorization_response.find("state=")
        loc += len("state=")
        state = authorization_response[loc:len(authorization_response)]

        db_user = db_manager.Users.query.filter_by(state=str(state)).first()
        if db_user != None:
            authorization_response = f"https://dffffc286267b8.lhrtunnel.link/callback{authorization_response}"
            client = BackendApplicationClient(client_id=client_id)
            spotify = OAuth2Session(client_id, redirect_uri=redirect_uri,
                                    scope=scope)

            auth = HTTPBasicAuth(client_id, client_secret)

            token = spotify.fetch_token(token_url, auth=auth,
                                        authorization_response=authorization_response)
            db_manager.add_auth_db(id=db_user.id, token=token)
            playlist_id = spotify_api.set_playlist(token["access_token"])
            db_manager.update_playlist_id(db_user, playlist_id)



            return 

        else:
            telegram_api.send_message(telegram_user, "error!!!")
            return

    # user_token = {"token":token["access_token"],
    #               "refresh_token": token["refresh_token"],
    #               "expires_in":  token["expires_in"]
    #             }

    # print({user:spotify})
    # print(user_token)
    # return {user:spotify}
    return


def refresh(db_user, db_user_auth):
    grant_type = "refresh_token"
    client_id = config.get('client_id')
    token_url = "https://accounts.spotify.com/api/token"
    client_secret = config.get('client_secret')

    auth = HTTPBasicAuth(client_id, client_secret)
    spotify = OAuth2Session(client_id)
    new_token = spotify.refresh_token(
        token_url=token_url, refresh_token=db_user_auth.refresh_token, auth=auth)
    
    db_manager.update_token_db(db_user_auth, new_token)

    return "refreshed"


# def print_a():
#         if "a" in session:
#                 print(session["a"])
#         print(f"sadsa {session}")
