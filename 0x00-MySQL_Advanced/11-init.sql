-- Initial
DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
    name VARCHAR(255) NOT NULL,
    score INT default 0,
    last_meeting DATE NULL 
);