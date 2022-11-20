from db import db
import users

def get_rooms():
    sql = "SELECT r.name, r.id FROM participants p, rooms r WHERE p.user_id=:x AND r.id = p.room_id"
    room_list = db.session.execute(sql, {"x":users.user_id()}).fetchall()
    return room_list

def get_room(room_id):
    '''returns room'''

    sql = "SELECT name FROM rooms WHERE id=:room_id"
    room = db.session.execute(sql, {"room_id":room_id}).fetchone()
    return room
