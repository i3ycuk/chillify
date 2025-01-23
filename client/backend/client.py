from telethon import TelegramClient
from telethon.events import NewMessage
from brain import API_ID, API_HASH  # ����������� �� ����

class TelegramClientWrapper:
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.client = TelegramClient("session_name", self.api_id, self.api_hash)

    def start(self):
        """������ �������."""
        self.client.start()
        self.client.run_until_disconnected()

    def add_handler(self, handler):
        """�������� ����������."""
        self.client.add_event_handler(handler)