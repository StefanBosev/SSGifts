import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute(
    '''
    CREATE TABLE IF NOT EXISTS Event (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        event_start_date TEXT NOT NULL,
        event_end_date TEXT NOT NULL,
        price_high_border INTEGER,
        price_low_border INTEGER
    )
    '''
)

conn.cursor().execute(
    '''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_first_name TEXT NOT NULL,
        user_last_name TEXT NOT NULL,
        age INTEGER CHECK(age >= 16),
        gender TEXT,
        user_mail TEXT NOT NULL,
        password TEXT NOT NULL,
        address TEXT,
        event_id INTEGER,
        admin NUMERIC default 0,
        FOREIGN KEY(event_id) REFERENCES Event(id)
    )
    '''
)

class DB:
    def __enter__(self):
        self.connection = sqlite3.connect(DB_NAME)
        return self.connection.cursor()

    def __exit__(self, type, value, traceback):
        self.connection.commit()