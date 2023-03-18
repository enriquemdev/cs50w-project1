CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(40),
    hashed_pass VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
