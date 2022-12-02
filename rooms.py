from db import db
import users

def get_rooms():
    sql = """SELECT r.name, r.id
            FROM participants p, rooms r
            WHERE p.user_id=:user_id AND r.id = p.room_id AND p.visible=TRUE"""
    room_list = db.session.execute(sql, {"user_id":users.get_user_id()}).fetchall()
    return room_list


def get_room(room_id):
    sql = "SELECT name FROM rooms WHERE id=:room_id"
    room = db.session.execute(sql, {"room_id":room_id}).fetchone()
    return room


def get_messages(room_id):
    sql = """SELECT u.username, m.sent_at, m.content
            FROM users u, messages m 
            WHERE m.room_id=:rid AND m.user_id = u.id ORDER BY m.sent_at"""
    messages = db.session.execute(sql, {"rid":room_id}).fetchall()
    return messages


def get_members(room_id):
    sql = """SELECT u.username
    FROM users u, participants p
    WHERE u.id = p.user_id AND p.room_id=:rid AND p.visible=TRUE"""
    members = db.session.execute(sql, {"rid":room_id}).fetchall()
    return members

def update_name(room_name):
    try:
        sql = """UPDATE rooms SET name=:room_name WHERE id=:rid"""
        db.session.execute(sql, {"room_name":room_name, "rid":users.get_room_id()})
        db.session.commit()
    except:
        return False
    return True

def remove_user(user_name):
    idn = users.get_user_id_by_username(user_name)
    try:
        sql = """UPDATE participants SET visible=FALSE WHERE user_id=:id"""
        db.session.execute(sql, {"id":idn})
        db.session.commit()
    except:
        return False
    return True
