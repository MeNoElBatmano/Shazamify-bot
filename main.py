
from email import message
from enum import unique
from lib2to3.pgen2 import token
from flask import Flask, request, session
from flask import request
from sqlalchemy.sql import func
from dotenv import dotenv_values, load_dotenv

import spotify_api
from db_manager import Users, Auth, encode_string, db
import time
import datetime
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import false, null, true
import authentication
import json
import telegram_api
"K_[7>*[AMu!/W3#="
'postgresql://yfiaihzuhsdvez:017a4ebc2f7e453828e0fa49125d4e9fb8830f663625b8ac834b6d68fa724137@ec2-34-253-119-24.eu-west-1.compute.amazonaws.com:5432/df499lq9jknjc3'

config = dotenv_values(".env")

app = Flask(__name__)
app.secret_key = config.get('app_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
db.init_app(app)


def main():

    return 1


@app.route('/', methods=['GET', 'POST'])
def bot():
    if request.method == 'POST':
        req = json.loads(request.get_data())
        print(req)
        message_text = req['message']['text']
        user = telegram_api.catch_user(req)


        if message_text == "/login":
            authentication.authenticate(
                user, first_time=True, authorization_response=None)
            return "Auth began"
        elif message_text == '/help':
            telegram_api.send_message(user, "1. type /login to authenticate with spotify \n2. choose a playlist from your existing personal playlists or use a default one called Shazamify \n3. share shazamed song with the bot (using the built-in share buttin in Shazam \n 4.???? \n 5. PROFIT!!!)")
            return "got help"



        if "Shazam" in message_text:
            hashed_id = encode_string(user["user_id"])
            db_user = Users.query.filter_by(id=str(hashed_id)).first()
            if db_user is None:
                # db_manager.add_user_db(user)
                authentication.authenticate(
                    user, first_time=True, authorization_response=None)
                return "step 1"
            else:
                expired_time = Auth.query.filter_by(user_id=str(hashed_id)).first().expired_in
                if datetime.datetime.now()  > expired_time :
                    db_user_auth = Auth.query.filter_by(user_id=str(hashed_id)).first()
                    authentication.refresh(user, db_user_auth)

                song = {"name": get_song(message_text)["name"],
                "artist": get_artist(message_text, get_song(message_text)["index"])}
           
                db_token = Auth.query.filter_by(user_id=hashed_id).first()
                uri = spotify_api.find_song(db_token.token, song, user)
                spotify_api.add_song(db_token.token, uri, user, db_user)
                return "stop"
        else:
            telegram_api.send_message(user, "Invalid query!")
            return "failed!"

        
        

    elif request.method == 'GET':
        return "What exactly are you trying to GET?"


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        print("called callback!")
        url = request.url
        authentication.authenticate(
            telegram_user=None, first_time=False, authorization_response=url)
    

    return "thank you"


if __name__ == "__main__":
    main()


def get_song(message):

    loc = message.find("discover ")
    loc += len("discover ")

    loc_space = message.find("by", loc) - 1

    name = message[loc:loc_space]
    return {"name": name, "index": loc_space}


def get_artist(message, loc_space):
    loc = message.find("by ", loc_space)
    loc += len("by ")

    loc_end = message.find("http", loc)
    loc_end -= 2

    artist_name = message[loc:loc_end]
    return artist_name




def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


