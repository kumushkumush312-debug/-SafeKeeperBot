import sqlite3
import datetime
from config import DATABASE_PATH, BLOCK_DAYS


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Bloklangan foydalanuvchilar jadvali
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocked_users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                block_date TIMESTAMP,
                block_until TIMESTAMP,
                reason TEXT
            )
        ''')

        # Tekshirilgan fayllar jadvali
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scanned_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT,
                file_name TEXT,
                user_id INTEGER,
                scan_result TEXT,
                scan_date TIMESTAMP
            )
        ''')
        self.conn.commit()

    def block_user(self, user_id, username, first_name, reason):
        block_date = datetime.datetime.now()
        block_until = block_date + datetime.timedelta(days=BLOCK_DAYS)

        self.cursor.execute('''
            INSERT OR REPLACE INTO blocked_users 
            (user_id, username, first_name, block_date, block_until, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, block_date, block_until, reason))
        self.conn.commit()

    def is_user_blocked(self, user_id):
        self.cursor.execute('''
            SELECT block_until FROM blocked_users 
            WHERE user_id = ? AND block_until > ?
        ''', (user_id, datetime.datetime.now()))
        return self.cursor.fetchone() is not None

    def add_scan_log(self, file_id, file_name, user_id, result):
        self.cursor.execute('''
            INSERT INTO scanned_files (file_id, file_name, user_id, scan_result, scan_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_id, file_name, user_id, result, datetime.datetime.now()))
        self.conn.commit()