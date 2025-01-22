from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit, QLineEdit, QPushButton
from backend.telethon_client import TelegramClientWrapper
import asyncio

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = TelegramClientWrapper()
        self.client.set_new_message_callback(self.on_new_message)
        self.init_ui()

    def on_new_message(self, message):
        """Обработчик новых сообщений."""
        self.message_display.append(f"{message.sender_id}: {message.text}")

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.returnPressed.connect(self.search_messages)

        # Кнопка поиска
        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.search_messages)


        # Список чатов
        self.chat_list = QListWidget()
        self.chat_list.itemClicked.connect(self.on_chat_selected)

        # Поле для сообщений
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)

        # Поле для ввода сообщения
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)

        # Кнопка отправки
        self.send_button = QPushButton("Отправить")
        self.send_button.clicked.connect(self.send_message)

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.chat_list)
        layout.addWidget(self.message_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        # Загружаем чаты
        asyncio.run_coroutine_threadsafe(self.load_chats(), asyncio.get_event_loop())

    async def load_chats(self):
        """Загрузить список чатов."""
        await self.client.start()
        dialogs = await self.client.get_dialogs()
        for dialog in dialogs:
            self.chat_list.addItem(dialog.name)

    def on_chat_selected(self, item):
        """Обработчик выбора чата."""
        self.message_display.clear()
        chat_name = item.text()
        asyncio.run_coroutine_threadsafe(self.load_messages(chat_name), asyncio.get_event_loop())

    def search_messages(self):
        """Поиск сообщений."""
        query = self.search_input.text()
        if query:
            asyncio.run_coroutine_threadsafe(self.load_messages(query), asyncio.get_event_loop())

    async def load_messages(self, query):
        """Загрузить сообщения по запросу."""
        messages = await self.client.get_messages(self.chat_list.currentItem().text())
        for message in messages:
            if query.lower() in message.text.lower():
                self.message_display.append(f"{message.sender_id}: {message.text}")

    def send_message(self):
        """Отправить сообщение."""
        text = self.message_input.text()
        if text:
            self.message_display.append(f"Вы: {text}")
            self.message_input.clear()
            asyncio.run_coroutine_threadsafe(self.client.send_message(self.chat_list.currentItem().text(), text), asyncio.get_event_loop())