from db import db
import users


def get_rooms():
    sql = """SELECT r.name, r.id, count(p.user_id)
            FROM rooms r
            LEFT JOIN participants p
            ON r.id = p.room_id AND p.visible=TRUE
            GROUP BY r.name, r.id"""
    room_list = db.session.execute(sql).fetchall()
    rooms = users.rooms()
    result = []
    for xroom in rooms:
        for yroom in room_list:
            if xroom[1] == yroom[1]:
                result.append(yroom)
    return result


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


def add_room(room_name):
    try:
        sql = "INSERT INTO rooms (name) VALUES (:room_name)"
        db.session.execute(sql, {"room_name":room_name})
        db.session.commit()
    except:
        return False
    room_id = db.session.execute("SELECT id FROM rooms WHERE name=:n", {"n": room_name}).fetchone()
    users.set_admin(room_id[0])
    return users.join_room(room_name)


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
        sql = """UPDATE participants SET visible=FALSE WHERE user_id=:uid AND room_id=:rid"""
        db.session.execute(sql, {"uid":idn, "rid":users.get_room_id()})
        db.session.commit()
    except:
        return False
    return True


def is_admin():
    sql = """SELECT u.id
            FROM users u, admins a
            WHERE u.id = a.user_id AND u.id=:uid AND a.room_id=:rid"""
    admins= db.session.execute(sql,{"uid":users.get_user_id(),"rid":users.get_room_id()}).fetchall()
    for admin in admins:
        if admin[0] == users.get_user_id():
            return True
    return False
