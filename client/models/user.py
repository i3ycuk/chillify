from backend.database import Database

class User:
    def __init__(self, user_id, username, first_name, last_name, tags=None, status=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.tags = tags or []
        self.status = status or "active"

    def save(self):
        db = Database()
        db.execute(
            "INSERT INTO users (user_id, username, first_name, last_name, tags, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.user_id, self.username, self.first_name, self.last_name, self.tags, self.status)
        )
        db.close()