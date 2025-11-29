PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS facilities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  details TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  facility_id INTEGER REFERENCES facilities(id),
  date TEXT,
  start_time TEXT,
  need_equipment INTEGER DEFAULT 0,
  created_at TEXT
);

DELETE FROM facilities;
INSERT INTO facilities (name, details) VALUES
('Cricket Ground 1','Full-size cricket ground with nets.'),
('Cricket Ground 2','Full-size match ground.'),
('Lawn Tennis Courts','6 courts (4 synthetic, 2 cemented).'),
('Basketball Courts','3 courts (1 synthetic, 2 cemented).'),
('Volleyball Courts','4 well-maintained courts.'),
('Badminton Courts','11 courts (1 indoor, 10 open-air).'),
('Table Tennis Hall','4 tables, indoor facility.');
