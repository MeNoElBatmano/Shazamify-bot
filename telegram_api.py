from cgitb import reset
from email import header
from email.quoprimime import body_check, header_check
import requests
import json
import db_manager
from main import config


def send_message(user, text):
    bot = config.get('bot')
    method = "sendMessage"
    chat_id = user["chat_id"]
    text = text
    url = f"https://api.telegram.org/{bot}/{method}"

    body = {
        "chat_id": chat_id,
        "text": text
    }

    headers = {
        "Content-Type": "application/json"
    }

    body = json.dumps(body)
    r = requests.post(url=url, data=body, headers=headers)
    print(r)
    print(url)
    return r


def catch_user(req):
    chat_id = req["message"]["chat"]["id"]
    if req["message"]["chat"].get("username"):
        user_name = req["message"]["chat"].get("username")   
    else:
        user_name = "None"
    
    user_id = req["message"]["from"]["id"]

    user_id = db_manager.encode_string(user_id)
    res = {
        "user_id": user_id,
        "chat_id": chat_id,
        "user_name": user_name
    }

    return res
