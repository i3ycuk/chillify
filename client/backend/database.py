from brain import psycopg2, DB_SETTINGS

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_SETTINGS)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        """Выполнить SQL-запрос."""
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_all(self, query, params=None):
        """Получить все результаты запроса."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        """Закрыть соединение с базой данных."""
        self.cursor.close()
        self.conn.close()