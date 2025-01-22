from models.user import User
from backend.database import Database

class CRMService:
    def __init__(self):
        self.db = Database()

    def get_clients(self):
        """Получить список клиентов."""
        self.db.cursor.execute("SELECT * FROM users")
        clients = self.db.cursor.fetchall()
        return [User(*client) for client in clients]

    def get_notes(self, client_name):
        """Получить заметки клиента."""
        self.db.cursor.execute("SELECT note FROM notes WHERE user_id = (SELECT user_id FROM users WHERE username = %s)", (client_name,))
        return [note[0] for note in self.db.cursor.fetchall()]

    def add_note(self, client_name, note):
        """Добавить заметку."""
        self.db.execute("INSERT INTO notes (user_id, note) VALUES ((SELECT user_id FROM users WHERE username = %s), %s)", (client_name, note))

    def add_tag(self, client_name, tag):
        """Добавить тег."""
        self.db.execute("UPDATE users SET tags = array_append(tags, %s) WHERE username = %s", (tag, client_name))

    def update_status(self, client_name, status):
        """Изменить статус."""
        self.db.execute("UPDATE users SET status = %s WHERE username = %s", (status, client_name))