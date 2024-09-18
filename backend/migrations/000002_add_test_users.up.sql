CREATE TYPE role_type AS ENUM ('COACH', 'MEDICAL');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role role_type NOT NULL
);