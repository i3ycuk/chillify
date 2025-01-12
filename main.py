from brain import Dispatcher, os, importlib, logging, dp, localization, asyncio, clear_cache_daily, DEBUG, CACHE_CLEANUP_INTERVAL, QApplication, QTextEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTabWidget, QLabel, TelegramClient, events, sync, SESSION_NAME, API_ID, API_HASH

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

# Класс для работы с кэшем
class Cache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def delete(self, key):
        self.cache.pop(key, None)

    async def auto_cleanup(self, interval):
        while True:
            await asyncio.sleep(interval)
            self.cache.clear()
            logging.info("Cache cleared.")

cache = Cache()

def register_handlers_from_directory(dp, handlers_dir="handlers"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    handlers_path = os.path.join(base_dir, handlers_dir)

    if not os.path.exists(handlers_path):
        raise FileNotFoundError(f"Папка '{handlers_dir}' не найдена.")

    init_file = os.path.join(handlers_path, "__init__.py")
    if not os.path.exists(init_file):
        logging.warning(f"В папке '{handlers_dir}' отсутствует файл '__init__.py'. Возможны проблемы с импортом.")

    for file_name in os.listdir(handlers_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = f"{handlers_dir}.{file_name[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(dp)
                else:
                    logging.warning(f"Модуль {module_name} не содержит функции register.")
            except ImportError as e:
                logging.error(f"Ошибка при импорте модуля {module_name}: {e}")
            except Exception as e:
                logging.exception(f"Неожиданная ошибка при регистрации обработчиков из {module_name}:")

# Регистрируем обработчики
print("Запуск регистрации обработчиков.")
register_handlers_from_directory(dp)
print("Регистрация обработчиков завершена.")
print("Начинаем polling...")
print("Бот запущен!")

# Инициализация клиента Telethon
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# GUI клиента
class TelegramClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chillify 🌿 - Telegram Client")
        self.setGeometry(100, 100, 900, 700)

        self.tabs = QTabWidget(self)

        # Логирование
        self.logs_tab = QWidget()
        self.text_area = QTextEdit(self.logs_tab)
        self.text_area.setReadOnly(True)
        logs_layout = QVBoxLayout()
        logs_layout.addWidget(self.text_area)
        self.logs_tab.setLayout(logs_layout)
        self.tabs.addTab(self.logs_tab, "Логи")

        # Сообщения
        self.messages_tab = QWidget()
        self.chat_id_input = QLineEdit(self.messages_tab)
        self.chat_id_input.setPlaceholderText("Введите chat_id")

        self.message_input = QTextEdit(self.messages_tab)
        self.message_input.setPlaceholderText("Введите сообщение")

        self.send_button = QPushButton("Отправить", self.messages_tab)
        self.send_button.clicked.connect(self.send_message)

        messages_layout = QVBoxLayout()
        messages_layout.addWidget(QLabel("Chat ID:"))
        messages_layout.addWidget(self.chat_id_input)
        messages_layout.addWidget(QLabel("Сообщение:"))
        messages_layout.addWidget(self.message_input)
        messages_layout.addWidget(self.send_button)
        self.messages_tab.setLayout(messages_layout)
        self.tabs.addTab(self.messages_tab, "Сообщения")

        # Чаты
        self.chats_tab = QWidget()
        self.chats_list = QTextEdit(self.chats_tab)
        self.chats_list.setReadOnly(True)
        self.load_chats_button = QPushButton("Загрузить чаты", self.chats_tab)
        self.load_chats_button.clicked.connect(self.load_chats)

        chats_layout = QVBoxLayout()
        chats_layout.addWidget(self.chats_list)
        chats_layout.addWidget(self.load_chats_button)
        self.chats_tab.setLayout(chats_layout)
        self.tabs.addTab(self.chats_tab, "Чаты")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def log(self, message):
        self.text_area.append(message)

    def send_message(self):
        chat_id = self.chat_id_input.text()
        message = self.message_input.toPlainText()

        if not chat_id or not message:
            self.log("Chat ID и сообщение не могут быть пустыми.")
            return

        async def send():
            try:
                await client.send_message(chat_id, message)
                self.log(f"Сообщение отправлено в чат {chat_id}: {message}")
            except Exception as e:
                self.log(f"Ошибка при отправке сообщения: {e}")

        client.loop.create_task(send())

    def load_chats(self):
        async def load():
            try:
                dialogs = await client.get_dialogs()
                self.chats_list.clear()
                for dialog in dialogs:
                    self.chats_list.append(f"{dialog.name or dialog.title}: {dialog.id}")
                self.log("Чаты успешно загружены.")
            except Exception as e:
                self.log(f"Ошибка при загрузке чатов: {e}")

        client.loop.create_task(load())

# Основная логика запуска
async def main():
    await client.start()
    logging.info("Telegram Client Started")

    app = QApplication([])
    gui = TelegramClientGUI()
    gui.show()

    app.exec_()

async def on_startup(dispatcher):
    asyncio.create_task(clear_cache_daily())
    logging.info("Cache cleaning task has been started.")

# Запуск приложения
if __name__ == '__main__':
    client.loop.run_until_complete(main())
