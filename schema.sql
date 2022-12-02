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
    name TEXT UNIQUE
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