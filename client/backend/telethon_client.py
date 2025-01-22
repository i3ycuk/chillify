from telethon import events
from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

# Теперь можно импортировать brain.py
from brain import GetHistoryRequest, TelegramClient, asyncio, API_ID, API_HASH


class TelegramClientWrapper:
    def __init__(self):
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        self.new_message_callback = None

    def set_new_message_callback(self, callback):
        """Установить callback для новых сообщений."""
        self.new_message_callback = callback

    async def start(self):
        await self.client.start()

        # Регистрируем обработчик новых сообщений
        @self.client.on(events.NewMessage)
        async def handler(event):
            if self.new_message_callback:
                self.new_message_callback(event.message)

    async def get_dialogs(self):
        """Получить список диалогов."""
        dialogs = await self.client.get_dialogs()
        return dialogs

    async def get_messages(self, chat_id, limit=100):
        """Получить сообщения из чата."""
        messages = await self.client(GetHistoryRequest(
            peer=chat_id,
            limit=limit,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        return messages.messages

    async def send_message(self, chat_id, text):
        """Отправить сообщение в чат."""
        await self.client.send_message(chat_id, text)

    async def disconnect(self):
        """Отключиться от Telegram."""
        await self.client.disconnect()