CREATE TABLE visitors (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    userID INTEGER,
    roomID INTEGER
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    roomID INTEGER,
    userID INTEGER,
    message TEXT,
    sent_at TIMESTAMP
);
