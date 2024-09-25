CREATE EXTENSION IF NOT EXISTS "citext";

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email citext UNIQUE NOT NULL,
    password TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    current_login_at TIMESTAMP,
    last_login_ip TEXT,
    current_login_ip TEXT,
    login_count INTEGER DEFAULT 0,
    fs_uniquifier TEXT UNIQUE NOT NULL,
    confirmed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    user_id BIGINT,
    role_id BIGINT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (id),
    PRIMARY KEY (user_id, role_id)
);
