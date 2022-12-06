import os
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False


def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def join_room(room_name):
    room_id = db.session.execute("SELECT id FROM rooms WHERE name=:n", {"n":room_name}).fetchone()
    try:
        sql = "INSERT INTO participants (user_id, room_id, visible) VALUES (:uid, :rid, TRUE)"
        db.session.execute(sql, {"uid":get_user_id(), "rid":room_id[0]})
        db.session.commit()
    except:
        return False
    return True


def send_message(content):
    try:
        sql = """INSERT INTO messages (room_id, user_id, content, sent_at)
                VALUES (:room_id, :user_id, :content, NOW())"""
        db.session.execute(sql,{"room_id":get_room_id(),"user_id":get_user_id(),"content":content})
        db.session.commit()
    except:
        return False
    return True


def get_user_id():
    return session.get("user_id",0)


def get_username():
    return session.get("username", 0)


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def get_user_id_by_username(user_name):
    sql = """SELECT id FROM users WHERE username=:un"""
    user_id = db.session.execute(sql, {"un": user_name}).fetchone()
    return user_id[0]


def get_room_id():
    return session.get("room_id", 0)


def set_room_id(room_id):
    session["room_id"] = room_id


def is_member(room_id):
    sql = """SELECT user_id FROM participants WHERE room_id=:id AND visible=TRUE"""
    users = db.session.execute(sql, {"id":room_id}).fetchall()
    for user in users:
        if user[0] == get_user_id():
            return True
    return False


def set_admin(room_id):
    try:
        sql = """INSERT INTO admins (user_id, room_id) VALUES (:user_id, :room_id)"""
        db.session.execute(sql, {"user_id":get_user_id(), "room_id":room_id})
    except:
        return False
    return True


def rooms():
    sql = """SELECT r.name, r.id
            FROM participants p, rooms r
            WHERE p.user_id=:uid AND p.room_id = r.id AND p.visible=TRUE"""
    users_rooms = db.session.execute(sql, {"uid": get_user_id()}).fetchall()
    return users_rooms
