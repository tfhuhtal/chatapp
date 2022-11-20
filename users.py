'''User module'''

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    '''login'''

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False


def logout():
    '''logout function'''

    del session["user_id"]


def register(username, password):
    '''register'''

    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def add_room(room_name):
    '''add room'''

    try:
        sql = "INSERT INTO rooms (name) VALUES (:room_name)"
        db.session.execute(sql, {"room_name":room_name})
        db.session.commit()
    except:
        return False
    return join_room(room_name)


def join_room(room_name):
    '''adds user to room'''
    
    try:  
        rid = db.session.execute("SELECT id FROM rooms WHERE name=:n", {"n": room_name}).fetchone()
        sql = "INSERT INTO participants (user_id, room_id) VALUES (:uid, :rid)"
        db.session.execute(sql, {"uid":user_id(), "rid":rid[0]})
        db.session.commit()
    except:
        return False
    return True


def user_id():
    '''returns users id'''
    
    return session.get("user_id",0)