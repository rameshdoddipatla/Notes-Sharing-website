-- Run once against your PostgreSQL database (createdb notesapp) if you
-- prefer manual setup instead of letting Flask-SQLAlchemy's db.create_all()
-- create the tables automatically on first run.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(500) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    uploaded_by VARCHAR(255),
    date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);
