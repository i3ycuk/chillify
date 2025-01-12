import sqlite3
import logging
from datetime import datetime, timedelta

DATABASE_FILE = "message_cache.db"
EXPIRATION_TIME = timedelta(days=1)

def create_cache_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_cache (
                    user_id INTEGER PRIMARY KEY,
                    group_message_id INTEGER,
                    group_bot_message_id INTEGER,
                    private_message_id INTEGER,
                    expire_time TEXT
                )
            """)
            conn.commit()
        logging.info("Cache table created (or already exists).")
    except sqlite3.Error as e:
        logging.error(f"Error creating cache table: {e}")

def store_message_data(user_id, group_message_id=None, group_bot_message_id=None, private_message_id=None):
    expire_time = (datetime.utcnow() + EXPIRATION_TIME).isoformat()
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO message_cache (user_id, group_message_id, group_bot_message_id, private_message_id, expire_time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, group_message_id, group_bot_message_id, private_message_id, expire_time))
            conn.commit()
        logging.info(f"Stored message data for user {user_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error storing message data: {e}")

def get_message_data(user_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM message_cache WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Error getting message data: {e}")
        return None

def delete_message_data(user_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM message_cache WHERE user_id = ?", (user_id,))
            conn.commit()
        logging.info(f"Deleted message data for user {user_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error deleting message data: {e}")

def cleanup_cache():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute("DELETE FROM message_cache WHERE expire_time < ?", (now,))
            conn.commit()
        logging.info("Expired cache entries cleaned up.")
    except sqlite3.Error as e:
        logging.error(f"Error cleaning up cache: {e}")