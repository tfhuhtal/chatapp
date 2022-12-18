CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    room_id INTEGER REFERENCES rooms,
    visible BOOLEAN
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    privacy BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    room_id INTEGER REFERENCES rooms
);

CREATE INDEX users_username_idx ON users (username);
CREATE INDEX participants_user_id_idx ON participants (user_id);
CREATE INDEX participants_room_id_idx ON participants (room_id);
CREATE INDEX rooms_name_idx ON rooms (name);
CREATE INDEX messages_room_id_idx ON messages (room_id);
CREATE INDEX messages_user_id_idx ON messages (user_id);
CREATE INDEX admins_user_id_idx ON admins (user_id);
CREATE INDEX admins_room_id_idx ON admins (room_id);