from brain import sqlite3, logging, dp, types, psycopg2, DB_SETTINGS, datetime, json

logger = logging.getLogger(__name__)

# Подключение к базе данных
def connect_db():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        return conn
    except psycopg2.Error as e:
        logging.critical(f"Ошибка подключения к базе данных: {e}")
        raise

# Создание таблиц
def create_db():
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, -- Уникальный ID пользователя.
                        first_name TEXT, -- Имя пользователя.
                        last_name TEXT, -- Фамилия пользователя.
                        username TEXT, -- Тег (никнейм) пользователя.
                        chats_info JSONB, -- JSON со списком чатов и статистикой сообщений. Пример: {"chat_id1": {"name": "Чат1", "messages": 25}, "chat_id2": {"name": "Чат2", "messages": 10}}
                        total_messages INTEGER DEFAULT 0, -- Общее количество сообщений пользователя.
                        last_seen TIMESTAMP WITH TIME ZONE, -- Время последней активности (в формате UTC).
                        first_message_date TIMESTAMP WITH TIME ZONE, -- Интересы пользователя (в виде строки или JSON). 
                        birth_date DATE, -- Дата рождения.
                        interests TEXT, -- Интересы пользователя (в виде строки или JSON). 
                        language TEXT, -- Язык пользователя (например, "ru", "en").
                        status TEXT,
                        last_start_message_id INTEGER,
                        last_bot_message_id INTEGER
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY, -- Уникальный ID сообщения.
                        user_full_name TEXT, -- Имя и фамилия пользователя, отправившего сообщение.
                        username TEXT, -- Тег пользователя, отправившего сообщение.
                        user_id INTEGER REFERENCES users(id), -- ID пользователя. 
                        chat_name TEXT, -- Название чата, где было отправлено сообщение.
                        chat_id BIGINT, -- ID чата, где было отправлено сообщение.
                        chat_type TEXT, -- Тип чата (private, group, supergroup).
                        message_text TEXT, -- Текст сообщения.
                        message_date TIMESTAMP WITH TIME ZONE, -- Дата и время отправки сообщения.
                        message_id_in_chat INTEGER -- 	ID сообщения в рамках чата.
                    )
                """)
            conn.commit()
    except psycopg2.Error as e:
        logging.critical(f"Ошибка создания таблиц: {e}")
        raise

# Добавление/обновление пользователя
def add_user(user_id, first_name, last_name, username, birth_date, interests, language, status=None):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (id, first_name, last_name, username, chats_info, total_messages, last_seen, first_message_date, birth_date, interests, language, status)
                    VALUES (%s, %s, %s, %s, %s::jsonb, 0, NULL, NULL, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET 
                        first_name = %s, 
                        last_name = %s, 
                        username = %s, 
                        birth_date = %s, 
                        interests = %s, 
                        language = %s,
                        status = %s,
                        last_seen = NULL
                """, (user_id, first_name, last_name, username, "{}", birth_date, interests, language, status, first_name, last_name, username, birth_date, interests, language, status))
                conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logger.critical(f"Ошибка добавления/обновления пользователя {user_id}: {e}")
        raise

# Добавление сообщения
def add_message(user_id, user_full_name, username, chat_name, chat_id, chat_type, message_text, message_id_in_chat):
    now = datetime.utcnow()
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO messages (user_full_name, username, user_id, chat_name, chat_id, chat_type, message_text, message_date, message_id_in_chat)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_full_name, username, user_id, chat_name, chat_id, chat_type, message_text, now, message_id_in_chat))

                cursor.execute("""
                    UPDATE users
                    SET chats_info = CASE
                        WHEN chats_info IS NULL THEN %s::jsonb
                        ELSE chats_info || %s::jsonb
                    END,
                    total_messages = total_messages + 1,
                    last_seen = %s,
                    first_message_date = COALESCE(first_message_date, %s)
                    WHERE id = %s
                """, (json.dumps({str(chat_id): {"name": chat_name, "messages": 1}}), json.dumps({str(chat_id): {"messages": 1}}), now, now, user_id))
                conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Ошибка добавления сообщения от пользователя {user_id} в чат {chat_id}: {e}", exc_info=True)
        raise

# Получение данных пользователя по ID
def get_user(user_id):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    columns = [desc[0] for desc in cursor.description]
                    user_dict = dict(zip(columns, user_data))
                    return user_dict
                return None
    except psycopg2.Error as e:
        logging.error(f"Ошибка получения пользователя {user_id}: {e}")
        return None

# Получение языка пользователя
def get_user_language(user_id):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT language FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                return result[0] if result else None
    except psycopg2.Error as e:
        logging.error(f"Ошибка получения языка пользователя {user_id}: {e}")
        return None

# Функция для получения информации о чате пользователя
def get_user_chat_info(user_id, chat_id):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT chats_info FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    chats_info = json.loads(result[0])
                    return chats_info.get(str(chat_id))
                return None
    except psycopg2.Error as e:
        logging.error(f"Ошибка получения информации о чате пользователя {user_id} в чате {chat_id}: {e}")
        return None

# Обновление ID сообщений start/menu
def update_user_messages(user_id, user_message_id, bot_message_id):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE users SET last_start_message_id = %s, last_bot_message_id = %s WHERE id = %s
                """, (user_message_id, bot_message_id, user_id))
                conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Ошибка обновления ID сообщений пользователя {user_id}: {e}")
        conn.rollback()