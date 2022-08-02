from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib



db = SQLAlchemy()

def encode_string(string):
    string = str(string)
    string = hashlib.md5(string.encode())
    string = string.hexdigest()
    return string

def add_user_db(user, state, playlist_id):
    user_insert = Users(
        id=user["user_id"], user_name=user["user_name"], state=state, playlist_id = playlist_id)
    db.session.add(user_insert)
    db.session.commit()
    return


def add_auth_db(token, id):
    db_user = Users.query.filter_by(id=str(id)).first()
    id = encode_string(id)

    db_user.id = id
    db.session.merge(db_user)
    db.session.commit()

    expired = datetime.timedelta(seconds=token["expires_in"])  + datetime.datetime.now()
    token_insert = Auth(user_id=id, token=token["access_token"], refresh_token=token["refresh_token"], expired_in=expired)
    db.session.add(token_insert)
    db.session.commit()
    
   
    return

def update_token_db(db_user, token):
    expired = datetime.timedelta(seconds=token["expires_in"])  + datetime.datetime.now()
    db_user.token = token["access_token"]
    db_user.refresh_token = token["refresh_token"]
    db_user.expired_in = expired
    db.session.merge(db_user)
    db.session.commit()
    return
    

def update_playlist_id(db_user, playlist_id):
    db_user.playlist_id = playlist_id
    db.session.merge(db_user)
    db.session.commit()
    return





class Users(db.Model):
    id = db.Column(db.String(), primary_key=True, nullable=False)
    user_name = db.Column(db.String(), nullable=True)
    joined_date = db.Column(db.DateTime(), nullable=False,
                            server_default=func.now())
    last_used = db.Column(db.DateTime(), nullable=False,
                          server_default=func.now(), onupdate=func.now())
    state = db.Column(db.String(), nullable=False, unique=True)
    playlist_id = db.Column(db.String(), nullable=True, unique=True)
    auth = db.relationship("Auth", uselist=False)


class Auth(db.Model):
    user_id = db.Column(db.String(), db.ForeignKey(
        'users.id'), nullable=False, primary_key=True)
    token = db.Column(db.String(), nullable=False, unique=True)
    refresh_token = db.Column(db.String(), nullable=False, unique=True)
    expired_in = db.Column(db.DateTime(), nullable=False)
