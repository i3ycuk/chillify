from brain import DATABASE_FILE, CACHE_EXPIRATION_TIME, sqlite3, timezone, logging, datetime, json

def create_cache_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_cache (
                    message_id INTEGER PRIMARY KEY,
                    chat_id INTEGER,
                    message_data TEXT,
                    expire_time TEXT
                )
            """)
            conn.commit()
        logging.info("Cache table created (or already exists).")
    except sqlite3.Error as e:
        logging.error(f"Error creating cache table: {e}")

def store_message_data(message_id, chat_id, message_data):
    expire_time = (datetime.now(timezone.utc) + CACHE_EXPIRATION_TIME).isoformat()
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO message_cache (message_id, chat_id, message_data, expire_time)
                VALUES (?, ?, ?, ?)
            """, (message_id, chat_id, json.dumps(message_data), expire_time))
            conn.commit()
        logging.info(f"Stored message data for message {message_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error storing message data: {e}")

def get_message_data(message_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message_data FROM message_cache WHERE message_id = ?", (message_id,))
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None
    except sqlite3.Error as e:
        logging.error(f"Error getting message data: {e}")
        return None

def delete_message_data(message_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM message_cache WHERE message_id = ?", (message_id,))
            conn.commit()
        logging.info(f"Deleted message data for message {message_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error deleting message data: {e}")

def cleanup_cache():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute("DELETE FROM message_cache WHERE expire_time < ?", (now,))
            conn.commit()
        logging.info("Expired cache entries cleaned up.")
    except sqlite3.Error as e:
        logging.error(f"Error cleaning up cache: {e}")