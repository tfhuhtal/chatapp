from db import db
import users


def get_rooms():
    sql = """SELECT r.name, r.id, COUNT(p.user_id) OVER (PARTITION BY r.id)
            FROM rooms r
            LEFT JOIN participants p
            ON r.id = p.room_id AND p.visible = TRUE"""
    room_list = db.session.execute(sql).fetchall()
    rooms = users.rooms()
    rooms_dict = {xroom[1]: True for xroom in rooms}
    result = [yroom for yroom in room_list if yroom[1] in rooms_dict]
    return result


def get_room(room_id):
    sql = "SELECT name, id FROM rooms WHERE id=:room_id"
    room = db.session.execute(sql, {"room_id":room_id}).fetchone()
    return room


def get_messages(room_id):
    sql = """SELECT u.username, m.sent_at, m.content, m.id
            FROM users u, messages m 
            WHERE m.room_id=:rid AND m.user_id = u.id ORDER BY m.sent_at DESC"""
    messages = db.session.execute(sql, {"rid":room_id}).fetchall()
    return messages


def get_message(message_id):
    sql = """SELECT u.username, m.sent_at, m.content, m.id
            FROM users u, messages m, participants p
            WHERE m.id=:mid AND m.user_id = u.id AND m.user_id=:uid"""
    message = db.session.execute(sql, {"mid":message_id,"uid":users.get_user_id()}).fetchone()
    return message


def update_message(content, message_id):
    sql = """UPDATE messages SET content=:content WHERE id=:mid"""
    db.session.execute(sql, {"content":content, "mid":message_id})
    db.session.commit()
    return True


def get_members(room_id):
    sql = """SELECT u.username
            FROM users u, participants p
            WHERE u.id = p.user_id AND p.room_id=:rid AND p.visible=TRUE"""
    members = db.session.execute(sql, {"rid":room_id}).fetchall()
    return members


def add_room(room_name):
    try:
        sql = "INSERT INTO rooms (name, privacy) VALUES (:room_name, FALSE)"
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
    sql = """UPDATE participants SET visible=FALSE WHERE user_id=:uid AND room_id=:rid"""
    db.session.execute(sql, {"uid":idn, "rid":users.get_room_id()})
    db.session.commit()
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


def get_results(word):
    sql = """SELECT DISTINCT m.content
            FROM messages m, participants p
            WHERE m.room_id=p.room_id AND p.user_id=:uid
            AND m.content LIKE :word"""
    results = db.session.execute(sql, {"uid":users.get_user_id(), "word":'%'+word+'%'}).fetchall()
    return results


def get_all_rooms():
    sql = """SELECT name FROM rooms"""
    room_list = db.session.execute(sql).fetchall()
    return room_list


def set_private():
    if is_admin():
        sql = """UPDATE rooms SET privacy=TRUE WHERE id=:rid"""
        db.session.execute(sql, {"rid":users.get_room_id()})
        db.session.commit()
        return True
    return False

def set_public():
    if is_admin():
        sql = """UPDATE rooms SET privacy=FALSE WHERE id=:rid"""
        db.session.execute(sql, {"rid":users.get_room_id()})
        db.session.commit()
        return True
    return False

def is_private(room_id):
    sql = """SELECT privacy FROM rooms WHERE id=:rid"""
    result = db.session.execute(sql, {"rid":room_id}).fetchone()
    return result[0]
