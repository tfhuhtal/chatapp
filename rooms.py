'''rooms module'''

from db import db
import users

def get_rooms():
    '''returns rooms'''
    
    query = "SELECT r.name FROM participants p, rooms r WHERE p.user_id=:x AND r.id = p.room_id"
    list = db.session.execute(query, {"x":users.user_id()}).fetchall()
    return list